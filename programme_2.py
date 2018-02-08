from programme_1 import *



if __name__ == '__main__':
    model = graphe_controle(3)

    # ajout des aretes de décision
    model.add_arete_decision(1, 2, d_inf_0)
    model.add_arete_decision(1, 3, d_sup_0)

    # ajout des aretes d'affectation
    model.add_arete_affectation(2, 1, a_x_plus_1)

    jeu_test = [-3, 2]
    print("Jeu de test : ", jeu_test)
    print("Toutes les affectations : ", model.toutes_affectations(jeu_test))
    print("Toutes les décisions : ", model.toutes_affectations(jeu_test))
    print("Toutes les i-boucles : ", model.toutes_boucles(jeu_test))
