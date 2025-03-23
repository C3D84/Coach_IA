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
Tu es un entraîneur diplômé UEFA B, responsable de la planification des entraînements pour une équipe de football {categorie}. 
Ton rôle est de proposer des séances structurées, précises et adaptées aux objectifs suivants :

- Objectif principal : {objectif}
- Nombre de joueurs disponibles : {nb_joueurs}
- Durée de la séance : {duree} minutes
- Nombre de séances hebdomadaires : {frequence}
- Programme spécifique gardiens : {"Oui" if gardiens else "Non"}

Ta séance doit comporter :
1. **Échauffement actif** : avec un objectif précis, durée, consignes claires
2. **Corps de séance** : 2 à 3 ateliers avec :
   - 🎯 Nom de l’atelier
   - ⏱️ Durée
   - 🎯 Objectif pédagogique
   - 📋 Description précise, consignes, variantes
3. **Travail spécifique gardien** (si activé) : avec description, matériel, intégration
4. **Retour au calme** : étirements, récupération
5. **Conseils du coach** : attitude, communication, progression

Utilise un **vocabulaire clair**, sans jargon, **en français uniquement**.  
Formate la réponse comme une **fiche séance prête à imprimer**.  
Structure bien les blocs avec titres et sauts de ligne.  
N’utilise **aucun anglicisme**.

Commence directement par l’échauffement.
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
            timeout=60
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
