from programme_1 import *



if __name__ == '__main__':
    model = graphe_controle(3)

    # ajout des variables
    model.add_variables(['x'])

    # ajout des aretes de décision
    model.add_arete_decision(1, 2, lambda dic: dic['x'] <= 0)
    model.add_arete_decision(1, 3, lambda dic: dic['x'] > 0)

    # ajout des aretes d'affectation
    model.add_arete_affectation(2, 1, lambda dic: dic.update({'x': dic['x']+1}))

    print(model.def_function(2))
    print(model.ref_function(2))

    jeu_test = [{'x': -3}, {'x': 2}]
    print("Jeu de test : ", jeu_test)
    print("Toutes les affectations : ", model.toutes_affectations(jeu_test))
    print("Toutes les décisions : ", model.toutes_affectations(jeu_test))
    print("Toutes les i-boucles : ", model.toutes_boucles(jeu_test))
