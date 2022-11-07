from collections import defaultdict

def read_data(file_name, nobj):
    with open(file_name, 'r') as fin:
        taille = int(fin.readline())
        # dico clé = worker i et valeur = liste avec les temps pour chaque tâche
        d = defaultdict(list)
        for line in range(nobj):
            for j in range(taille):
                d[j+1].append(list(fin.readline().strip().split()))
    return d 

