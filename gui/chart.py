# gui/chart.py
"""
Gère l'affichage du graphique matplotlib dans la fenêtre Tkinter.
- afficher_barres_tkinter() : intègre le graphe dans un widget Tkinter
- afficher_barres_standalone() : version fenêtre séparée (debug)
"""

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from gui.colors import COULEURS_BARRES, COULEUR_ALGO, BG_PANEL, BG_CARD, TXT_MAIN, TXT_MUTED


def creer_canvas(parent):
    """
    Crée et retourne un canvas matplotlib vide intégré dans `parent` (widget Tkinter).
    Retourne (fig, ax, canvas).
    """
    fig = Figure(figsize=(8, 3), facecolor=BG_PANEL)
    ax  = fig.add_subplot(111)
    _styler_ax(ax, fig)

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.get_tk_widget().configure(bg=BG_PANEL, highlightthickness=0)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    return fig, ax, canvas


def dessiner_barres(ax, canvas, liste, nom_algo, interrompu=False):
    """
    Dessine les barres de la liste sur l'ax donné et rafraîchit le canvas.

    Paramètres
    ----------
    ax          : Axes matplotlib
    canvas      : FigureCanvasTkAgg
    liste       : list[int|float]  — valeurs à afficher
    nom_algo    : str              — nom de l'algorithme (pour titre + couleur)
    interrompu  : bool             — True si Ctrl+C a été déclenché
    """
    ax.clear()
    _styler_ax(ax, canvas.figure)

    n      = len(liste)
    couleur_base = COULEUR_ALGO.get(nom_algo, "#3498DB")

    # Dégradé de couleurs sur les barres
    couleurs = [COULEURS_BARRES[i % len(COULEURS_BARRES)] for i in range(n)]

    barres = ax.bar(range(n), liste, color=couleurs, width=0.85, zorder=2)

    # Valeurs sur les barres si liste courte (≤ 30 éléments)
    if n <= 30:
        for i, (barre, valeur) in enumerate(zip(barres, liste)):
            ax.text(
                i, valeur + max(liste) * 0.01,
                str(valeur),
                ha="center", va="bottom",
                color=TXT_MAIN, fontsize=8, fontweight="bold",
            )

    # Titre
    statut = "  ⚠ Interrompu" if interrompu else ""
    ax.set_title(
        f"{nom_algo}{statut}",
        color=couleur_base if not interrompu else "#ffca28",
        fontsize=11, fontweight="bold", pad=8,
    )

    canvas.draw()


def _styler_ax(ax, fig):
    """Applique le thème sombre à un axe."""
    ax.set_facecolor(BG_CARD)
    ax.tick_params(colors=TXT_MUTED, labelsize=8)
    ax.set_xlabel("")
    ax.set_ylabel("")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2a3a5c")
    ax.grid(axis="y", color="#2a3a5c", linewidth=0.5, zorder=0)
    fig.tight_layout(pad=1.5)