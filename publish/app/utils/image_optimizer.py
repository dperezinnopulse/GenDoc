"""
image_optimizer.py — utilidades para optimizar imágenes en servidores Python (Pillow)
-------------------------------------------------------------------------------
Requisitos:
  pip install pillow==10.4.0

Uso rápido:
  from app.utils.image_optimizer import optimize_image_bytes

  with open("in.png","rb") as f:
      data = f.read()

  out = optimize_image_bytes(
      data,
      target_kb=180,           # tamaño objetivo (KB). Si None, usa 'quality' directo
      format_hint="webp",      # "jpeg" | "webp" | None (elige en base a transparencia)
      max_width=1600,          # redimensionado máximo (mantiene proporción). None = sin cambio
      max_height=1600,
      doc_mode=True            # optimizaciones para documentos/escaneos (grises + nitidez)
  )

  with open("out.webp","wb") as f:
      f.write(out)

Funciones principales:
  - optimize_image_bytes(...): API única de alto nivel
  - save_with_target_filesize(...): compresión con búsqueda binaria a tamaño objetivo

Notas:
  - Para imágenes con transparencia, WebP suele rendir mejor que PNG/JPEG.
  - Para documentos con texto, activar doc_mode mejora legibilidad y peso.
  - progressive=True en JPEG y lossless para WebP cuando convenga.
"""

from io import BytesIO
from typing import Optional, Tuple
from PIL import Image, ImageOps, ImageFilter

# -------- Helpers --------

def _strip_metadata(img: Image.Image) -> Image.Image:
    # crea una copia sin EXIF/ICC para reducir peso
    data = list(img.getdata())
    new = Image.new(img.mode, img.size)
    new.putdata(data)
    return new

def _maybe_downscale(img: Image.Image, max_w: Optional[int], max_h: Optional[int]) -> Image.Image:
    if not max_w and not max_h:
        return img
    w, h = img.size
    scale = 1.0
    if max_w and w > max_w:
        scale = min(scale, max_w / w)
    if max_h and h > max_h:
        scale = min(scale, max_h / h)
    if scale < 1.0:
        # LANCZOS ofrece gran calidad al reducir
        new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
        return img.resize(new_size, Image.LANCZOS)
    return img

def _to_grayscale_if_doc(img: Image.Image, doc_mode: bool) -> Image.Image:
    if not doc_mode:
        return img
    # Para documentos, pasamos a L (grises) para reducir ruido de compresión
    # y aplicamos un sharpening suave para mantener bordes del texto.
    g = ImageOps.grayscale(img)
    # Suavizado + nítidez leve
    g = g.filter(ImageFilter.MedianFilter(size=3))
    g = g.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=8))
    return g

def _has_transparency(img: Image.Image) -> bool:
    if img.mode in ("RGBA", "LA"):
        return True
    if img.mode == "P":
        transparency = img.info.get("transparency", None)
        return transparency is not None
    return False

# -------- Core save with target size --------

def save_with_target_filesize(
    img: Image.Image,
    target_kb: int,
    fmt: str = "jpeg",
    min_quality: int = 35,
    max_quality: int = 95,
    extra_kwargs: dict = None
) -> bytes:
    """
    Guarda 'img' en 'fmt' aproximando el tamaño 'target_kb' mediante
    búsqueda binaria de 'quality'. Devuelve bytes del archivo.
    """
    fmt = fmt.lower()
    params = dict(optimize=True)
    if extra_kwargs:
        params.update(extra_kwargs)

    lo, hi = min_quality, max_quality
    best_bytes = None
    # Intento rápido: calidad media
    while lo <= hi:
        q = (lo + hi) // 2
        buf = BytesIO()
        if fmt == "jpeg":
            params_q = dict(params, quality=q, subsampling=2, progressive=True)
            img.convert("RGB").save(buf, "JPEG", **params_q)
        elif fmt == "webp":
            # WebP con q ajustable, sin lossless aquí
            params_q = dict(params, quality=q, method=6)
            img.save(buf, "WEBP", **params_q)
        else:
            raise ValueError("Formato no soportado para binsearch: " + fmt)

        data = buf.getvalue()
        size_kb = len(data) / 1024
        best_bytes = data if best_bytes is None or abs(size_kb - target_kb) < abs(len(best_bytes)/1024 - target_kb) else best_bytes

        if size_kb > target_kb:
            hi = q - 1
        else:
            lo = q + 1

    return best_bytes

# -------- High level API --------

def optimize_image_bytes(
    data: bytes,
    target_kb: Optional[int] = 180,
    format_hint: Optional[str] = None,  # "jpeg" | "webp" | None
    max_width: Optional[int] = 1800,
    max_height: Optional[int] = 1800,
    doc_mode: bool = False,
    prefer_lossless_for_alpha: bool = True
) -> bytes:
    """
    Optimiza 'data' (bytes de imagen). Pasos:
      1) abre + auto-orienta + elimina metadatos
      2) opcional: downscale a (max_w, max_h)
      3) modo documento (grises + unsharp)
      4) selecciona formato (webp si hay alfa, o hint)
      5) si target_kb -> binsearch calidad; si no -> guarda con calidad fija
    """
    with Image.open(BytesIO(data)) as im:
        # auto-orientación por EXIF
        im = ImageOps.exif_transpose(im)
        # elimina metadatos
        im = _strip_metadata(im)
        # downscale
        im = _maybe_downscale(im, max_width, max_height)
        # doc mode
        im = _to_grayscale_if_doc(im, doc_mode)

        # selección de formato
        has_alpha = _has_transparency(im)
        fmt = (format_hint or "").lower()
        if not fmt:
            if has_alpha:
                fmt = "webp"  # mejor que PNG para web
            else:
                fmt = "jpeg"

        # Guardado
        if target_kb:
            # parámetros extra base
            extra = {}
            if fmt == "jpeg":
                extra = {"progressive": True, "subsampling": 2}
            elif fmt == "webp":
                extra = {"method": 6}

            return save_with_target_filesize(im, target_kb=target_kb, fmt=fmt, extra_kwargs=extra)

        # si no hay target_kb, guardamos con calidades razonables
        buf = BytesIO()
        if fmt == "jpeg":
            im.convert("RGB").save(buf, "JPEG", optimize=True, quality=75, subsampling=2, progressive=True)
        elif fmt == "webp":
            if has_alpha and prefer_lossless_for_alpha and not doc_mode:
                im.save(buf, "WEBP", lossless=True, method=6)
            else:
                im.save(buf, "WEBP", quality=78, method=6)
        else:
            # fallback a PNG optimizado (puede ser pesado)
            im.save(buf, "PNG", optimize=True)
        return buf.getvalue()
