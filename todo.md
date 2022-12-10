### TODO

Mieux initialier les solutions -> inutile d'avoir coef 2/2 et 1/1 
Améliorer complexité condition domine + différent
Update?
J'ai oublié une condition dans l'algo -> si update alors il faut explorer les voisins du point ajouté!!

Pure numpy + numba for speed

attention que borne sur init -> param qui influence bcp le temps car génère la première archive

prendre en compte hypervolume dans exploration et garde meilleures solutions ?? 

voisinage: mélanger voisins de 1 + permutations n! et tout explorer

init random + petit coef 0.1

coder une vraie local search avec un vrai voisinage et pas juste un voisinage random héhéhé


mixer les solutions obtenues avec 1 2 3 et garder meilleure

paralléliser la recherche random au début pour aller plus vite -> chaque coeur cherche de façon random dans son domaine -> séparer le domaine en x coeurs et lancer chaque coeur sur son domaine

bug pour lap 8-3 avec random 0 et coef 1 on a 51 solutions alors qu'avec 2 on en a que 50 or quand coef = 2 on inclut les mêmes valeurs que quand coef = 1 et même des valeurs en plus 





