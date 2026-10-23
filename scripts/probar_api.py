"""Prueba de un solo uso: ¿acepta la API de MailerLite el cuerpo (content) con mi plan?

Crea una campaña borrador con HTML propio y, si sale bien, la borra.
No envía nada a nadie.

Uso: cd scripts && python probar_api.py
"""
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env.local")

API_KEY = os.environ["MAILERLITE_API_KEY"]
GROUP_ID = os.environ.get("MAILERLITE_GROUP_ID")  # opcional para la prueba
API_URL = "https://connect.mailerlite.com/api/campaigns"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

HTML_PRUEBA = """<html><body>
<p>Correo de prueba. Si lees esto en MailerLite, la API acepta content.</p>
<p><a href="{$unsubscribe}">Darse de baja</a></p>
</body></html>"""


def main():
    data = {
        "type": "regular",
        "name": "PRUEBA API - borrar",
        "emails": [
            {
                "from": "hola@leonardohansa.com",
                "from_name": "Leonardo Hansa",
                "reply_to": "hola@leonardohansa.com",
                "subject": "PRUEBA API - borrar",
                "content": HTML_PRUEBA,
            }
        ],
    }
    if GROUP_ID:
        data["groups"] = [GROUP_ID]

    response = requests.post(API_URL, headers=HEADERS, json=data)
    if not response.ok:
        print(f"[ERROR] La API rechaza la campaña ({response.status_code}):")
        print(response.text)
        sys.exit(1)

    campana_id = response.json()["data"]["id"]
    print(f"[OK] La API acepta content. Campaña de prueba creada: {campana_id}")

    borrado = requests.delete(f"{API_URL}/{campana_id}", headers=HEADERS)
    if borrado.ok:
        print("[OK] Campaña de prueba borrada.")
    else:
        print(f"[AVISO] No se pudo borrar ({borrado.status_code}), bórrala a mano en MailerLite:")
        print(borrado.text)


if __name__ == "__main__":
    main()
