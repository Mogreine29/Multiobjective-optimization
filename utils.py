from collections import defaultdict
import numpy as np
from scipy.optimize import linear_sum_assignment
from itertools import product
from pymoo.indicators.hv import HV 

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
    # TODO si rapport coef est le même alors pas besoin car on connait déjà -> exemple (2,2) similaire à (1,1) : trier ici directement au lieu de trier les solutions après
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
    # on veut les solutions uniques
    solutions = np.unique(sols, axis=0)
    return solutions

# permet de lier à chaque solution trouvée son score au format {score:solution}
def generate_solution(solutions, d, nobj):
    # stocker les vecteurs de solutions sous la forme d'un dico {(f1,f2,..): [vecteur]}
    score_dict = dict()
    for sol in solutions:
        score_dict[tuple(score(sol, d, nobj))] = sol 
    return score_dict

# fonction qui calcule le score d'une solution
# entrée = vecteur sol, d = dictionnaire qui stocke les données et nbre objectifs
def score(sol, d, nobj):
    obj = np.zeros(nobj)
    for i,v in enumerate(sol):
        obj+=d[(i,v)]      
    return obj


# calcul du hypervolume
def hypervolume(ref_point,A):
    '''
    ref_point = [x,y,z]
    A = np.array(np.array())
    '''
    ref_point = np.array(ref_point)
    A = np.array(A)
    print(A)
    ind = HV(ref_point=ref_point)
    return ind(A)



# voisinage d'une solution
# pour le cas 1 on a déjà 6 solutions optimales à l'initialisation en optimisant des 
# combinaisons linéaires des objectifs
# -> si on intensifie autour des solutions optimales peut être pas toujours intéressant
# il faut diversifier
def voisinage(x):
    pass


# fonction qui cherche dominance x domine y 
# -> il faut une f obj > et les autres >=
def domine(x, y):
    x = np.array(x)
    y = np.array(y)
    return (x<=y).all() and (x<y).any()

# TODO: pas optimal de mettre à jour comme ça en terme de complexité algorithmique-> réfléchir à une méthode plus intelligente
# x = archive, y = nouvelle solution
# si y est dominé par x alors pas d'update, si y pas dominé alors y dans archive et supprimer de l'archive les solutions dominées par y
def update(x,y):
    # si y dominé par une des solutions de x alors on ne met pas à jour
    for sol in x:
        if domine(sol, y):
            return x 
    # si pas alors on garde seulemlent les solutions non dominées
    good = list()
    for sol in x:
        if not domine(y, sol):
            good.append(sol)
    good.append(y) 
    return good

