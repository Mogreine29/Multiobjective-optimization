from collections import defaultdict
import numpy as np
from scipy.optimize import linear_sum_assignment
from itertools import product

# lit les données et return un dictionnaire (machine, job): [f obj1, f obj2]
def read_data(file_name, nobj):
    with open(file_name, 'r') as fin:
        taille = int(fin.readline())
        # dico (machine, job): (f obj1, f obj2, ..)
        d = defaultdict(list)
        for _ in range(nobj):
            m = 0
            for j in range(taille):
                line = list(map(int,fin.readline().strip().split()))
                for i,j in enumerate(line):
                    d[(m,i)].append(j)
                m += 1           
    return d


# données sous forme matricielle pour init des solutions en faisant des combinaisons linéaires des objectifs
def get_matrix(file_name, nobj):
    with open(file_name, 'r') as fin:
        matrices = []
        taille = int(fin.readline())
        for _ in range(nobj):
            mx = np.zeros(shape=(taille, taille))
            for j in range(taille):
                line = np.array(list(map(int, fin.readline().strip().split())))
                mx[j] = line 
            matrices.append(mx)
    return matrices


# objectif = trouver la solution exacte pour chaque objectif séparément pour trouver les valeurs extrêmes
# size = coef
# nobjectif
def init_solution(mx, nobj, max_coef):
    # génération de coefficients pour les combinaisons linéaires des fonctions objectifs
    x = [int(i) for i in range(max_coef+1)]
    coef = []
    for iter in product(x,repeat = nobj):
        if sum(iter)>0:
            coef.append(iter)
    
    # multiplication des fonctions objectifs par ces coefficients et calcul du vecteur optimale pour chaque combinaison linéaire
    sols = []
    for c in coef:
        m = np.zeros(shape=(mx[0].shape[0], mx[0].shape[1]))
        for i,z in enumerate(c):
            m+=z*mx[i]
        row_ind, col_ind = linear_sum_assignment(m)
        sols.append(col_ind) 
    return sols 


# fonction qui calcule le score d'une solution
# entrée = vecteur sol, d = dictionnaire qui stocke les données et nbre objectifs
def score(sol, d, nobj):
    obj = np.zeros(shape=(1,nobj))
    for i,v in enumerate(sol):
        obj+=d[(i,v)]      
    return obj


