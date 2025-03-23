# utils/export_txt.py

def exporter_programme_txt(contenu: str) -> bytes:
    """
    Prépare le contenu pour le téléchargement en .txt
    """
    return contenu.encode("utf-8")
