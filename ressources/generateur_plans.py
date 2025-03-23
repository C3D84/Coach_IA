# generateur_plans.py

from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("ressources/plans", exist_ok=True)

def dessiner_exercice_simple(nom_fichier, titre, elements):
    img = Image.new("RGB", (600, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Terrain simplifié
    draw.rectangle([50, 50, 550, 350], outline="green", width=4)
    draw.line([300, 50, 300, 350], fill="green", width=2)
    draw.ellipse([270, 170, 330, 230], outline="green", width=2)

    for el in elements:
        if el[0] == "joueur":
            x, y = el[1]
            draw.ellipse([x-8, y-8, x+8, y+8], fill="blue", outline="black")
        elif el[0] == "plot":
            x, y = el[1]
            draw.ellipse([x-4, y-4, x+4, y+4], fill="orange", outline="black")
        elif el[0] == "fleche":
            (x1, y1), (x2, y2) = el[1]
            draw.line([x1, y1, x2, y2], fill="red", width=2)
            draw.polygon([(x2, y2), (x2-5, y2-5), (x2-5, y2+5)], fill="red")

    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()

    draw.text((60, 360), titre, fill="black", font=font)
    img.save(os.path.join("ressources/plans", nom_fichier))

# === 3 exemples à générer ===
dessiner_exercice_simple(
    "atelier_passe_et_suit.png",
    "Atelier passe et suit",
    [
        ("joueur", (120, 100)),
        ("joueur", (200, 180)),
        ("joueur", (280, 260)),
        ("fleche", ((120, 100), (200, 180))),
        ("fleche", ((200, 180), (280, 260))),
    ]
)

dessiner_exercice_simple(
    "jeu_en_triangle.png",
    "Jeu en triangle",
    [
        ("joueur", (200, 150)),
        ("joueur", (300, 100)),
        ("joueur", (400, 150)),
        ("fleche", ((200, 150), (300, 100))),
        ("fleche", ((300, 100), (400, 150))),
        ("fleche", ((400, 150), (200, 150))),
    ]
)

dessiner_exercice_simple(
    "animation_offensive_en_433.png",
    "Animation offensive en 4-3-3",
    [
        ("joueur", (250, 300)),
        ("joueur", (300, 250)),
        ("joueur", (350, 200)),
        ("joueur", (400, 150)),
        ("fleche", ((250, 300), (300, 250))),
        ("fleche", ((300, 250), (350, 200))),
        ("fleche", ((350, 200), (400, 150))),
    ]
)
