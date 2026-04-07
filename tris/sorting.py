# Implémentation des 7 algorithmes de tri.

# Signature commune:

#     fn(liste: list, compteur: list[int], **kwargs) -> None | list

#   - `liste`    : liste à trier (modifiée en place sauf tri_fusion / quick_sort)
#   - `compteur` : compteur[0] est incrémenté à chaque opération élémentaire
#   - `stop_flag`  (Event, facultatif) : arrêt anticipé pour algos lents
#   - `pause_flag` (Event, facultatif) : pause pour algos lents

# Les algos rapides (fusion, rapide, tas, peigne) ignorent stop_flag/pause_flag.
# Les algos lents  (sélection, insertion, bulles) les respectent.

import threading


# ──────────────────────────────────────────────────────────────────────────────
#  Utilitaire interne
# ──────────────────────────────────────────────────────────────────────────────

def _check(stop_flag, pause_flag) -> bool:
    """
    Gère la pause et retourne True si on doit s'arrêter.
    """
    if pause_flag is not None:
        pause_flag.wait()          # bloque tant que l'event est effacé
    if stop_flag is not None and stop_flag.is_set():
        return True
    return False


# ──────────────────────────────────────────────────────────────────────────────
#  1. Tri par sélection  — O(n²)  lent
# ──────────────────────────────────────────────────────────────────────────────

def tri_selection(liste: list, compteur: list,
                  stop_flag=None, pause_flag=None) -> None:
    n = len(liste)
    for i in range(n):
        if _check(stop_flag, pause_flag):
            return
        min_idx = i
        for j in range(i + 1, n):
            compteur[0] += 1
            if liste[j] < liste[min_idx]:
                min_idx = j
        liste[i], liste[min_idx] = liste[min_idx], liste[i]


# ──────────────────────────────────────────────────────────────────────────────
#  2. Tri par insertion  — O(n²)  lent
# ──────────────────────────────────────────────────────────────────────────────

def tri_insertion(liste: list, compteur: list,
                  stop_flag=None, pause_flag=None) -> None:
    for i in range(1, len(liste)):
        if _check(stop_flag, pause_flag):
            return
        cle = liste[i]
        j = i - 1
        while j >= 0 and liste[j] > cle:
            compteur[0] += 1
            liste[j + 1] = liste[j]
            j -= 1
        liste[j + 1] = cle
        compteur[0] += 1


# ──────────────────────────────────────────────────────────────────────────────
#  3. Tri à bulles  — O(n²)  lent
# ──────────────────────────────────────────────────────────────────────────────

def bubble_sort(liste: list, compteur: list,
                stop_flag=None, pause_flag=None) -> None:
    n = len(liste)
    for i in range(n):
        if _check(stop_flag, pause_flag):
            return
        echange = False
        for j in range(0, n - i - 1):
            compteur[0] += 1
            if liste[j] > liste[j + 1]:
                liste[j], liste[j + 1] = liste[j + 1], liste[j]
                echange = True
        if not echange:
            break


# ──────────────────────────────────────────────────────────────────────────────
#  4. Tri fusion  — O(n log n)  rapide
# ──────────────────────────────────────────────────────────────────────────────

def tri_fusion(liste: list, compteur: list, **_) -> list:
    if len(liste) <= 1:
        return liste

    milieu = len(liste) // 2
    gauche = tri_fusion(liste[:milieu], compteur)
    droite = tri_fusion(liste[milieu:], compteur)

    return _fusionner(gauche, droite, compteur)


def _fusionner(gauche, droite, compteur):
    resultat = []
    i = j = 0
    while i < len(gauche) and j < len(droite):
        compteur[0] += 1
        if gauche[i] <= droite[j]:
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1
    resultat.extend(gauche[i:])
    resultat.extend(droite[j:])
    return resultat


# ──────────────────────────────────────────────────────────────────────────────
#  5. Tri rapide (quicksort)  — O(n log n) moy.  rapide
# ──────────────────────────────────────────────────────────────────────────────

def quick_sort(liste: list, compteur: list, **_) -> list:
    if len(liste) <= 1:
        return liste

    pivot  = liste[len(liste) // 2]
    gauche = []
    milieu = []
    droite = []

    for x in liste:
        compteur[0] += 1
        if x < pivot:
            gauche.append(x)
        elif x == pivot:
            milieu.append(x)
        else:
            droite.append(x)

    return quick_sort(gauche, compteur) + milieu + quick_sort(droite, compteur)


# ──────────────────────────────────────────────────────────────────────────────
#  6. Tri par tas (heapsort)  — O(n log n)  rapide
# ──────────────────────────────────────────────────────────────────────────────

def tri_tas(liste: list, compteur: list, **_) -> None:
    n = len(liste)

    # Construction du tas max
    for i in range(n // 2 - 1, -1, -1):
        _entasser(liste, n, i, compteur)

    # Extraction des éléments un par un
    for i in range(n - 1, 0, -1):
        liste[0], liste[i] = liste[i], liste[0]
        compteur[0] += 1
        _entasser(liste, i, 0, compteur)


def _entasser(liste, n, i, compteur):
    plus_grand = i
    gauche     = 2 * i + 1
    droite     = 2 * i + 2

    if gauche < n:
        compteur[0] += 1
        if liste[gauche] > liste[plus_grand]:
            plus_grand = gauche

    if droite < n:
        compteur[0] += 1
        if liste[droite] > liste[plus_grand]:
            plus_grand = droite

    if plus_grand != i:
        liste[i], liste[plus_grand] = liste[plus_grand], liste[i]
        _entasser(liste, n, plus_grand, compteur)


# ──────────────────────────────────────────────────────────────────────────────
#  7. Tri à peigne (comb sort)  — O(n log n) moy.  rapide
# ──────────────────────────────────────────────────────────────────────────────

def tri_peigne(liste: list, compteur: list, **_) -> None:
    n      = len(liste)
    ecart  = n
    facteur = 1.3
    trie   = False

    while not trie:
        ecart = int(ecart / facteur)
        if ecart <= 1:
            ecart = 1
            trie  = True

        for i in range(n - ecart):
            compteur[0] += 1
            if liste[i] > liste[i + ecart]:
                liste[i], liste[i + ecart] = liste[i + ecart], liste[i]
                trie = False