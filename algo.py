from utils import get_matrix, init_solution, read_data, score, hypervolume, generate_solution


file_name = "Data/LAP-8-2objSOL.txt"
nombre_objectif = 2

# Lecture des données
d = read_data(file_name, nombre_objectif)
mx = get_matrix(file_name, nombre_objectif)

 
# Initialisation des solutions
init = init_solution(mx, 2, 10)
sol = generate_solution(init, d, nombre_objectif)


