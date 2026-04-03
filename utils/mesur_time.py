import tracemalloc
import time
import signal
import threading
from typing import Callable


def mesurer(
    fn:         Callable,
    liste:      list,
    compteur:   list,
    retourne:   bool             = False,
    stop_flag:  threading.Event  = None,
    pause_flag: threading.Event  = None,
) -> dict:

    taille     = len(liste)
    interrompu = False

    #Ctrl+C clavier : on lève le stop_flag au lieu de crasher 
    original_handler = signal.getsignal(signal.SIGINT)

    def _handler_ctrlc(sig, frame):
        if stop_flag:
            stop_flag.set()
        if pause_flag:
            pause_flag.set()   # débloque si en pause

    signal.signal(signal.SIGINT, _handler_ctrlc)

    #Lancement mesure
    tracemalloc.start()
    debut = time.perf_counter()

    try:
        if retourne:
            liste[:] = fn(liste, compteur)
        else:
            fn(liste, compteur)

    except KeyboardInterrupt:
        # Sécurité si le signal n'est pas capturé à temp
        interrompu = True
        if stop_flag:
            stop_flag.set()

    finally:
        # Restaure le handler original dans tous les cas
        signal.signal(signal.SIGINT, original_handler)

    fin = time.perf_counter()
    mem_actuelle, mem_pic = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Vérifie aussi le flag (bouton UI ou signal)
    if stop_flag and stop_flag.is_set():
        interrompu = True

    return {
        "operations" : compteur[0],
        "temps_sec"  : fin - debut,
        "memoire_ko" : mem_actuelle / 1024,
        "pic_ko"     : mem_pic / 1024,
        "taille"     : taille,
        "interrompu" : interrompu,
    }