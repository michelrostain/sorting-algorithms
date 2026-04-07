# Mesure du temps d'exécution et de la mémoire (tracemalloc).

# La fonction `mesurer` est compatible avec :
#   - les algos rapides  (stop_flag=None, pause_flag=None)
#   - les algos lents    (reçoivent stop_flag + pause_flag en kwargs)

import time
import tracemalloc
import threading


def mesurer(
    fn,
    liste: list,
    compteur: list,
    retourne: bool = False,
    stop_flag:  threading.Event | None = None,
    pause_flag: threading.Event | None = None,
) -> dict:
    """
    Exécute `fn` sur `liste` en mesurant :
      - le temps écoulé (time.perf_counter)
      - la mémoire courante et le pic (tracemalloc)
      - le nombre d'opérations (via `compteur[0]`)

    Parameters
    ----------
    fn          : callable  – fonction de tri
    liste       : list      – liste à trier (modifiée en place OU retournée)
    compteur    : list[int] – compteur[0] incrémenté par l'algo
    retourne    : bool      – True si fn retourne la liste triée
    stop_flag   : Event     – positionné pour interrompre les algos lents
    pause_flag  : Event     – effacé pour mettre en pause les algos lents

    Returns
    -------
    dict avec clés : taille, operations, temps_sec, memoire_ko, pic_ko, interrompu
    """
    tracemalloc.start()
    debut = time.perf_counter()
    interrompu = False

    try:
        kwargs: dict = {}
        if stop_flag  is not None:
            kwargs["stop_flag"]  = stop_flag
        if pause_flag is not None:
            kwargs["pause_flag"] = pause_flag

        resultat = fn(liste, compteur, **kwargs)

        if retourne and resultat is not None:
            liste[:] = resultat

        # Vérification : l'algo a-t-il été interrompu ?
        if stop_flag is not None and stop_flag.is_set():
            interrompu = True

    except KeyboardInterrupt:
        interrompu = True

    fin = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "taille"     : len(liste),
        "operations" : compteur[0],
        "temps_sec"  : fin - debut,
        "memoire_ko" : current / 1024,
        "pic_ko"     : peak    / 1024,
        "interrompu" : interrompu,
    }