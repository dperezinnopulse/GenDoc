import os
import shutil
import subprocess
import tempfile


def _find_soffice() -> str:
    # Check Windows LibreOffice installation
    windows_paths = [
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
    ]
    for path in windows_paths:
        if os.path.isfile(path):
            return path
    
    # Check PATH
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
