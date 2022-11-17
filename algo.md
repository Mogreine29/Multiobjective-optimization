### Pseudo-code de l'algorithme

PLS = Pareto Local Search
```
while P != 0 do
    for all x in P do
        for all x' in N(x) do
            if y(x') not dominated by y(x) and y(x)!=y(x') then
                if Update(A, x') then
                    Pa <- Pa U {x'}
                endif
            endif
        endfor
    endfor
P<-Pa
Pa<-0
```
with A = initial solutions to explore  
Pa = interesting solutions to explore further  
N(x) denotes neighboorhood of x and Update() the Pareto Archive (A)  

### Codage de la solution
-> On veut trouver quel job assigner à quelle machine
Codage de la solution  = vecteur de taille n = nombre de jobs à assigner

Exemple:
[0,3,2,1,4,5,6,7]
- machine 0 = job 0
- machine 1 = job 3
- machine 2 = job 2
- machine 3 = job 1
- machine 4 = job 4
- machine 5 = job 5
- machine 6 = job 6
- machine 7 = job 7

### Initialisation du problème
Pour initialiser le problème, on fait des combinaisons linéaires des fonctions objectifs 
et on résoud cela comme un problème mono-objectif avec le solveur linear_sum_assignment de scipy (on veut résoudre un problème d'assignation).
Cela nous permet de connaître les valeurs extrêmes du front de Pareto. 

### Exploration
Plusieurs façons d'explorer possibles. Soit on explore tous les voisins. Soit on peut explorer les voisins jusqu'au moment où une solution n'est pas dominée et on repart de cette solution. On pourrait aussi prendre en compte le calcul de l'hypervolume dans l'exploration: est-ce que cette solution va augmenter la taille de mon hypervolume ? 

