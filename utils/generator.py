# Génération de listes de nombres réels aléatoires.

import random


def generer_liste(n: int, vmin: float = 0.0, vmax: float = 10_000.0) -> list[float]:
    """
    Retourne une liste de `n` flottants aléatoires dans [vmin, vmax].
    """
    return [random.uniform(vmin, vmax) for _ in range(n)]