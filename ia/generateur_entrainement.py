# ia/generateur_entrainement.py

import requests
import json
import random
import os

def charger_exercices(objectif, inclure_gardiens=False):
    chemin = os.path.join("ressources", "exercices.json")
    if not os.path.exists(chemin):
        return "", []

    with open(chemin, "r", encoding="utf-8") as f:
        data = json.load(f)

    exercices = data.get(objectif, [])
    exercices_choisis = random.sample(exercices, min(2, len(exercices)))

    if inclure_gardiens and "Gardiens" in data:
        gardien_exos = random.sample(data["Gardiens"], min(1, len(data["Gardiens"])))
        exercices_choisis += gardien_exos

    texte_exos = "\n".join(
        f"- {exo['nom']} ({exo['duree']}): {exo['description']} [Matériel: {exo['materiel']}]"
        for exo in exercices_choisis
    )

    return texte_exos, exercices_choisis

def generer_programme_ia(categorie, objectif, duree, nb_joueurs, frequence, gardiens, progression=None):
    exemples_exos, _ = charger_exercices(objectif, inclure_gardiens=gardiens)
    progression_txt = f"\nSéance axée sur : {progression}" if progression else ""

    prompt = f"""
Tu es un éducateur de football diplômé FFF. Tu rédiges des plans d'entraînement détaillés pour des équipes {categorie}.

Ton objectif est de proposer une séance complète, cohérente, et directement utilisable sur le terrain.

Chaque séance doit inclure :
1. Échauffement (avec durée, objectif, description)
2. Corps de séance (2 à 3 ateliers nommés avec :
   - Titre
   - Durée
   - Objectif
   - Description précise
   - Variante possible
)
3. Partie spécifique gardiens (si activée)
4. Retour au calme / étirements
5. Conseils du coach

Paramètres à prendre en compte :
- Niveau de l'équipe : {categorie}
- Objectif principal : {objectif}
- Durée : {duree} minutes
- Nombre de joueurs : {nb_joueurs}
- Séances par semaine : {frequence}
- Programme spécifique gardiens : {"Oui" if gardiens else "Non"}
{progression_txt}

Voici quelques exemples d'exercices à utiliser ou adapter :
{exemples_exos}

Règles :
- Reste entièrement en français
- Évite les anglicismes ou termes techniques en anglais
- Utilise un vocabulaire clair, pédagogique, professionnel
- Ne répète pas les titres comme "Voici le programme" : va droit au but

Commence directement par l’échauffement.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        return response.json()["response"].strip()
    except Exception as e:
        return f"❌ Erreur avec le moteur IA local : {e}"

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
