import os
import shutil
import subprocess
import tempfile


def _find_soffice() -> str:
    for name in ["soffice", "/usr/bin/soffice", "/usr/local/bin/soffice"]:
        if shutil.which(name) or os.path.isfile(name):
            return shutil.which(name) or name
    raise FileNotFoundError("LibreOffice (soffice) no encontrado en PATH")


def convert_to_pdf(input_path: str, output_path: str):
    soffice = _find_soffice()
    outdir = os.path.dirname(output_path)
    os.makedirs(outdir, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [
            soffice,
            "--headless",
            "--norestore",
            "--nolockcheck",
            "--nodefault",
            "--convert-to",
            "pdf",
            "--outdir",
            tmp,
            input_path,
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Move resulting pdf (same basename but .pdf) to desired output
        base = os.path.splitext(os.path.basename(input_path))[0]
        produced = os.path.join(tmp, base + ".pdf")
        if not os.path.isfile(produced):
            # Try to find any PDF in tmp
            candidates = [p for p in os.listdir(tmp) if p.lower().endswith('.pdf')]
            if candidates:
                produced = os.path.join(tmp, candidates[0])
        if not os.path.isfile(produced):
            raise RuntimeError("No se pudo convertir a PDF")
        shutil.move(produced, output_path)


def convert_pdf_to_image(pdf_path: str, output_path: str) -> bool:
    """
    Convierte un PDF a imagen PNG usando LibreOffice.
    
    Args:
        pdf_path: Ruta del archivo PDF de entrada
        output_path: Ruta del archivo de imagen de salida
        
    Returns:
        True si la conversión fue exitosa, False en caso contrario
    """
    try:
        soffice = _find_soffice()
        outdir = os.path.dirname(output_path)
        os.makedirs(outdir, exist_ok=True)
        
        with tempfile.TemporaryDirectory() as tmp:
            # LibreOffice puede convertir PDF a imagen usando el formato PNG
            cmd = [
                soffice,
                "--headless",
                "--norestore",
                "--nolockcheck",
                "--nodefault",
                "--convert-to",
                "png",
                "--outdir",
                tmp,
                pdf_path,
            ]
            
            result = subprocess.run(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                timeout=30
            )
            
            if result.returncode != 0:
                return False
            
            # Buscar el archivo PNG generado
            base = os.path.splitext(os.path.basename(pdf_path))[0]
            produced = os.path.join(tmp, base + ".png")
            
            if not os.path.isfile(produced):
                # Buscar cualquier PNG en tmp
                candidates = [p for p in os.listdir(tmp) if p.lower().endswith('.png')]
                if candidates:
                    produced = os.path.join(tmp, candidates[0])
            
            if not os.path.isfile(produced):
                return False
            
            # Mover el archivo a la ubicación deseada
            shutil.move(produced, output_path)
            return True
            
    except Exception as e:
        print(f"Error convirtiendo PDF a imagen: {e}")
        return False