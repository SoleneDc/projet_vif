# 08/02/2018 Solène Duchamp - Charles Jacquet

# Programme 3: programme suivant
# 1 : while X <= 0 :
#     then 2 :
#            if Y <= 0 :
#            then 3 : X := X - Y
#            else 4 : X := X + Y
# 5 : then : return X, Y


from model_graph import graphe_controle


if __name__ == '__main__':

    model = graphe_controle(5)

    # ajout des variables
    model.add_variables(['x', 'y'])

    # ajout des aretes de décision
    model.add_arete_decision(1, 2, lambda dic: dic['x'] <= 0)
    model.add_arete_decision(2, 3, lambda dic: dic['y'] <= 0)
    model.add_arete_decision(2, 4, lambda dic: dic['y'] > 0)
    model.add_arete_decision(1, 5, lambda dic: dic['x'] > 0)

    # ajout des aretes d'affectation
    model.add_arete_affectation(3, 1, lambda dic: dic.update({'x': dic['x'] - dic['y']}))
    model.add_arete_affectation(4, 1, lambda dic: dic.update({'x': dic['x'] + dic['y']}))

    #jeu_test =[{'x': -1, 'y': 3}, {'x': 2, 'y': 1}, {'x': -4, 'y': -2}]
    jeu_test = [{'x': -4, 'y': -2}]
    # print(model.show_graph())
    print("Jeu de test : ", jeu_test)
    # print("Toutes les affectations : ", model.toutes_affectations(jeu_test))
    # print("Toutes les décisions : ", model.toutes_affectations(jeu_test))
    # print("Toutes les 5-boucles : ", model.toutes_boucles(jeu_test, i=5))
    # print("Toutes les 15-boucles : ", model.toutes_boucles(jeu_test, i=15))
    # print("Toutes les définitions : ", model.toutes_les_def(jeu_test))
    print(model.parcours_tous_chemins())
    # print(model.loops())

    # print(model.def_function(2))
    # print(model.ref_function(2))
    # print(model.def_function(3))
    # print(model.ref_function(3))
    # print(model.travel_with_path({'x': -1, 'y': 3}))
    # for i in range(1, 6):
    #     print(i, model.def_function(i))
    #     print(i, model.ref_function(i))
