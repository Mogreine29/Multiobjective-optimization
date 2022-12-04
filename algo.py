from utils import get_matrix, init_combinaisons, read_data, score, hypervolume, generate_solution, voisinage, check_domine_diff, update, write, init_random
import time 

# Paramètres importantes à remplir au début
file_name = "Data/input/LAP15-4obj.txt"
nombre_objectif = 4
ref = (50,120,150,200) # point de référence pour le calcul de l'hypervolume
taille_init_random = 0
taille_coef_combi = 50

# Lecture des données
d = read_data(file_name, nombre_objectif)
mx = get_matrix(file_name, nombre_objectif)

start = time.monotonic()
# Initialisation des solutions
sols = init_combinaisons(mx, nombre_objectif, taille_coef_combi)
solutions = generate_solution(sols, d, nombre_objectif)
print('random')
print(len(solutions))
all_solutions = init_random(solutions, taille_init_random, d, nombre_objectif)
end = time.monotonic()
print(f"Temps d'initialisation : {end - start}")


# Algo
def algo(solutions, d, nombre_objectif):
    # stock de l'archive qu'on met à jour
    archive = solutions.copy()
    for sol in solutions.values():
        voisins = voisinage(sol)
        # parcourir les voisins et chercher une meilleure valeur
        for voisin in voisins:
            score_newsol = score(voisin, d, nombre_objectif)
            # si pas dominé et différent
            if check_domine_diff(score_newsol, archive.keys()):
                new_sol = {score_newsol: voisin}
                archive = update(archive, new_sol)
    return archive

# Benchmark temps algo
start2 = time.monotonic()
sols = algo(all_solutions, d, nombre_objectif)
end2 = time.monotonic()
print(f"Solutions trouvées en {end2-start2} s")

print(len(sols))


# Calcul de l'hypervolume
# h = hypervolume(ref, (sols.keys()))
# print(f"Hypervolume = {h} %")


# Stocker la solution obtenue
write(sols, file_name)