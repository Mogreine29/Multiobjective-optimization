from collections import defaultdict
import numpy as np
from scipy.optimize import linear_sum_assignment
from itertools import product, permutations
from pymoo.indicators.hv import HV 

# lit les données et return un dictionnaire (machine, job): [f obj1, f obj2, f obj3]
def read_data(file_name, nobj):
    with open(file_name, 'r') as fin:
        taille = int(fin.readline())
        # dico (machine, job): (f obj1, f obj2, ..)
        d = defaultdict(list)
        # parcourir les n objectifs
        for _ in range(nobj):
            # parcourir les machines
            for machine in range(taille):
                line = list(map(int,fin.readline().strip().split()))
                # parcourir les jobs
                for job, f in enumerate(line):
                    d[(machine, job)].append(f)     
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


# initialisation des solutions en résolvant le problème de façon exacte comme si on avait un seul objecitf = combinaison linéaire des obj
# -> trouver la solution exacte pour chaque objectif séparément pour trouver les valeurs extrêmes
def init_combinaisons(mx, nobj, max_coef):
    # génération de coefficients pour les combinaisons linéaires des fonctions objectifs (+0.1 si jamais 2 possibilités pour un objectif, pour prendre le meilleur pour n obj)
    x = [int(i)+0.1 for i in range(max_coef+1)]
    coef = product(x, repeat = nobj)
    # multiplication des fonctions objectifs par ces coefficients et calcul du vecteur optimal pour chaque combinaison linéaire
    sols = []
    for c in coef:
        if sum(c)>0:
            m = np.zeros(shape=(mx[0].shape[0], mx[0].shape[1]))
            for i,z in enumerate(c):
                # créer une matrice m qui est la somme pondérée des objectifs avec une pondération différente pour chaque objectif
                m+=z*mx[i]
            row_ind, col_ind = linear_sum_assignment(m)
            sols.append(col_ind) 
    # on veut les solutions uniques
    solutions = np.unique(sols, axis=0)
    return solutions

# initialisation de solution de façon random
# on part des solutions générées avec les combinaisons et si on trouve une solution non dominée on la garde
def init_random(sols, size, d, nobj):
    x = list(sols.values())[0]
    # toutes les permutations = generator = peu couteux en mémoire
    all_permutations = permutations(x)
    i = 0
    while i < size:
        permut = np.array(next(all_permutations))
        score_permut = score(permut, d, nobj)
        # si pas dominé et différent
        if check_domine_diff(score_permut, sols.keys()):
            new_sol = {score_permut: permut}
            sols = update(sols, new_sol)
            i+=1    
    return sols

    
# permet de lier à chaque solution trouvée son score au format {score:solution}
def generate_solution(solutions, d, nobj):
    # stocker les vecteurs de solutions sous la forme d'un dico {(f1,f2,..): [vecteur]}
    score_dict = dict()
    for sol in solutions:
        # update à chaque fois en vérifiant la dominance des points
        score_dict = update(score_dict, {tuple(score(sol, d, nobj)):sol})
    return score_dict

# fonction qui calcule le score d'une solution
# entrée = vecteur sol, d = dictionnaire qui stocke les données et nbre objectifs
def score(sol, d, nobj):
    obj = np.zeros(nobj)
    for i,v in enumerate(sol):
        obj+=d[(i,v)]      
    return tuple(obj)


# calcul du hypervolume -> return un %
def hypervolume(ref_point, A):
    ref_point = np.array(ref_point)
    A = np.array(list(A))
    ind = HV(ref_point=ref_point)
    hpv = ind(A)
    volume = (np.prod(ref_point, dtype=np.float64))
    return (hpv/volume)*100


# voisinage d'une solution
def voisinage(x):
    # trouver tous les voisins de x
    voisins = []
    for i in range(len(x)):
        for j in range(i+1, len(x)):
            temp = x.copy()
            temp[i], temp[j] = temp[j], temp[i]
            voisins.append(temp)
    return voisins 

    



# fonction qui cherche dominance x domine y 
# -> il faut une f obj > et les autres >=
def domine(x, y):
    x = np.array(x)
    y = np.array(y)
    return (x<=y).all() and (x<y).any()

# check si un nouveau score domine au moins un des scores des solutions actuelles de l'archive x
def check_domine_diff(new_score, x):
    for score in x:
        if domine(score, new_score):
            return False 
    if new_score not in x:  
        return True 
    return False  

# TODO: pas optimal de mettre à jour comme ça en terme de complexité algorithmique-> réfléchir à une méthode plus intelligente
# x = archive, y = nouvelle solution
# si y est dominé par x alors pas d'update, si y pas dominé alors y dans archive et supprimer de l'archive les solutions dominées par y
def update(x,y):
    # si y dominé par une des solutions de x alors on ne met pas à jour
    # il faut regarder au niveau des clés car clés = score 
    scores = x.keys()
    new_score = tuple(y.keys())[0]
    for sol in scores:
        if domine(sol, new_score):
            return x 
    # si pas alors on garde seulemlent les solutions non dominées
    good = dict()
    for k,v in x.items():
        if not domine(new_score, k):
            good[k] = v 
    good[new_score] = list(y.values())[0] 
    return good


# écrire un fichier avec les solutions pour pouvoir comparer facilement
def write(sols, filename):
    filename = filename.split('/')[-1]
    with open(f'Data/solutions/{filename}', 'w') as fout:
        for sol in sols:
            fout.write(" ".join(str(int(i)) for i in sol) + "\n")