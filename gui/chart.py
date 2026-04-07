import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from gui.colors import BG_PANEL, BG_DARK, ACCENT, TXT_MAIN, TXT_MUTED


def creer_canvas(parent):
    """
    Crée et retourne (fig, ax, canvas) intégrés dans le widget `parent`.
    """
    fig, ax = plt.subplots(figsize=(9, 3.2), dpi=96)
    fig.patch.set_facecolor(BG_PANEL)
    _styler_axes(ax)

    canvas = FigureCanvasTkAgg(fig, master=parent)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    canvas.draw()
    return fig, ax, canvas


def dessiner_barres(ax, canvas, valeurs, titre_algo: str, interrompu: bool = False):
    """
    Dessine un histogramme des `valeurs` dans `ax`.

    Parameters
    ----------
    ax          : matplotlib Axes
    canvas      : FigureCanvasTkAgg
    valeurs     : list[float]  – aperçu (100 premières valeurs max)
    titre_algo  : str          – nom de l'algorithme (affiché en titre)
    interrompu  : bool         – colorie en orange si vrai
    """
    ax.clear()
    _styler_axes(ax)

    if not valeurs:
        canvas.draw()
        return

    n      = len(valeurs)
    x      = np.arange(n)
    vmin   = min(valeurs)
    vmax   = max(valeurs) if max(valeurs) != vmin else vmin + 1

    # Palette : dégradé cyan → violet ; orange si interrompu
    if interrompu:
        couleurs = plt.cm.autumn(np.linspace(0.1, 0.6, n))
    else:
        couleurs = plt.cm.cool(np.linspace(0.0, 1.0, n))

    bars = ax.bar(x, valeurs, color=couleurs, width=0.85, zorder=3)

    # Axe et grille
    ax.set_xlim(-0.8, n - 0.2)
    ax.set_ylim(vmin - (vmax - vmin) * 0.05, vmax + (vmax - vmin) * 0.12)
    ax.set_xlabel("Index (aperçu 100 premiers)", color=TXT_MUTED, fontsize=8)
    ax.set_ylabel("Valeur", color=TXT_MUTED, fontsize=8)

    statut = "⚠ Interrompu" if interrompu else "✔ Trié"
    ax.set_title(f"{titre_algo}  —  {statut}",
                 color="#ffca28" if interrompu else "#69f0ae",
                 fontsize=10, fontweight="bold", pad=8)

    canvas.draw()


# ──────────────────────────────────────────────────────────────────────────────
#  Helpers internes
# ──────────────────────────────────────────────────────────────────────────────

def _styler_axes(ax):
    """Applique le thème sombre aux axes."""
    ax.set_facecolor(BG_DARK)
    for spine in ax.spines.values():
        spine.set_color("#2a3a5c")
    ax.tick_params(colors=TXT_MUTED, labelsize=7)
    ax.xaxis.label.set_color(TXT_MUTED)
    ax.yaxis.label.set_color(TXT_MUTED)
    ax.grid(axis="y", color="#1e3050", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)