import os
import requests
import random
from pathlib import Path
import markdown
from utils import parse_markdown_with_frontmatter, update_frontmatter_field

# from dotenv import load_dotenv
# load_dotenv(dotenv_path=".env.local")  # o el path que prefieras


CORREOS_DIR = Path("../correos")
API_KEY = os.environ["MAILERLITE_API_KEY"]
API_URL_CREATE = "https://connect.mailerlite.com/api/campaigns"
API_URL_SCHEDULE = "https://connect.mailerlite.com/api/campaigns/{id}/schedule"


HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def crear_newsletter(titulo, contenido_html, send_at=None):
    data = {
        "type": "regular",
        "name": titulo,
        "status": "draft", 
        "emails": [
            {
                "from": "hola@leonardohansa.com", 
                "from_name": "Leonardo Hansa",
                "reply_to": "hola@leonardohansa.com",
                "subject": titulo,
                "content": "hola"
            }
        ],
        # "scheduled_for": send_at.strftime('%Y-%m-%d %H:%M:%S'),
        "scheduled_for": "2025-07-21 18:40:00",
        "groups": ["160454873555404503"] # ["93330267065812572"]
    }

    response = requests.post(API_URL_CREATE, headers=HEADERS, json=data)
    response.json()
    response.raise_for_status()
    return response.json()

def main():
    archivos = list(CORREOS_DIR.glob("*.md"))
    if not archivos:
        print("No se encontraron correos.")
        return

    for archivo in archivos:
        # archivo = archivos[0]
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
