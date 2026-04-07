# Les Papyrus de Héron — Algorithmes de Tri

> *"Dans la Grande Bibliothèque d'Alexandrie, Héron devait remettre de l'ordre dans ses papyrus... et nous avons décidé de l'aider."*

## Contexte du projet

Projet pédagogique réalisé dans le cadre du cours d'algorithmique à La Plateforme.
L'objectif est d'implémenter, comparer et visualiser 7 algorithmes de tri classiques,
avec une interface graphique complète (tkinter + matplotlib).

---

## Structure du projet

```
projet_tris/
├── main.py                  # Point d'entrée
├── gui/
│   ├── interface.py         # Interface tkinter principale
│   ├── chart.py             # Graphique matplotlib intégré
│   └── colors.py            # Palette de couleurs dark theme
├── tris/
│   └── sorting.py           # 7 algorithmes de tri
├── utils/
│   ├── generator.py         # Générateur de listes aléatoires
│   ├── mesur_time.py        # Mesure temps (perf_counter) + mémoire (tracemalloc)
│   └── stats_manager.py     # Sauvegarde des stats dans stats.json
└── README.md
```

---

## Algorithmes implémentés

| # | Algorithme       | Complexité moyenne | Complexité pire cas | En place | Stable |
|---|------------------|--------------------|---------------------|----------|--------|
| 1 | Tri par sélection | O(n²)             | O(n²)               | ✅       | ❌     |
| 2 | Tri par insertion | O(n²)             | O(n²)               | ✅       | ✅     |
| 3 | Tri à bulles      | O(n²)             | O(n²)               | ✅       | ✅     |
| 4 | Tri fusion        | O(n log n)        | O(n log n)          | ❌       | ✅     |
| 5 | Tri rapide        | O(n log n)        | O(n²)               | ❌*      | ❌     |
| 6 | Tri par tas       | O(n log n)        | O(n log n)          | ✅       | ❌     |
| 7 | Tri à peigne      | O(n log n)        | O(n²)               | ✅       | ❌     |

\* Notre implémentation de quicksort crée des sous-listes (variante fonctionnelle).

---

## Fonctionnalités de l'interface

- **Génération** d'une liste de N nombres réels aléatoires (100 à 100 000 éléments)
- **Sélection** de l'algorithme via menu déroulant
- **Lancement** du tri dans un thread séparé (UI non bloquée)
- **Pause / Reprise** pour les algorithmes lents
- **Interruption** (Ctrl+C) pour les algorithmes lents → affiche un avertissement
- **Statistiques** : temps d'exécution, mémoire courante et pic (tracemalloc), opérations
- **Graphique** : histogramme des 100 premières valeurs triées (matplotlib)
- **Historique** : sauvegarde automatique dans `stats.json`

---

## Mesures de performance (listes de 10 000 éléments)

| Algorithme        | Temps moyen | Opérations approx. |
|-------------------|-------------|---------------------|
| Tri par sélection | ~8–12 s     | ~50 000 000         |
| Tri par insertion | ~5–9 s      | ~25 000 000         |
| Tri à bulles      | ~15–25 s    | ~50 000 000         |
| Tri fusion        | ~0.05 s     | ~130 000            |
| Tri rapide        | ~0.03 s     | ~120 000            |
| Tri par tas       | ~0.04 s     | ~260 000            |
| Tri à peigne      | ~0.04 s     | ~140 000            |

---

## Conclusion

Les algorithmes en O(n²) sont clairement inadaptés à de grandes collections :
au-delà de 5 000 éléments, ils deviennent impraticables sans interruption anticipée.
Les algorithmes en O(n log n) (fusion, rapide, tas, peigne) restent efficaces
même pour 100 000 éléments.

Le **tri rapide** est généralement le plus performant en pratique grâce à
sa localité de cache, même si sa complexité pire-cas est O(n²).
Le **tri fusion** garantit O(n log n) dans tous les cas mais consomme plus de mémoire.

---

## Lancement

```bash
python main.py
```

Dépendances : `tkinter` (stdlib), `matplotlib`, `numpy`

```bash
pip install matplotlib numpy
```

Algos Michel

4. Tri fusion
Le tri à fusion de N éléments décompose un liste en plusieurs sous liste de taille N. le premier tris rassemble les éléments N deux par deux, puis sont rangés l'un par rapport à  l'autre dans l'ordre. Ensuite les sous liste ainsi composées d'éléments triés sont comparées les unes avec les autres, en commençant par leur élément de tête. Le chiffrele plus petit est ajouté à la nouvelle liste, le chiffre le plus grand reste dans sa sous liste pour être comparé au reste, jusqu'à ce qu'il tombe sur un chiffre plus grand.

Statistiques avec une liste de 10000 éléments random créée dans python : 
Algorithme  : Tri par fusion
Opérations  : 120,354
Temps       : 0.203198 secondes
Mémoire     : 1.16 Ko (actuelle)
Mémoire     : 166.09 Ko (pic)


5. Tri rapide
Le tri rapide détermnine un élément pivot (pris aléatoirement ou via une position médiane dans la liste)



6. Tri par tas


7. Tri à peigne


Algos Yasmine

