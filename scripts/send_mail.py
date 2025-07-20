import os
import requests
from pathlib import Path
import markdown
from utils import parse_markdown_with_frontmatter, update_frontmatter_field

CORREOS_DIR = Path("correos")
API_KEY = os.environ["MAILERLITE_API_KEY"]
API_URL = "https://connect.mailerlite.com/api/newsletters"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def crear_newsletter(titulo, contenido_html, send_at=None):
    data = {
        "type": "regular",
        "subject": titulo,
        "name": titulo,
        "html": contenido_html
    }

    if send_at:
        data["schedule"] = {
            "send_at": send_at  # Debe estar en formato ISO 8601
        }

    response = requests.post(API_URL, headers=HEADERS, json=data)
    response.raise_for_status()
    return response.json()

def main():
    archivos = list(CORREOS_DIR.glob("*.md"))
    if not archivos:
        print("No se encontraron correos.")
        return

    for archivo in archivos:
        try:
            front, cuerpo_md = parse_markdown_with_frontmatter(archivo)
        except Exception as e:
            print(f"[ERROR] Al leer {archivo.name}: {e}")
            continue

        if front.get("status") != "sending":
            continue  # ignorar si no está listo para enviar

        titulo = front.get("title")
        if not titulo:
            print(f"[ERROR] Falta título en {archivo.name}")
            continue

        cuerpo_html = markdown.markdown(cuerpo_md)

        try:
            send_at = front.get("send_at")  # debe ser str en formato "2025-07-21T10:00:00+02:00"
            crear_newsletter(titulo, cuerpo_html, send_at)
            update_frontmatter_field(archivo, "status", "sent")
            print(f"[OK] Enviado y actualizado: {archivo.name}")
        except Exception as e:
            print(f"[ERROR] Falló el envío de {archivo.name}: {e}")

if __name__ == "__main__":
    main()
