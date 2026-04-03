# utils/stats_manager.py
"""
Sauvegarde et lecture des statistiques de tri dans stats.json.
Le fichier est créé automatiquement à la racine du projet.
"""

import json
import os
from datetime import datetime

# Chemin absolu vers stats.json à la racine du projet
STATS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "stats.json")


def sauvegarder_stats(nom_algo: str, stats: dict) -> None:
    """
    Ajoute les stats d'un tri à stats.json.
    Crée le fichier s'il n'existe pas.
    """
    historique = charger_stats()

    entree = {
        "date"       : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "algorithme" : nom_algo,
        "taille"     : stats.get("taille", 0),
        "operations" : stats.get("operations", 0),
        "temps_sec"  : round(stats.get("temps_sec", 0.0), 6),
        "memoire_ko" : round(stats.get("memoire_ko", 0.0), 2),
        "pic_ko"     : round(stats.get("pic_ko", 0.0), 2),
        "interrompu" : stats.get("interrompu", False),
    }

    historique.append(entree)

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(historique, f, indent=2, ensure_ascii=False)


def charger_stats() -> list:
    """Retourne l'historique complet depuis stats.json."""
    if not os.path.exists(STATS_FILE):
        return []
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def effacer_stats() -> None:
    """Vide stats.json."""
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=2)