import streamlit as st
import os
import json
import pandas as pd
import io
from ia.generateur_entrainement import generer_programme_ia, generer_planification_seances
from utils.export_txt import exporter_programme_txt
from utils.export_pdf import exporter_programme_pdf

# === CONFIGURATION ===
st.set_page_config(page_title="Coach IA - Assistant Entraîneur", layout="wide")

# === Chargement du profil coach ===
profil_path = os.path.join("ressources", "profil.json")
profil = {"nom": "Coach", "club": "", "logo": ""}

if os.path.exists(profil_path):
    with open(profil_path, "r", encoding="utf-8") as f:
        profil.update(json.load(f))

# === MENU LATÉRAL ===
if profil.get("logo") and os.path.exists(profil["logo"]):
    st.sidebar.image(profil["logo"], width=100)
else:
    st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Football_iu_1996.svg/512px-Football_iu_1996.svg.png", width=80)

st.sidebar.title(f"⚙️ {profil.get('nom', 'Coach')} - Menu")
choix = st.sidebar.radio("Navigation", [
    "🏠 Accueil",
    "🎯 Générer une séance IA",
    "📅 Planification multi-séances",
    "📋 Entraînement manuel",
    "➕ Ajouter un exercice",
    "⭐ Mes exercices",
    "👤 Mon profil"
])

# === ACCUEIL ===
if choix == "🏠 Accueil":
    st.title(f"👋 Bienvenue {profil.get('nom', 'Coach')} !")
    st.markdown(f"""
    Bienvenue dans votre assistant d'entraînement **Coach IA** pour le club **{profil.get('club', '')}**.

    Ce logiciel vous permet de :
    - Générer automatiquement des séances d'entraînement adaptées ⚽
    - Planifier plusieurs séances cohérentes 📅
    - Composer vos propres séances 📋
    - Enrichir votre base d’exercices ➕
    - Noter et filtrer vos exercices ⭐
    - Exporter votre base en Excel 📤

    **Choisissez une option dans le menu à gauche.**
    """)

# === GENERATEUR IA ===
elif choix == "🎯 Générer une séance IA":
    st.title("🎯 Générateur IA de séance")
    categorie = st.selectbox("Catégorie d'âge :", ["U9", "U11", "U13", "U15", "U17", "Sénior"])
    objectif = st.selectbox("Objectif principal :", ["Technique", "Physique", "Tactique", "Mixte"])
    duree = st.slider("Durée de la séance (minutes)", 30, 120, 75, step=5)
    nb_joueurs = st.slider("Nombre de joueurs disponibles", 6, 25, 14)
    frequence = st.selectbox("Nombre de séances par semaine :", [1, 2, 3, 4, 5])
    gardiens = st.checkbox("🧤 Inclure un programme spécifique pour gardiens de but", value=False)

    if st.button("Générer la séance"):
        with st.spinner("Génération IA en cours..."):
            programme = generer_programme_ia(categorie, objectif, duree, nb_joueurs, frequence, gardiens)
        st.success("✅ Séance générée !")
        st.text(programme)
        st.download_button("📥 Télécharger en .txt", exporter_programme_txt(programme), "entrainement.txt", mime="text/plain")
        st.download_button("📤 Télécharger en PDF", exporter_programme_pdf(programme), "entrainement.pdf", mime="application/pdf")

