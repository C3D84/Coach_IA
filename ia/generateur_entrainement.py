# ia/generateur_entrainement.py

import requests
import json
import random
import os
from dotenv import load_dotenv
load_dotenv()

import os
HF_TOKEN = os.getenv("HF_TOKEN")



def charger_exercices(objectif, inclure_gardiens=False):
    chemin = os.path.join("ressources", "exercices.json")
    if not os.path.exists(chemin):
        return "", []

    with open(chemin, "r", encoding="utf-8") as f:
        data = json.load(f)

    tous_exos = data.get("exercices", [])
    exercices_choisis = []

    if tous_exos:
        exercices_choisis = random.sample(tous_exos, min(3, len(tous_exos)))

    texte_exos = "\n".join(
        f"- {exo['nom']} ({exo['duree']}): {exo['description']} [Matériel: {exo['materiel']}]"
        for exo in exercices_choisis
    )

    return texte_exos, exercices_choisis

def generer_programme_ia(categorie, objectif, duree, nb_joueurs, frequence, gardiens, progression=None):
    exemples_exos, _ = charger_exercices(objectif, inclure_gardiens=gardiens)
    progression_txt = f"\nSéance axée sur : {progression}" if progression else ""

    prompt = f"""
Tu es un entraîneur de football diplômé UEFA B. Tu rédiges des plans d'entraînement complets, cohérents et réalistes pour des joueurs {categorie}.

Ton objectif : proposer une séance structurée, pédagogique et directement applicable sur le terrain.

Contexte :
- Objectif principal : {objectif}
- Nombre de joueurs : {nb_joueurs}
- Durée : {duree} minutes
- Fréquence : {frequence} fois par semaine
- Gardiens spécifiques : {"Oui" if gardiens else "Non"}
{progression_txt}

Ta réponse doit inclure :
1. Échauffement (durée, objectif, consignes)
2. Corps de séance (2 à 3 ateliers avec nom, objectif, description, variantes)
3. Travail gardien (si activé)
4. Retour au calme
5. Conseils du coach

IMPORTANT : Rédige ta réponse uniquement en bon français clair et naturel. Utilise un ton professionnel, comme un éducateur de club de niveau national.

Voici des exemples d'exercices à utiliser ou adapter :
{exemples_exos}

Commence directement par la fiche séance :
"""

    try:
        hf_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
        headers = {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Accept": "application/json"
        }

        response = requests.post(
            hf_url,
            headers=headers,
            json={"inputs": prompt},
            timeout=120
        )

        if response.status_code == 200:
            resultat = response.json()
            texte_genere = resultat[0]["generated_text"]
            return texte_genere
        else:
            return f"❌ Erreur HuggingFace [{response.status_code}] : {response.text}"

    except Exception as e:
        return f"❌ Erreur lors de l’appel HuggingFace : {str(e)}"




def generer_planification_seances(categorie, objectif, duree, nb_joueurs, frequence, gardiens, nb_seances=3):
    seances = []
    progres = ["Travail technique", "Circulation de balle", "Transitions offensives", "Pressing collectif", "Jeu combiné"]

    for i in range(nb_seances):
        progression = progres[i % len(progres)] if objectif == "Mixte" else None
        seance = generer_programme_ia(
            categorie=categorie,
            objectif=objectif,
            duree=duree,
            nb_joueurs=nb_joueurs,
            frequence=frequence,
            gardiens=gardiens,
            progression=progression
        )
        seances.append(f"🗓️ Séance {i+1} - {progression if progression else objectif}\n\n{seance}")

    return seances
