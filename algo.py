from utils import get_matrix, init_solution, read_data, score, hypervolume, generate_solution, voisinage, check_domine_diff, update
import time 

file_name = "Data/LAP-8-4objSOL.txt"
nombre_objectif = 4

# Lecture des données
d = read_data(file_name, nombre_objectif)
mx = get_matrix(file_name, nombre_objectif)


# Initialisation des solutions
init = init_solution(mx, nombre_objectif, 10)
solutions = generate_solution(init, d, nombre_objectif)

def algo(solutions, d, nombre_objectif):
    # stock de l'archive qu'on met à jour
    archive = solutions.copy()
    for sol in solutions.values():
        voisins = voisinage(sol)
        # parcourir les voisins et chercher une meilleure valeur, si mieux alors stop exploration des voisins
        for voisin in voisins:
            score_newsol = score(voisin, d, nombre_objectif)
            # si pas dominé et différent
            if check_domine_diff(score_newsol, archive.keys()):
                new_sol = {score_newsol: voisin}
                archive = update(archive, new_sol)
                break
    return archive

start = time.monotonic()
sols = algo(solutions, d, nombre_objectif)
end = time.monotonic()
print(f"Solutions trouvées en {end-start} s")

print(len(sols))
for sol in sols.keys():
    print(sol)



# Calcul de l'hypervolume
ref = (100,100,100,100)
h = hypervolume(ref, (sols.keys()))
print(h)



