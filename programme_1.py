# 08/02/2018 Solène Duchamp - Charles Jacquet

from model_graph import graphe_controle


def presentation_1():
    print("\n\n---------------------------------------------")
    print("Lancement de la vérification du programme 1")
    print("---------------------------------------------")
    print(" 1 : if X <= 0\n \
    then 2 : X := -X\n \
    else 3 : X = 1 - X\n \
4 : if X = 1\n \
    then 5 : X := 1\n \
    else 6 : X = X + 1")
    print("---------------------------------------------\n")


def test_programme_1(jeu_test = [{'x': -9}, {'x': -1}, {'x': 1}]):
    prog1_graph = graphe_controle(7)

    #ajout des variables
    prog1_graph.add_variables(['x'])

    # ajout des aretes de décision
    prog1_graph.add_arete_decision(1, 2, lambda dic: dic['x'] <= 0)
    prog1_graph.add_arete_decision(1, 3, lambda dic: dic['x'] > 0)
    prog1_graph.add_arete_decision(4, 5, lambda dic: dic['x'] == 1)
    prog1_graph.add_arete_decision(4, 6, lambda dic: dic['x'] != 1)

    # ajout des aretes d'affectation
    prog1_graph.add_arete_affectation(2, 4, lambda dic: dic.update({'x': -dic['x']}))
    prog1_graph.add_arete_affectation(3, 4, lambda dic: dic.update({'x': 1 - dic['x']}))
    prog1_graph.add_arete_affectation(5, 7, lambda dic: dic.update({'x': 1}))
    prog1_graph.add_arete_affectation(6, 7, lambda dic: dic.update({'x': dic['x']+1}))


    # Tests sur les critères

    print("Jeu de test : ", jeu_test)
    print("Toutes les affectations : ", prog1_graph.toutes_affectations(jeu_test))
    print("Toutes les décisions : ", prog1_graph.toutes_decisions(jeu_test))
    print("Toutes les 2-chemins : ", prog1_graph.tous_k_chemins(jeu_test, k=2))
    print("Toutes les 4-chemins : ", prog1_graph.tous_k_chemins(jeu_test, k=4))
    print("Toutes les i-boucles : ", prog1_graph.toutes_boucles(jeu_test))
    print("Toutes les définitions : ", prog1_graph.toutes_les_def(jeu_test))
    print("Toutes les utilisations : ", prog1_graph.toutes_les_utilisations(jeu_test))
    print("Tous les DU-chemins : ", prog1_graph.tous_les_DU_chemins(jeu_test))
    print("Toutes les conditions : ", prog1_graph.toutes_les_conditions(jeu_test))



if __name__ == '__main__':
    test_programme_1()