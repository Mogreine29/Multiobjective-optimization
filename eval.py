# Comparaison des solutions obtenus avec celles des autres étudiants / celles du prof
from utils import hypervolume, domine

def compare(filenameA, filenameB, reference):
    with open(filenameA, 'r') as f1, open(filenameB, 'r') as f2:
        data1 = [tuple(map(int,line.strip().split())) for line in f1]
        data2 = [tuple(map(int,line.strip().split())) for line in f2]
        domine1 = 0
        domine2 = 0
        for sc in data1:
            for sc2 in data2:
                # si score 1 dominé alors compteur + 1 et on passe au prochain score du jeu 1
                if domine(sc2, sc):
                    domine1+=1
                    break 
        for sc in data2:
            for sc2 in data1:
                if domine(sc2,sc):
                    domine2+=1
                    break 
    print(f"Nombre de solutions dominées dans 1 par 2 = {domine1}")
    print(f"Nombre de solutions dominées dans 2 par 1 = {domine2}")
    print(f"Nombre de solutions non dominées dans 1 par 2 = {len(data1)-domine1}")
    print(f"Nombre de solutions non dominées dans 2 par 1 = {len(data2)-domine2}")

    print('')
    
    print(f"Hypervolume 1 = {hypervolume(reference, data1)}")
    print(f"Hypervolume 2 = {hypervolume(reference, data2)}")

ref = (900,900)
compare("Data/solutions/test1.txt", "Data/solutions/test2.txt", ref)