# === PLANIFICATION MULTI-SEANCES ===
elif choix == "📅 Planification multi-séances":
    st.title("📅 Planification intelligente de plusieurs séances")
    categorie = st.selectbox("Catégorie d'âge :", ["U9", "U11", "U13", "U15", "U17", "Sénior"], key="cat_planif")
    objectif = st.selectbox("Objectif principal :", ["Technique", "Physique", "Tactique", "Mixte"], key="obj_planif")
    duree = st.slider("Durée de chaque séance", 30, 120, 75, step=5, key="dur_planif")
    nb_joueurs = st.slider("Effectif moyen", 6, 25, 14, key="nb_planif")
    frequence = st.selectbox("Séances par semaine", [1, 2, 3, 4, 5], key="freq_planif")
    gardiens = st.checkbox("Inclure gardiens ?", key="gard_planif")
    nb_seances = st.slider("Nombre de séances à générer :", 2, 5, 3)

    if st.button("Générer les séances"):
        with st.spinner("Création des séances..."):
            liste = generer_planification_seances(categorie, objectif, duree, nb_joueurs, frequence, gardiens, nb_seances)
        st.success("✅ Planification terminée !")
        for i, prog in enumerate(liste, 1):
            st.markdown(f"### 🗓️ Séance {i}")
            st.text(prog)
        st.download_button("📤 Télécharger toute la planification en PDF", exporter_programme_pdf("\n\n".join(liste), titre="planification"), "planification.pdf", mime="application/pdf")

# === ENTRAINEMENT MANUEL ===
elif choix == "📋 Entraînement manuel":
    st.title("📋 Composer manuellement un entraînement")
    chemin_exos = os.path.join("ressources", "exercices.json")
    if os.path.exists(chemin_exos):
        with open(chemin_exos, "r", encoding="utf-8") as f:
            base_exos = json.load(f)
    else:
        st.warning("Aucune base d'exercices trouvée.")
        base_exos = {}

    categorie_manuelle = st.selectbox("Choisissez une catégorie :", list(base_exos.keys()))
    selection = []
    if categorie_manuelle:
        for exo in base_exos[categorie_manuelle]:
            with st.expander(f"{exo['nom']} ({exo.get('duree', 'N/A')}) - ⭐ {exo.get('note', 3)}/5"):
                st.markdown(f"🎯 {exo.get('description', '')}")
                st.markdown(f"🧰 Matériel : {exo.get('materiel', '')}")
                if st.checkbox(f"✅ Ajouter « {exo['nom']} »", key=exo['nom']):
                    selection.append(exo)

    if selection:
        plan = "PLAN D’ENTRAÎNEMENT MANUEL\n\nÉchauffement libre (10-15min)\n"
        for i, exo in enumerate(selection, 1):
            plan += f"\nAtelier {i} : {exo['nom']} ({exo['duree']})\nObjectif : {exo['description']}\nMatériel : {exo['materiel']}\n"
        plan += "\nRetour au calme / étirements\nConseils du coach"

        st.text(plan)
        st.download_button("📥 Télécharger en .txt", exporter_programme_txt(plan), "entrainement_personnalise.txt", mime="text/plain")
        st.download_button("📤 Télécharger en PDF", exporter_programme_pdf(plan, titre="entrainement_personnalise"), "entrainement_personnalise.pdf", mime="application/pdf")

# === AJOUT D’EXERCICE ===
elif choix == "➕ Ajouter un exercice":
    st.title("➕ Ajouter un nouvel exercice")

    chemin_exos = os.path.join("ressources", "exercices.json")
    if os.path.exists(chemin_exos):
        with open(chemin_exos, "r", encoding="utf-8") as f:
            base_exos = json.load(f)
    else:
        base_exos = {"exercices": []}

    with st.form("form_ajout"):
        nom = st.text_input("Nom de l'exercice")
        duree = st.text_input("Durée (ex: 10 min)")
        description = st.text_area("Description")
        materiel = st.text_input("Matériel")
        niveau = st.selectbox("Niveau", ["U9", "U11", "U13", "U15", "U17"])
        note = st.slider("Note", 1, 5, 3)
        submitted = st.form_submit_button("✅ Ajouter")

        if submitted:
            exo = {
                "nom": nom,
                "duree": duree,
                "description": description,
                "materiel": materiel,
                "niveau": niveau,
                "note": note
            }
            base_exos["exercices"].append(exo)
            with open(chemin_exos, "w", encoding="utf-8") as f:
                json.dump(base_exos, f, indent=4, ensure_ascii=False)
            st.success(f"✅ Exercice '{nom}' ajouté avec succès.")


