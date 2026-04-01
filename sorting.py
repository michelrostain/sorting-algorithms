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

#jehvqfhjqbsdvkjdqbksjdq