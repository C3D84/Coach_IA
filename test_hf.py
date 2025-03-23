import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
print(f"Token chargé : {HF_TOKEN[:10]}...")  # Masqué partiellement pour vérif

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Accept": "application/json"
}

response = requests.post(
    "https://api-inference.huggingface.co/models/google/flan-t5-base",
    headers=headers,
    json={"inputs": "Génère une séance d'entraînement football U13"},
    timeout=60
)

print("Statut :", response.status_code)
print("Réponse :", response.text)
input("\nAppuie sur Entrée pour fermer...")
