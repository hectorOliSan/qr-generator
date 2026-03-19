#!/usr/bin/env python3

import io
import qrcode
import sys

from imgcat import imgcat
from io import BytesIO
from pathlib import Path
from qrcode.constants import ERROR_CORRECT_Q
from qrcode.image.svg import SvgPathImage
from qrcode.main import QRCode

from decorators import handle_errors, print_styled

OUTPUT_DIR = Path("output")

@handle_errors("Error al crear el código QR")
def create_qr(url: str) -> QRCode:
    """Crea un objeto QRCode a partir de una URL."""
    qr: QRCode = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_Q,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr

@handle_errors("Error al guardar el código QR")
def save_qr_as_svg(qr: QRCode, filename: str) -> Path:
    """Guarda el código QR como archivo SVG en el directorio output."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    if not filename.endswith(".svg"):
        filename += ".svg"

    filepath: Path = OUTPUT_DIR / filename
    img_svg: SvgPathImage = qr.make_image(image_factory=SvgPathImage)
    img_svg.save(stream=str(object=filepath))
    return filepath

@handle_errors("Error al guardar el código QR")
def save_qr_as_png(qr: QRCode, filename: str) -> Path:
    """Guarda el código QR como archivo PNG en el directorio output."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    if not filename.endswith(".png"):
        filename += ".png"

    filepath: Path = OUTPUT_DIR / filename
    img_png = qr.make_image(fill_color="black", back_color="white")
    img_png.save(filepath)
    return filepath

@handle_errors("Error al mostrar el código QR en la terminal")
def display_qr_in_terminal(qr: QRCode) -> None:
    """Muestra el código QR en la terminal usando imgcat."""
    img_png: BytesIO = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img_png.save(buffer, format="PNG")
    imgcat(data=buffer.getvalue())

@handle_errors("Error al generar el código QR")
def generate_qr(url: str, filename: str) -> None:
    """Genera un código QR, lo guarda como SVG y lo muestra en la terminal."""
    qr: QRCode = create_qr(url=url)
    saved_filepath_svg: Path = save_qr_as_svg(qr=qr, filename=filename)
    saved_filepath_png: Path = save_qr_as_png(qr=qr, filename=filename)
    print_styled(
        message=f"✓ QR generado correctamente: {saved_filepath_svg}\n",
        color="green"
    )
    print_styled(
        message=f"✓ QR generado correctamente: {saved_filepath_png}\n",
        color="green"
    )
    display_qr_in_terminal(qr=qr)

def main():
    """Función principal que maneja la ejecución del script."""
    if len(sys.argv) != 3:
        print_styled(
            message="Número de argumentos inválido\n",
            error_type="ValueError",
            color="red"
        )
        print_styled(
            message="📖 Uso: python main.py <url> <filename>",
            color="cyan"
        )
        print_styled(
            message="📝 Ejemplo: python main.py https://ejemplo.com qr_code",
            color="cyan"
        )
        sys.exit(1)

    url: str = sys.argv[1]
    filename: str = sys.argv[2]
    generate_qr(url=url, filename=filename)

if __name__ == "__main__":
    main()
