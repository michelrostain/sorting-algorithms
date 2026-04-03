Algos Michel

### Tri par sélection

#### Description

On parcourt le tableau de gauche à droite.  
Pour chaque position i :

On cherche l’indice du plus petit élément dans la partie i à n-1.
On échange cet élément minimum avec l’élément situé à l’indice i.

En première passe, on place le plus petit élément au début de la liste.  
En deuxième passe, on place le deuxième plus petit en deuxième position, et ainsi de suite.

#### Complexité

Temps : \(O(n^2)\) pour un tableau de taille \(n\) (deux boucles imbriquées).
Mémoire : \(O(1)\), car le tri se fait en place (uniquement des échanges dans le tableau).

#### Idée simple

Toujours choisir **le plus petit élément restant** et le placer à sa **prochaine position** dans l’ordre croissant.

#### Stats   
Algorithme  : Tri par sélection
Opérations  : 49,995,000
Temps       : 38.408551 secondes
Mémoire     : 0.61 Ko (actuelle)
Mémoire     : 41.66 Ko (pic)
CPU         : 0.0 %   


### Tri à bulles

#### Description

Le tri à bulles parcourt plusieurs fois le tableau en comparant des **éléments voisins** :

Si deux éléments consécutifs sont dans le mauvais ordre (par exemple a[i] > a[i+1] pour un tri croissant), on les **échange**.
À la fin d’un passage complet, le **plus grand élément** est « remonté » à la fin du tableau.
On recommence en s’arrêtant de plus en plus tôt, car la fin du tableau est déjà triée.

#### Complexité

Temps : \(O(n^2)\) pour un tableau de taille \(n\) (deux boucles imbriquées).
Mémoire : \(O(1)\), car le tri se fait en place (uniquement des échanges dans le tableau).

#### Idée simple

On compare sans cesse les **paires voisines** et on échange quand c’est mal ordonné, ce qui fait remonter petit à petit les plus grands éléments vers la fin, comme des bulles qui montent à la surface.

#### Stats   
Algorithme  : Bubble sort
Opérations  : 99,430,056
Temps       : 139.452754 secondes
Mémoire     : 0.12 Ko (actuelle)
Mémoire     : 41.33 Ko (pic)
CPU         : 0.0 %


### Tri par insertion

#### Description

Le tri par insertion construit progressivement une partie **triée** au début du tableau :

On considère que le premier élément est déjà trié.
Pour chaque nouvel élément, on le **compare** aux éléments de gauche.
Tant que les éléments de gauche sont plus grands, on les **décale vers la droite**.
On insère ensuite l’élément à sa **bonne place** dans la partie triée.

#### Complexité

Temps : \(O(n^2)\) dans le pire cas (tableau en ordre décroissant) et le cas moyen.
Meilleur cas (tableau déjà trié) : \(O(n)\), car chaque élément est inséré directement.
Mémoire : \(O(1)\), car le tri se fait en place.

#### Idée simple

C’est comme trier des **cartes dans la main** :  
on prend une nouvelle carte, on décale celles qui sont plus grandes, puis on insère la carte au bon endroit dans le paquet déjà rangé.

#### Stats   
Algorithme  : Tri par insertion
Opérations  : 24,919,413
Temps       : 33.736267 secondes
Mémoire     : 0.12 Ko (actuelle)
Mémoire     : 41.33 Ko (pic)
CPU         : 0.0 %


### Tri fusion   
Le tri à fusion de N éléments décompose un liste en plusieurs sous liste de taille N. le premier tri rassemble les éléments N deux par deux, puis sont rangés l'un par rapport à  l'autre dans l'ordre. Ensuite les sous liste ainsi composées d'éléments triés sont comparées les unes avec les autres, en commençant par leur élément de tête. Le chiffrele plus petit est ajouté à la nouvelle liste, le chiffre le plus grand reste dans sa sous liste pour être comparé au reste, jusqu'à ce qu'il tombe sur un chiffre plus grand.

Statistiques avec une liste de 10000 éléments random créée dans python : 
Algorithme  : Tri par fusion
Opérations  : 120,354
Temps       : 0.203198 secondes
Mémoire     : 1.16 Ko (actuelle)
Mémoire     : 166.09 Ko (pic)


### Tri rapide
Le tri rapide détermnine un élément pivot (pris aléatoirement ou via une position médiane dans la liste), cet élément deviens le centre de la distribution des autres éléments et détermine deux sous-listes : les éléments plus petits vont à gauche, les éléments plus grands vont à droite. Le même procédé est appliqué de manière récursive aux sous listes ainsi créées, jusqu'à la fin du classement (d'abord la gauche, puis la droite). La condition d'arrêt est lorsque les sous liste ne font qu'un seul éléments.
Complexité : O(N log N), pire des cas O(N²)
Travaille avec un nombre de sous liste important, consomme de la mémoire (O log N), car les appels récursif consomment de la mémoire.

Statistiques avec une liste de 10000 éléments random créée dans python : 
Algorithme  : Tri rapide   
Opérations  : 159,995   
Temps       : 0.102782 secondes   
Mémoire     : 3.95 Ko (actuelle)   
Mémoire     : 512.88 Ko (pic)   
CPU         : 0.0 %   


### Tri par tas
Le tri par tas crée une arborescence. Le chiffre le plus grand est toujours remonté à la racine pour ensuite être inclu dans la nouvelle liste de tri. Les chiffres les plus petits sont descendus au branches les plus basses, pour être remontés en dernier et ainsi respecter l'ordre de tri dans la nouvelle liste.
Le tri se fait dans l'arboresence.
Complexité : N log N. Pas de pire cas.

Statistiques avec une liste de 10000 éléments random créée dans python : 
Algorithme  : Tri par tas
Opérations  : 166,599
Temps       : 0.190436 secondes
Mémoire     : 0.39 Ko (actuelle)
Mémoire     : 41.61 Ko (pic)
CPU         : 0.0 %


### Tri à peigne
C'est une forme de tri à bulles amélioré : au lieu de trier les éléments côte à côte, il tri les éléments éloigné d'un facteur 1,3 pour atteindre 1 à  la fin. A chaque passe, l'écart se réduit jusqu'à être un écart de tri à bulle à la fin. Si le facteur est bien choisi, il n'y a que très peu de passe de tri à bulle à faire (idéal : 1 passe).
La complexité varie en fonction du facteur de réduction approprié.Celui est optimal à 1,3 et est appliqué à "n" pour une liste de "n" éléments.
Le pire cas (une liste trié inversée) mène la complexité à O(N²), mais pas autant q'un tri à bulle car les coeff permet de limiter le nombre d'opération.

Statistiques avec une liste de 10000 éléments random créée dans python : 
Algorithme  : Tri à peigne
Opérations  : 326,734
Temps       : 0.523580 secondes
Mémoire     : 0.12 Ko (actuelle)
Mémoire     : 41.33 Ko (pic)
CPU         : 0.0 %



**Conclusion :** 
les pires cas pour les algorithme de tri  par bulles, insertion et peignes sont des listes déjà triées dans l'ordre inversée.
Pour un tri rapide, c'est une liste déjà triée avec un pivot en dernier élément. La complexité passe alors de O(N log N) à 0(N²).
Pour un tri par sélection, il n'y a pas de pire cas, c'est toujours O(N²)
Pour un tri à, fusion et un tri par tas, la complexité ne bouge pas quel que soit le cas, soit O(N log N).
