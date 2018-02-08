# Devoir Maison d'IVF

Programme analysé:

1 : if X <= 0  
    then 2 : X := -X  
    else 3 : X = 1 - X;  
4 : if X = 1  
    then 5 : X := 1  
    else 6 : X = X + 1  

# Structure:   

├── main.py -> module où l'on définit les commandes du programme à analyser et où on les assigne aux arêtes   
├── model.py -> classe représentant un graphe de contrôle pour un programme donné  
└── set_generator.py -> module contenant un solveur par contraintes, permettant la génération de test sets

# Environment 
Python 3.6

### Installed libraries:  
* pyscipopt : wrapper python pour le programme SCIP (Solving Constraint Integers Programs)   
* networkx : librairie de création de graphes

