from utils import clean_solutions, get_matrix, init_solution, read_data, score

file_name = "Data/LAP-8-2objSOL.txt"
nombre_objectif = 2

# Lecture des données
d = read_data(file_name, nombre_objectif)
mx = get_matrix(file_name, nombre_objectif)


# Initialisation des solutions
sol = clean_solutions(init_solution(mx, 2, 10))

for s in sol:
    print(score(s,d,2))



