from utils import get_matrix, init_combinaisons, read_data, score, generate_solution, voisinage, check_domine_diff, update, write, init_random
import time
import numpy as np

# Paramètres importantes à remplir au début
file_name = "Data/input/LAP30-4obj.txt"
nombre_objectif = 4
ref = (50, 120, 150, 200)  # point de référence pour le calcul de l'hypervolume
taille_init_random = 50 
taille_random = 100
taille_coef_combi = 1

# Lecture des données
d = read_data(file_name, nombre_objectif)
mx = get_matrix(file_name, nombre_objectif)

start = time.monotonic()
# Initialisation des solutions
sols = init_combinaisons(mx, nombre_objectif, taille_coef_combi)
solutions = generate_solution(sols, d, nombre_objectif)
print(len(solutions))
print('random')
all_solutions = init_random(solutions, taille_init_random, d, nombre_objectif)
print('after random', len(all_solutions))
end = time.monotonic()
print(f"Temps d'initialisation : {end - start}")


# Algo
def algo(solutions, d, nombre_objectif):
    try:
        # stock de l'archive qu'on met à jour
        archive = solutions.copy()
        # solutions à explorer
        sols = list(solutions.values()).copy()
        x = sols[0]
        for _ in range(taille_random):
            sols.append(np.random.permutation(x))
            for sol in sols:
                voisins = voisinage(sol)
                # parcourir les voisins et chercher une meilleure valeur
                for voisin in voisins:
                    # si voisin déjà dans sols alors on passe
                    if np.any(np.all(voisin==sols, axis = 1)):
                        continue
                    score_newsol = score(voisin, d, nombre_objectif)
                    # si solution déjà présente alors on ne met pas à jour l'archive mais on veut quand même explorer les voisins de cette solution
                    if score_newsol in archive.keys():
                        sols.append(voisin)
                        continue
                    # si pas dominé et différent
                    if check_domine_diff(score_newsol, archive.keys()):
                        new_sol = {score_newsol: voisin}
                        archive = update(archive, new_sol)
                        sols.append(voisin)
                print(len(archive.keys()))
    except KeyboardInterrupt:
        write(archive,"30.txt" )
    return archive



# Benchmark temps algo
start2 = time.monotonic()
for _ in range(10):
    all_solutions = algo(all_solutions, d, nombre_objectif)
end2 = time.monotonic()
print(f"Solutions trouvées en {end2-start2} s")

print(len(sols))

# Calcul de l'hypervolume
# h = hypervolume(ref, (sols.keys()))
# print(f"Hypervolume = {h} %")

# Stocker la solution obtenue
write(sols, "AAAA.txt")