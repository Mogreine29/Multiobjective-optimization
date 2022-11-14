from utils import get_matrix, init_solution, read_data, score

file_name = "Data/LAP-8-2objSOL.txt"
nombre_objectif = 2

# Lecture des données
d = read_data(file_name, nombre_objectif)
mx = get_matrix(file_name, nombre_objectif)

sl = init_solution(mx, 2, 1)

for c in sl:
    print(score(c,d,2))


