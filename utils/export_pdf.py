# utils/export_pdf.py

from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Programme d'entraînement football", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def exporter_programme_pdf(programme: str, titre: str = "entrainement") -> bytes:
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "", 12)

    for ligne in programme.split("\n"):
        ligne_clean = ligne.strip()
        ligne_clean = ligne_clean.encode("latin-1", "replace").decode("latin-1")
        if not ligne_clean:
            continue

        pdf.multi_cell(0, 10, ligne_clean)

        # Tentative d'ajout d'image liée à l'exercice
        nom_exercice = (
            ligne_clean.lower()
            .replace("é", "e")
            .replace("è", "e")
            .replace("ê", "e")
            .replace("à", "a")
            .replace(" ", "_")
            .replace("'", "")
            .replace("-", "_")
        )
        chemin_image = os.path.join("ressources", "plans", f"{nom_exercice}.png")
        if os.path.exists(chemin_image):
            pdf.ln(3)
            pdf.image(chemin_image, w=120)
            pdf.ln(5)

    # Sauvegarde temporaire
    chemin_temp = os.path.join("utils", f"{titre}.pdf")
    pdf.output(chemin_temp)

    with open(chemin_temp, "rb") as f:
        contenu_pdf = f.read()

    os.remove(chemin_temp)
    return contenu_pdf
