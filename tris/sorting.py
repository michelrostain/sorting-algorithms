# gui/interface.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk
import threading

from gui.colors import BG_DARK, BG_PANEL, BG_CARD, ACCENT, TXT_MAIN, TXT_MUTED
from gui.chart import creer_canvas, dessiner_barres
from utils.generator import generer_liste
from utils.mesur_time import mesurer
from utils.stats_manager import sauvegarder_stats
from tris.sorting import (
    tri_selection, tri_insertion, bubble_sort,
    quick_sort, tri_fusion, tri_tas, tri_peigne,
)

ALGOS = {
    "Tri par sélection": {"fn": tri_selection, "retourne": False, "lent": True },
    "Tri par insertion": {"fn": tri_insertion, "retourne": False, "lent": True },
    "Tri à bulles"     : {"fn": bubble_sort,   "retourne": False, "lent": True },
    "Tri fusion"       : {"fn": tri_fusion,    "retourne": True,  "lent": False},
    "Tri rapide"       : {"fn": quick_sort,    "retourne": True,  "lent": False},
    "Tri par tas"      : {"fn": tri_tas,       "retourne": False, "lent": False},
    "Tri à peigne"     : {"fn": tri_peigne,    "retourne": False, "lent": False},
}


class AppTri(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Les Papyrus de Héron  —  Algorithmes de Tri")
        self.geometry("1020x730")
        self.minsize(860, 620)
        self.configure(bg=BG_DARK)

        self._liste      = []
        self._stop_flag  = threading.Event()
        self._pause_flag = threading.Event()
        self._pause_flag.set()
        self._thread     = None

        self._construire_ui()
        self._generer_liste()

    # ══════════════════════════════════════════════════════════════════════════
    #  UI
    # ══════════════════════════════════════════════════════════════════════════

    def _construire_ui(self):
        # En-tête
        header = tk.Frame(self, bg=BG_PANEL, pady=10)
        header.pack(fill="x")
        tk.Label(header, text="🏛  Les Papyrus de Héron",
                 font=("Georgia", 18, "bold"), fg=ACCENT, bg=BG_PANEL).pack(side="left", padx=18)
        self._lbl_statut = tk.Label(header, text="En attente...",
                                     font=("Consolas", 9), fg=TXT_MUTED, bg=BG_PANEL)
        self._lbl_statut.pack(side="right", padx=18)

        # Contrôles
        ctrl = tk.Frame(self, bg=BG_CARD, pady=10, padx=14)
        ctrl.pack(fill="x", padx=14, pady=(10, 0))

        tk.Label(ctrl, text="Taille :", font=("Consolas", 10),
                 fg=TXT_MUTED, bg=BG_CARD).grid(row=0, column=0, padx=(0, 4))

        self._var_taille = tk.IntVar(value=10000)
        tk.Spinbox(ctrl, from_=100, to=100000, increment=1000,
                   textvariable=self._var_taille, width=8,
                   font=("Consolas", 10), bg=BG_DARK, fg="#4fc3f7",
                   buttonbackground=BG_PANEL, relief="flat", bd=0,
                   ).grid(row=0, column=1, padx=(0, 12))

        self._btn_gen = self._btn(ctrl, "⟳  Générer liste", "#4fc3f7", self._generer_liste)
        self._btn_gen.grid(row=0, column=2, padx=6)

        tk.Label(ctrl, text="|", fg="#2a3a5c", bg=BG_CARD,
                 font=("Consolas", 14)).grid(row=0, column=3, padx=8)

        tk.Label(ctrl, text="Algorithme :", font=("Consolas", 10),
                 fg=TXT_MUTED, bg=BG_CARD).grid(row=0, column=4, padx=(0, 4))

        self._var_algo = tk.StringVar(value="Tri rapide")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("D.TCombobox",
                         fieldbackground=BG_DARK, background=BG_DARK,
                         foreground=TXT_MAIN, bordercolor="#2a3a5c",
                         arrowcolor="#4fc3f7",
                         selectbackground=BG_DARK, selectforeground=TXT_MAIN)
        self._combo = ttk.Combobox(ctrl, textvariable=self._var_algo,
                                    values=list(ALGOS.keys()),
                                    state="readonly", style="D.TCombobox",
                                    font=("Consolas", 10), width=20)
        self._combo.grid(row=0, column=5, padx=(0, 12))
        self._combo.bind("<<ComboboxSelected>>", self._on_algo_change)

        self._btn_run = self._btn(ctrl, "▶  Lancer tri", "#69f0ae", self._lancer_tri)
        self._btn_run.grid(row=0, column=6, padx=6)

        self._btn_pause = self._btn(ctrl, "⏸  Pause", "#ffca28",
                                     self._toggle_pause, state="disabled")
        self._btn_pause.grid(row=0, column=7, padx=6)

        self._btn_stop = self._btn(ctrl, "⏹  Ctrl+C", "#ff5252",
                                    self._interrompre, state="disabled")
        self._btn_stop.grid(row=0, column=8, padx=(6, 0))

        # Badge
        self._badge = tk.Label(self, text="", font=("Consolas", 9, "bold"), bg=BG_DARK)
        self._badge.pack(anchor="w", padx=18, pady=(6, 2))
        self._on_algo_change()

        # Zone résultats
        zone = tk.Frame(self, bg=BG_DARK)
        zone.pack(fill="both", expand=True, padx=14, pady=(6, 10))

        # Bloc texte stats AU-DESSUS du graphique
        cadre_stats = tk.Frame(zone, bg=BG_PANEL, padx=16, pady=10)
        cadre_stats.pack(fill="x", pady=(0, 8))

        self._txt_stats = tk.Text(cadre_stats, height=8,
                                   bg=BG_PANEL, fg=TXT_MAIN,
                                   font=("Consolas", 11),
                                   bd=0, relief="flat", wrap="word",
                                   state="disabled")
        self._txt_stats.pack(fill="x")
        self._configurer_tags()

        # Graphique
        cadre_graph = tk.Frame(zone, bg=BG_PANEL)
        cadre_graph.pack(fill="both", expand=True)
        self._fig, self._ax, self._canvas = creer_canvas(cadre_graph)

        # Progress bar
        style.configure("Tri.Horizontal.TProgressbar",
                         troughcolor=BG_PANEL, background=ACCENT,
                         bordercolor=BG_DARK)
        self._progress = ttk.Progressbar(self, mode="indeterminate", length=500,
                                          style="Tri.Horizontal.TProgressbar")
        self._progress.pack(pady=(0, 6))

    def _configurer_tags(self):
        self._txt_stats.tag_configure("titre_ok",
            foreground="#69f0ae", font=("Consolas", 12, "bold"))
        self._txt_stats.tag_configure("titre_warn",
            foreground="#ffca28", font=("Consolas", 12, "bold"))
        self._txt_stats.tag_configure("label",
            foreground=TXT_MUTED, font=("Consolas", 11))
        self._txt_stats.tag_configure("valeur",
            foreground="#4fc3f7",  font=("Consolas", 11, "bold"))
        self._txt_stats.tag_configure("sep",
            foreground="#2a3a5c",  font=("Consolas", 11))

    # ══════════════════════════════════════════════════════════════════════════
    #  ACTIONS
    # ══════════════════════════════════════════════════════════════════════════

    def _generer_liste(self):
        n = self._var_taille.get()
        self._liste = generer_liste(n)
        self._set_statut(f"Liste de {n:,} éléments générée.")
        self._effacer_stats()

    def _lancer_tri(self):
        if self._thread and self._thread.is_alive():
            return

        algo_nom = self._var_algo.get()
        cfg      = ALGOS[algo_nom]

        self._stop_flag.clear()
        self._pause_flag.set()

        self._btn_run.config(state="disabled")
        self._btn_stop.config(state="normal" if cfg["lent"] else "disabled")
        self._btn_pause.config(state="normal" if cfg["lent"] else "disabled")
        self._progress.start(12)
        self._set_statut(f"Tri en cours : {algo_nom}…")

        self._thread = threading.Thread(
            target=self._executer_tri,
            args=(algo_nom, cfg),
            daemon=True,
        )
        self._thread.start()

    def _toggle_pause(self):
        if self._pause_flag.is_set():
            self._pause_flag.clear()
            self._btn_pause.config(text="▶  Reprendre")
            self._set_statut("⏸ Tri en pause…")
        else:
            self._pause_flag.set()
            self._btn_pause.config(text="⏸  Pause")
            self._set_statut("Tri repris…")

    def _interrompre(self):
        """Bouton UI Ctrl+C."""
        self._stop_flag.set()
        self._pause_flag.set()

    def _on_algo_change(self, *_):
        algo = self._var_algo.get()
        if ALGOS.get(algo, {}).get("lent"):
            self._badge.config(
                text="🐢  Algorithme lent  —  Ctrl+C disponible (bouton ou clavier)",
                fg="#ffca28")
        else:
            self._badge.config(text="⚡  Algorithme rapide", fg="#69f0ae")

    # ══════════════════════════════════════════════════════════════════════════
    #  EXÉCUTION (thread)
    # ══════════════════════════════════════════════════════════════════════════

    def _executer_tri(self, nom_algo, cfg):
        copie    = self._liste.copy()
        compteur = [0]
        lent     = cfg["lent"]

        stats = mesurer(
            fn         = cfg["fn"],
            liste      = copie,
            compteur   = compteur,
            retourne   = cfg["retourne"],
            # On passe stop_flag seulement aux algos lents
            stop_flag  = self._stop_flag if lent else None,
            pause_flag = self._pause_flag if lent else None,
        )

        # ── Sauvegarde dans stats.json ────────────────────────────────────────
        sauvegarder_stats(nom_algo, stats)

        self.after(0, self._afficher_resultats, nom_algo, stats, copie)

    # ══════════════════════════════════════════════════════════════════════════
    #  AFFICHAGE
    # ══════════════════════════════════════════════════════════════════════════

    def _afficher_resultats(self, nom_algo, stats, liste_triee):
        self._progress.stop()
        self._btn_run.config(state="normal")
        self._btn_stop.config(state="disabled")
        self._btn_pause.config(state="disabled")
        self._btn_pause.config(text="⏸  Pause")

        interrompu = stats.get("interrompu", False)
        n          = stats.get("taille", len(liste_triee))
        operations = stats.get("operations", 0)
        temps      = stats.get("temps_sec", 0.0)
        mem_ko     = stats.get("memoire_ko", 0.0)
        pic_ko     = stats.get("pic_ko", 0.0)

        # Texte stats
        self._txt_stats.config(state="normal")
        self._txt_stats.delete("1.0", "end")

        if interrompu:
            self._txt_stats.insert("end",
                "⚠  Attention ! : Liste non entièrement triée !\n\n", "titre_warn")
        else:
            self._txt_stats.insert("end",
                "✔  Liste triée avec succès !\n\n", "titre_ok")

        self._txt_stats.insert("end",
            f"Statistiques avec une liste de {n:,} éléments random créée dans python :\n",
            "label")
        self._txt_stats.insert("end", "─" * 58 + "\n", "sep")

        self._txt_stats.insert("end", "Algorithme  : ", "label")
        self._txt_stats.insert("end", f"{nom_algo}\n",  "valeur")

        self._txt_stats.insert("end", "Opérations  : ", "label")
        self._txt_stats.insert("end", f"{operations:,}\n", "valeur")

        self._txt_stats.insert("end", "Temps       : ", "label")
        self._txt_stats.insert("end", f"{temps:.6f}", "valeur")
        self._txt_stats.insert("end", " secondes\n", "label")

        self._txt_stats.insert("end", "Mémoire     : ", "label")
        self._txt_stats.insert("end", f"{mem_ko:.2f} Ko", "valeur")
        self._txt_stats.insert("end", "  (actuelle)\n", "label")

        self._txt_stats.insert("end", "Mémoire     : ", "label")
        self._txt_stats.insert("end", f"{pic_ko:.2f} Ko", "valeur")
        self._txt_stats.insert("end", "  (pic)\n", "label")

        self._txt_stats.config(state="disabled")

        # Graphique
        apercu = liste_triee[:100] if len(liste_triee) > 100 else liste_triee
        dessiner_barres(self._ax, self._canvas, apercu, nom_algo, interrompu)

        statut = "⚠ Interrompu" if interrompu else "✔ Terminé"
        self._set_statut(f"{statut}  —  {temps:.4f}s  —  {operations:,} opérations")

    # ══════════════════════════════════════════════════════════════════════════
    #  HELPERS
    # ══════════════════════════════════════════════════════════════════════════

    def _btn(self, parent, texte, couleur, cmd, state="normal"):
        return tk.Button(parent, text=texte,
                          font=("Consolas", 10, "bold"),
                          bg=BG_PANEL, fg=couleur,
                          activebackground=BG_DARK, activeforeground=couleur,
                          relief="flat", bd=0, padx=10, pady=5,
                          cursor="hand2", command=cmd, state=state)

    def _set_statut(self, msg):
        self._lbl_statut.config(text=msg)

    def _effacer_stats(self):
        self._txt_stats.config(state="normal")
        self._txt_stats.delete("1.0", "end")
        self._txt_stats.config(state="disabled")
        self._ax.clear()
        self._canvas.draw()


def lancer_interface():
    app = AppTri()
    app.mainloop()