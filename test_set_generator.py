# Solveur pour trouver des valeurs pour tester les critères "toutes les affectations" et "toutes les décisions"

# Toutes les affectations veut dire qu'on explore toutes les arêtes portant des affectations
# Dans le programme 1, cela correspond aux arêtes 2-4, 2-3, 5-7, 6-7

# Toutes les décisions veut dire qu'on explore toutes les arêtes portant des décisions
# Dans le programme 1, cela correspond aux arêtes 1-2, 1-3, 4-5, 4-6

# Pour ces deux critères, si on veut les valider, et s'il existe des valuations de départ qui le permettent,
# il faut au minimum passer par une combinaison des chemins couvrant toutes les arêtes:
# Soit:
    # chemin 2 = 1-2-4-6-7
    # chemin 3 = 1-3-4-5-7 -> impossible 
# Soit:
    # chemin 1 = 1-2-4-5-7
    # chemin 4 = 1-3-4-6-7

from constraint import *

def get_test_set(path):
    problem = Problem()
    # Afin d'exprimer la temporalité, nous avons créé plusieurs variables numérotées par variable de base (x)
    problem.addVariables(["x", "x1", "x2"], range(-10, 10 + 1))
    problem.addVariables(["a"], [1])


    if path == 1:
        #chemin 1-2-4-5-7
        problem.addConstraint(lambda x : x <= 0, "x")
        problem.addConstraint(lambda x, x1: x1 == -x, ("x", "x1"))
        problem.addConstraint(lambda x1, a: x1 == a , ("x1", "a"))
        problem.addConstraint(lambda x2, a: x2 == a , ("x2", "a"))
        # print(problem.getSolutions()[0]['x'])

    elif path == 2:
        #chemin 1-2-4-6-7
        problem.addConstraint(lambda x : x <= 0, "x")
        problem.addConstraint(lambda x, x1: x1 == -x, ("x", "x1"))
        problem.addConstraint(lambda x1, a: x1 != a, ("x1", "a"))
        problem.addConstraint(lambda x2, x1: x2 == x1 + 1, ("x2", "x1"))

    elif path == 3:
        #chemin 1-3-4-5-7 -> impossible 
        problem.addConstraint(lambda x : x > 0, "x")
        problem.addConstraint(lambda x, x1: x1 == 1-x, ("x", "x1"))
        problem.addConstraint(lambda x1, a: x1 == a , ("x1", "a"))
        problem.addConstraint(lambda x2, a: x2 == a , ("x2", "a"))

    elif path == 4:
        #chemin 1-3-4-6-7
        problem.addConstraint(lambda x : x > 0, "x")
        problem.addConstraint(lambda x, x1: x1 == 1-x, ("x", "x1"))
        problem.addConstraint(lambda x1, a: x1 != a, ("x1", "a"))
        problem.addConstraint(lambda x2, x1: x2 == x1 + 1, ("x2", "x1"))

    solution = [s['x'] for s in problem.getSolutions()]

    if solution:
        return solution
    else: 
        return "Impossible de trouver une valeur convenable"

if __name__ == "__main__":
    min_pairs = [(2,3),(1,4)]
    test_set = {}
    for i in range(1,5,1):
        print("chemin", i, " - valeurs possibles :", get_test_set(i))
        if isinstance(get_test_set(i), list):
            test_set[i] = {'x':get_test_set(i)[0]}
    for pair in min_pairs:
        if pair[0] in test_set and pair[1] in test_set:
            mint_test_set = [ test_set[pair[0]], test_set[pair[1]] ] 
            print('Plus petit test set :', mint_test_set)
            