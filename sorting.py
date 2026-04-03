def tri_insertion(L, compteur = None):
    N = len(L)
    for n in range (1, N):
        cle = L[n]
        j = n-1
        while j>=0 and L[j] > cle:
            if compteur is not None:
                compteur[0]+=1
            L [j+1] = L[j]
            j = j-1
        L[j+1] = cle

def bubble_sort(arr, compteur=None):
    n = len(arr)
    switch = True
    while switch == True :
        switch = False
        for i in range(0, n-1):
            if compteur is not None :
                compteur[0]+=1
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                switch = True

def quick_sort(l, compteur=None):
    # COndition d'arrêt : une liste vide ou un élément déjà trié
    if len(l) <=1:
        return l
    # On choisi notre pivot, par exemple l'élément du milieu
    pivot = l[len(l) // 2]

    gauche = []
    milieu = []
    droite = []

    for x in l:
        if compteur is not None:
            compteur[0] += 1        # On compte chaque comparaison
        if x < pivot:
            gauche.append(x)
        elif x == pivot:
            milieu.append(x)
        else:
            droite.append(x)
    # On appelle la fonction sur les sous listes (régner)
    return quick_sort(gauche, compteur) + milieu + quick_sort(droite, compteur)


def tri_selection(l, compteur = None):
    # Mémorisation taille de la liste
    n = len(l)
    # On parcourt la iste de gauche à droite, i gère le nombre de passe sur le reste à trier de la liste 
    for i in range(n-1):
        i_mini = i
        # Comme la dernière passe a rangé un chiffre (placé à l'index i), on repart de i+1. j gère le nombre d'opérations effectué par passe. Une passe i génère un nombre d'opérations qui est le nombre de chiffre restant à trier dans chaque passe.
        for j in range (i+1, n):
            if compteur  is not None :
                compteur[0] += 1
            if  l[j]<l[i_mini]:
                i_mini = j
        l[i], l[i_mini] = l[i_mini], l[i]


def tri_fusion(l, compteur=None):
    # Condition d'arrêt
    if len(l) <= 1:
        return l
    
    # Décomposition
    milieu = len(l) // 2
    gauche = tri_fusion(l[:milieu], compteur)
    droite = tri_fusion(l[milieu:], compteur)
    
    # Fusion directement ici
    resultat = []
    i = 0
    j = 0
    
    while i < len(gauche) and j < len(droite):
        if compteur  is not None :
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


def tri_tas(l, compteur=None):
    n = len(l)
    
    # Fonction de tamisage imbriquée
    def tamiser(taille, i):
        plus_grand = i
        gauche = 2 * i + 1
        droite = 2 * i + 2
        
        if gauche < taille and l[gauche] > l[plus_grand]:
            plus_grand = gauche
            if compteur is not None:
                compteur[0] += 1  
        
        if droite < taille and l[droite] > l[plus_grand]:
            plus_grand = droite
            if compteur is not None:
                compteur[0] += 1  

        
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

def tri_peigne(l, compteur=None):
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
            if compteur is not None:
                compteur[0] += 1
            if l[i] > l[i + ecart]:
                l[i], l[i + ecart] = l[i + ecart], l[i]
                tri_termine = False  # Un échange a eu lieu, on continue


