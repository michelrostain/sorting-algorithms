
# Persistance des statistiques de tri dans un fichier JSON local.

import json
import os
from datetime import datetime

STATS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "stats.json")


def sauvegarder_stats(nom_algo: str, stats: dict) -> None:
    """
    Ajoute une entrée dans stats.json avec horodatage.
    """
    entree = {
        "date"       : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "algorithme" : nom_algo,
        **stats,
    }

    historique: list = []
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                historique = json.load(f)
        except (json.JSONDecodeError, OSError):
            historique = []

    historique.append(entree)

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(historique, f, ensure_ascii=False, indent=2)


def charger_stats() -> list[dict]:
    """
    Retourne tout l'historique, ou [] si le fichier n'existe pas.
    """
    if not os.path.exists(STATS_FILE):
        return []
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []