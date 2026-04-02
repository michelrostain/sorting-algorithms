import random
import tracemalloc
import time
import psutil
import os

# Import de toutes les fonctions de tri
from sorting import (
    tri_selection,
    tri_insertion,
    bubble_sort,
    quick_sort,
    tri_fusion,
    tri_tas,
    tri_peigne
)

liste_origine = [random.randint(1, 10000) for _ in range(10000)]

def mesurer(nom_algo, fonction, liste, retourne_liste=False):
    processus = psutil.Process(os.getpid())
    compteur = [0]
    copie = liste.copy()
    
    tracemalloc.start()
    processus.cpu_percent(interval=None)
    debut = time.perf_counter()
    
    if retourne_liste:
        copie[:] = fonction(copie, compteur)
    else:
        fonction(copie, compteur)
    
    fin = time.perf_counter()
    cpu_apres = processus.cpu_percent(interval=0.1)
    memoire_actuelle, memoire_pic = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"\n{'='*40}")
    print(f"Algorithme  : {nom_algo}")
    print(f"Opérations  : {compteur[0]:,}")
    print(f"Temps       : {fin - debut:.6f} secondes")
    print(f"Mémoire     : {memoire_actuelle / 1024:.2f} Ko (actuelle)")
    print(f"Mémoire     : {memoire_pic / 1024:.2f} Ko (pic)")
    print(f"CPU         : {cpu_apres:.1f} %")

# Lancement
mesurer("Tri par sélection", tri_selection, liste_origine)
mesurer("Tri par insertion", tri_insertion, liste_origine)
mesurer("Bubble sort",       bubble_sort,   liste_origine)
mesurer("Tri par fusion",    tri_fusion,    liste_origine, retourne_liste=True)
mesurer("Tri rapide",        quick_sort,    liste_origine, retourne_liste=True)
mesurer("Tri par tas",       tri_tas,       liste_origine)
mesurer("Tri à peigne",      tri_peigne,    liste_origine)