# Comparaison des solutions obtenus avec celles des autres étudiants / celles du prof

from utils import hypervolume

file_name = "Data/data3SOL.txt"

with open(file_name, 'r') as fin:
    scores = [tuple(map(int,line.strip().split())) for line in fin]

ref = (100,100,100,100)
h = hypervolume(ref, scores)
print(h)