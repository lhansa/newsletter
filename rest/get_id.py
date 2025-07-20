import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="../scripts/.env.local")  # o el path que prefieras

API_KEY = os.environ["MAILERLITE_API_KEY"]

response = requests.get(
    "https://connect.mailerlite.com/api/groups",
    headers={
        "Authorization": f"Bearer {API_KEY}"
    }
)

if response.status_code == 200:
    for grupo in response.json()['data']:
        print(f"{grupo['name']} → {grupo['id']}")
else:
    print("Error al obtener los grupos:", response.status_code, response.text)
