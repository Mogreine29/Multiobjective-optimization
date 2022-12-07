## Pareto Local Search algorithm for solving multi-objective assignment problem

### Pseudo-code de l'algorithme

**Pareto Local Search:**

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

- with A = initial solutions to explore
- Pa = interesting solutions to explore further
- N(x) denotes neighboorhood of x and Update() the Pareto Archive (A)

### Codage de la solution

On veut trouver quel job assigner à quelle machine. Le codage de la solution est donc un vecteur de taille n (n = nombre de jobs / machines) et on assigne à la machine d'indice i le job qui se trouve à cet indice dans la liste.

Exemple de solution:
[0,3,2,1,4,5,6,7]

- machine 0 = job 0
- machine 1 = job 3
- machine 2 = job 2
- machine 3 = job 1
- machine 4 = job 4
- machine 5 = job 5
- machine 6 = job 6
- machine 7 = job 7

## Initialisation du problème

### Combibaisons linéaires

Pour initialiser le problème, on fait des combinaisons linéaires des fonctions objectifs et on résoud cela comme un problème mono-objectif avec le solveur linear_sum_assignment de scipy (on veut résoudre un problème d'assignation).
Cela nous permet de connaître les valeurs extrêmes du front de Pareto.

### Exploration random

On initialise le problème aussi avec des solutions aléatoires qu'on va explorer par la suite.

## Algorithme

### Exploration

On a simplement implémenté l'algorithme décrit ci-dessus en pseudo-code. On va explorer le domaine de recherche et quand on trouve une solution non dominée par l'archive actuelle alors on met à jour l'archive. C'est à dire qu'on va ajouter à l'archive la nouvelle solution trouvée qui n'est pas dominée et on va supprimer de l'archive les solutions qui sont dominées par la nouvelle solution qu'on vient d'ajouter.

### Voisinage

Pour obtenir le voisinage d'une solution, on va simplement faire tous les swaps de l'array possibles. On veut juste les swaps 1 à 1 pour intensifier un maximum et explorer autour des solutions déjà trouvées (on fait la diversification avec l'aléatoire lors de l'initialisation). On a donc (n\*(n-1))/2 voisins à explorer pour chaque solution.

## Comparaison des solutions obtenues

Etant donné que c'est un problème multi-objectifs, pour comparer les solutions obtenues entre 2 jeux de solutions, on va calculer combien de solutions sont communes aux 2, combien de solutions du jeu 1 sont dominées par le 2 et inversément, et on va calculer l'hypervolume. Le but est de maximiser l'hypervolume. [(Calcul hypervolume)](https://arxiv.org/abs/1510.01963)

