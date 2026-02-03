import qrcode
from PIL import Image
import os

DEFAULT_QR_COLOR = "#000000"
DEFAULT_BG_COLOR = "#FFFFFF"
OUTPUT_FILE = "MyQR.png"

def ask(prompt, default=None):
    value = input(prompt).strip()
    return value if value else default

def file_exists(path):
    return path and os.path.isfile(path)

url = ask("Ingrese la URL: ")
if not url:
    print("La URL es obligatoria")
    exit(1)

qr_color = ask(
    f"Color del QR en hex [{DEFAULT_QR_COLOR}]: ",
    DEFAULT_QR_COLOR
)

bg_color = ask(
    f"Color de fondo en hex [{DEFAULT_BG_COLOR}]: ",
    DEFAULT_BG_COLOR
)

logo_path = ask("Ruta del logo (PNG): ")

if not file_exists(logo_path):
    print("Ruta de logo inválida o archivo inexistente")
    exit(1)

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)

qr.add_data(url)
qr.make(fit=True)

qr_img = qr.make_image(
    fill_color=qr_color,
    back_color=bg_color
).convert("RGBA")

logo = Image.open(logo_path).convert("RGBA")

qr_w, qr_h = qr_img.size
logo_size = qr_w // 4
logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

pos = (
    (qr_w - logo_size) // 2,
    (qr_h - logo_size) // 2
)

qr_img.paste(logo, pos, logo)

qr_img.save(OUTPUT_FILE)

print(f"QR generado correctamente: {OUTPUT_FILE}")
