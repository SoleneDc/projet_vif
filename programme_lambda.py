# 08/02/2018 Solène Duchamp - Charles Jacquet

# Programme 1: programme de l'énoncé
# 1 : if X <= 0
#     then 2 : X := -X
#     else 3 : X = 1 - X;
# 4 : if X = 1
#     then 5 : X := 1
#     else 6 : X = X + 1

from model_graph import graphe_controle


if __name__ == '__main__':
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




    jeu_test = [{'x': 2}, {'x': -2}, {'x': -1}]
    # print("Jeu de test : ", jeu_test)
    # print("Toutes les affectations : ", prog1_graph.toutes_affectations(jeu_test))
    # print("Toutes les décisions : ", prog1_graph.toutes_affectations(jeu_test))
    # print("Toutes les i-boucles : ", prog1_graph.toutes_boucles(jeu_test))
    # print("Toutes les définitions : ", prog1_graph.toutes_les_def(jeu_test))
    print("Toutes les utilisations : ", prog1_graph.toutes_les_utilisations(jeu_test))
    # print(prog1_graph.chemins_partiels(1, 7))
    #print(prog1_graph.tous_les_DU_chemins())
    # print(prog1_graph.parcourir_boolean({'x': 2}))
    #print(prog1_graph.parcourir({'x': 2}))
    #print(prog1_graph.toutes_les_conditions([{'x': 2}, {'x': -2}]))

    #print(prog1_graph.travel_with_path({'x': 1}))
    # print(prog1_graph.travel_with_path({'x': -3}))

    # print("Toutes les définitions : ", prog1_graph.toutes_les_def(jeu_test))
    #print("Toutes les utilisations :", prog1_graph.toutes_les_utilisations(jeu_test))
    #chemins = prog1_graph.parcours_tous_chemins_string()
    #print(prog1_graph.nodes_between(2, 7, chemins))
    #print(prog1_graph.loops())