# === PAGE PROFIL COACH ===
elif choix == "👤 Mon profil":
    st.title("👤 Mon profil d'entraîneur")
    with st.form("form_profil"):
        nom_coach = st.text_input("Nom du coach", value=profil.get("nom", ""))
        club = st.text_input("Nom du club", value=profil.get("club", ""))
        logo_upload = st.file_uploader("📸 Logo du club (PNG ou JPG)", type=["png", "jpg", "jpeg"])
        submitted = st.form_submit_button("💾 Sauvegarder le profil")
    if submitted:
        if logo_upload:
            dossier_logos = os.path.join("ressources", "logos")
            os.makedirs(dossier_logos, exist_ok=True)
            chemin_logo = os.path.join(dossier_logos, logo_upload.name)
            with open(chemin_logo, "wb") as f:
                f.write(logo_upload.read())
            profil["logo"] = chemin_logo
        profil["nom"] = nom_coach
        profil["club"] = club
        with open(profil_path, "w", encoding="utf-8") as f:
            json.dump(profil, f, indent=4)
        st.success("✅ Profil mis à jour avec succès ! Veuillez recharger la page pour voir les changements.")

elif choix == "⭐ Mes exercices":
    st.title("⭐ Ma bibliothèque d'exercices")

    chemin_exos = os.path.join("ressources", "exercices.json")
    if os.path.exists(chemin_exos):
        with open(chemin_exos, "r", encoding="utf-8") as f:
            base_exos = json.load(f)
    else:
        st.warning("Aucun fichier d'exercices trouvé.")
        base_exos = {"exercices": []}

    recherche = st.text_input("🔍 Rechercher un mot-clé")
    niveau_filtre = st.selectbox("🎓 Filtrer par niveau :", ["Tous", "U9", "U11", "U13", "U15", "U17"])

    exercices = base_exos.get("exercices", [])
    modif = False

    for i, exo in enumerate(exercices):
        nom = exo.get("nom", "")
        if recherche and recherche.lower() not in nom.lower():
            continue
        if niveau_filtre != "Tous" and exo.get("niveau") != niveau_filtre:
            continue

        with st.expander(f"{nom} ({exo.get('duree')}) – Niveau {exo.get('niveau')} ⭐{exo.get('note', 3)}"):
            st.markdown(f"📝 {exo.get('description')}")
            st.markdown(f"📦 Matériel : {exo.get('materiel', 'N/A')}")
            nouvelle_note = st.slider("⭐ Note", 1, 5, exo.get("note", 3), key=f"note_{i}")
            if nouvelle_note != exo.get("note", 3):
                base_exos["exercices"][i]["note"] = nouvelle_note
                modif = True

    if modif:
        with open(chemin_exos, "w", encoding="utf-8") as f:
            json.dump(base_exos, f, indent=4, ensure_ascii=False)
        st.toast("💾 Modifications sauvegardées.")


    for cat, idx in reversed(exercice_a_supprimer):
        del base_exos[cat][idx]
        modif_effectuee = True

    if modif_effectuee:
        with open(chemin_exos, "w", encoding="utf-8") as f:
            json.dump(base_exos, f, indent=4, ensure_ascii=False)
        st.toast("💾 Modifications sauvegardées avec succès.")

    # EXPORT EXCEL
    if st.button("📥 Exporter toute la base au format Excel (.xlsx)"):
        liste_export = []
        for cat, exercices in base_exos.items():
            for exo in exercices:
                ligne = {
                    "Catégorie": cat,
                    "Nom": exo.get("nom", ""),
                    "Description": exo.get("description", ""),
                    "Matériel": exo.get("materiel", ""),
                    "Durée": exo.get("duree", ""),
                    "Note": exo.get("note", ""),
                    "Niveau": exo.get("niveau", "")
                }
                liste_export.append(ligne)

        df = pd.DataFrame(liste_export)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name="Exercices")
        buffer.seek(0)

        st.download_button(
            label="📊 Télécharger le fichier Excel",
            data=buffer,
            file_name="base_exercices_coachIA.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

