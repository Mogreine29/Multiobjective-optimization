from utils import get_matrix, init_solution, read_data, score, hypervolume, generate_solution, voisinage, check_domine_diff, update, write
import time 

# Paramètres importantes à remplir au début
file_name = "Data/input/LAP15-4obj.txt"
nombre_objectif = 4
ref = (50,120,150,200) # point de référence pour le calcul de l'hypervolume


# Lecture des données
d = read_data(file_name, nombre_objectif)
mx = get_matrix(file_name, nombre_objectif)


# Initialisation des solutions
init = init_solution(mx, nombre_objectif, 10)
solutions = generate_solution(init, d, nombre_objectif)

# Algo
def algo(solutions, d, nombre_objectif):
    # stock de l'archive qu'on met à jour
    archive = solutions.copy()
    for sol in solutions.values():
        voisins = voisinage(sol, 5000000)
        # parcourir les voisins et chercher une meilleure valeur
        for voisin in voisins:
            score_newsol = score(voisin, d, nombre_objectif)
            # si pas dominé et différent
            if check_domine_diff(score_newsol, archive.keys()):
                new_sol = {score_newsol: voisin}
                archive = update(archive, new_sol)
    return archive

# Benchmark temps algo
start = time.monotonic()
sols = algo(solutions, d, nombre_objectif)
end = time.monotonic()
print(f"Solutions trouvées en {end-start} s")

print(len(sols))


# Calcul de l'hypervolume
# h = hypervolume(ref, (sols.keys()))
# print(f"Hypervolume = {h} %")


# Stocker la solution obtenue
# write(sols, file_name)