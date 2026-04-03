"""
Génère des listes aléatoires pour les tests de tri.
"""

import random


def generer_liste(n: int, min_val: int = 1, max_val: int = 100_000) -> list:
    """
    Retourne une liste de n entiers aléatoires entre min_val et max_val.

    Paramètres
    ----------
    n       : nombre d'éléments
    min_val : valeur minimale (défaut 1)
    max_val : valeur maximale (défaut 100 000)
    """
    return [random.randint(min_val, max_val) for _ in range(n)]