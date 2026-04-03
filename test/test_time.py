import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from tris.sorting import (
    tri_selection, tri_insertion, bubble_sort,
    quick_sort, tri_fusion, tri_tas, tri_peigne,
)

# Données de test

LISTE_VIDE   = []
LISTE_UN     = [42]
LISTE_TRIEE  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
LISTE_INVERSE= [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
LISTE_RANDOM = [random.randint(1, 1000) for _ in range(200)]
LISTE_DOUBLONS = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

ALGOS_EN_PLACE = [
    ("tri_selection", tri_selection),
    ("tri_insertion", tri_insertion),
    ("bubble_sort",   bubble_sort),
    ("tri_tas",       tri_tas),
    ("tri_peigne",    tri_peigne),
]

ALGOS_RETOURNE = [
    ("quick_sort",  quick_sort),
    ("tri_fusion",  tri_fusion),
]

# Tests 

def _tester_en_place(fn, liste):
    copie = liste.copy()
    compteur = [0]
    fn(copie, compteur)
    return copie, compteur[0]

def _tester_retourne(fn, liste):
    compteur = [0]
    resultat = fn(liste.copy(), compteur)
    return resultat, compteur[0]


class TestAlgosEnPlace:
    def test_liste_vide(self):
        for nom, fn in ALGOS_EN_PLACE:
            res, _ = _tester_en_place(fn, LISTE_VIDE)
            assert res == [], f"{nom} : liste vide doit rester vide"

    def test_liste_un_element(self):
        for nom, fn in ALGOS_EN_PLACE:
            res, _ = _tester_en_place(fn, LISTE_UN)
            assert res == [42], f"{nom} : liste à 1 élément"

    def test_deja_triee(self):
        for nom, fn in ALGOS_EN_PLACE:
            res, _ = _tester_en_place(fn, LISTE_TRIEE)
            assert res == sorted(LISTE_TRIEE), f"{nom} : liste déjà triée"

    def test_ordre_inverse(self):
        for nom, fn in ALGOS_EN_PLACE:
            res, _ = _tester_en_place(fn, LISTE_INVERSE)
            assert res == sorted(LISTE_INVERSE), f"{nom} : ordre inverse"

    def test_aleatoire(self):
        for nom, fn in ALGOS_EN_PLACE:
            res, _ = _tester_en_place(fn, LISTE_RANDOM)
            assert res == sorted(LISTE_RANDOM), f"{nom} : liste aléatoire"

    def test_doublons(self):
        for nom, fn in ALGOS_EN_PLACE:
            res, _ = _tester_en_place(fn, LISTE_DOUBLONS)
            assert res == sorted(LISTE_DOUBLONS), f"{nom} : doublons"

    def test_compteur_incremente(self):
        for nom, fn in ALGOS_EN_PLACE:
            _, ops = _tester_en_place(fn, LISTE_RANDOM)
            assert ops > 0, f"{nom} : compteur doit être > 0"


class TestAlgosRetourne:
    def test_liste_vide(self):
        for nom, fn in ALGOS_RETOURNE:
            res, _ = _tester_retourne(fn, LISTE_VIDE)
            assert res == [], f"{nom} : liste vide"

    def test_liste_un_element(self):
        for nom, fn in ALGOS_RETOURNE:
            res, _ = _tester_retourne(fn, LISTE_UN)
            assert res == [42], f"{nom} : un élément"

    def test_ordre_inverse(self):
        for nom, fn in ALGOS_RETOURNE:
            res, _ = _tester_retourne(fn, LISTE_INVERSE)
            assert res == sorted(LISTE_INVERSE), f"{nom} : ordre inverse"

    def test_aleatoire(self):
        for nom, fn in ALGOS_RETOURNE:
            res, _ = _tester_retourne(fn, LISTE_RANDOM)
            assert res == sorted(LISTE_RANDOM), f"{nom} : liste aléatoire"

    def test_doublons(self):
        for nom, fn in ALGOS_RETOURNE:
            res, _ = _tester_retourne(fn, LISTE_DOUBLONS)
            assert res == sorted(LISTE_DOUBLONS), f"{nom} : doublons"

    def test_compteur_incremente(self):
        for nom, fn in ALGOS_RETOURNE:
            _, ops = _tester_retourne(fn, LISTE_RANDOM)
            assert ops > 0, f"{nom} : compteur doit être > 0"