import random

liste = []
for k in range (101):
    liste.append(random.randint(0, 100000))


def tri_insertion(L):
    N = len(L)
    for n in range (1, N):
        cle = L[n]
        j = n-1
        while j>=0 and L[j] > cle:
            L [j+1] = L[j]
            j = j-1
        L[j+1] = cle

def bubble_sort(arr):
    n = len(arr)
    switch = True
    while switch == True :
        switch = False
        for i in range(0, n-1):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                switch = True

def quick_sort(arr):
    # COndition d'arrêt : une liste vide ou un élément déjà trié
    if len(arr) <=1:
        return arr
    # On choisi notre pivot, par exemple l'élément du milieu
    pivot = arr[len(arr) // 2]

    # On divide la liste la liste en 3 groupes :
    gauche = [x for x in arr if x< pivot]
    milieu = [x for x in arr if x == pivot]
    droite = [x for x in arr if x> pivot]

    # On appelle la fonction sur les sous listes (régner)
    return quick_sort(gauche) + milieu + quick_sort(droite)


def tri_selection(l):
    # Mémorisation taille de la liste
    n = len(l)
    # On parcourt la iste de gauche à droite, i gère le nombre de passe sur le reste à trier de la liste 
    for i in range(n-1):
        i_mini = i
        # Comme la dernière passe a rangé un chiffre (placé à l'index i), on repart de i+1. j gère le nombre d'opérations effectué par passe. Une passe i génère un nombre d'opérations qui est le nombre de chiffre restant àtrier dans chaque passe.
        for j in range (i+1, n):
            if  l[j]<l[i_mini]:
                i_mini = j
        l[i], l[i_mini] = l[i_mini], l[i]


def tri_fusion(l):
    # Condition d'arrêt
    if len(l) <= 1:
        return l
    
    # Décomposition
    milieu = len(l) // 2
    gauche = tri_fusion(l[:milieu])
    droite = tri_fusion(l[milieu:])
    
    # Fusion directement ici
    resultat = []
    i = 0
    j = 0
    
    while i < len(gauche) and j < len(droite):
        if gauche[i] <= droite[j]:
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1
    
    resultat.extend(gauche[i:])
    resultat.extend(droite[j:])
    
    return resultat


def tri_tas(l):
    n = len(l)
    
    # Fonction de tamisage imbriquée
    def tamiser(taille, i):
        plus_grand = i
        gauche = 2 * i + 1
        droite = 2 * i + 2
        
        if gauche < taille and l[gauche] > l[plus_grand]:
            plus_grand = gauche
        
        if droite < taille and l[droite] > l[plus_grand]:
            plus_grand = droite
        
        if plus_grand != i:
            l[i], l[plus_grand] = l[plus_grand], l[i]
            tamiser(taille, plus_grand)
    
    # PHASE 1 : Construction du tas max
    for i in range(n // 2 - 1, -1, -1):
        tamiser(n, i)
    
    # PHASE 2 : Extraction des éléments un par un
    for i in range(n - 1, 0, -1):
        l[0], l[i] = l[i], l[0]
        tamiser(i, 0)    

def tri_peigne(l):
    n = len(l)
    
    # L'écart initial est la taille de la liste
    ecart = n
    
    # Facteur de réduction classique : 1.3 (empiriquement optimal)
    facteur = 1.3
    
    tri_termine = False
    
    while not tri_termine:
        
        # On réduit l'écart à chaque passe
        ecart = int(ecart / facteur)
        
        # L'écart minimum est 1 — on devient alors un tri à bulles classique
        if ecart <= 1:
            ecart = 1
            tri_termine = True  # On suppose que c'est la dernière passe
        
        # On parcourt la liste en comparant les éléments séparés par l'écart
        for i in range(0, n - ecart):
            if l[i] > l[i + ecart]:
                l[i], l[i + ecart] = l[i + ecart], l[i]
                tri_termine = False  # Un échange a eu lieu, on continue