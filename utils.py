from collections import defaultdict
import numpy as np
from scipy.optimize import linear_sum_assignment

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


# objectif = trouver la solution exacte pour chaque objectif séparément pour trouver les valeurs extrêmes
def init_solution(file_name, nobj):
    with open(file_name, 'r') as fin:
        sols = []
        taille = int(fin.readline())
        for _ in range(nobj):
            mx = np.zeros(shape=(taille, taille))
            for j in range(taille):
                line = np.array(list(map(int, fin.readline().strip().split())))
                mx[j] = line 
            
            row_ind, col_ind = linear_sum_assignment(mx)
            sols.append(col_ind)
    return sols

sols = init_solution("Data/LAP-8-2objSOL.txt",2)
print(sols)