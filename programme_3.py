# 08/02/2018 Solène Duchamp - Charles Jacquet

from model_graph import graphe_controle

def presentation_3():
    print("\n\n---------------------------------------------")
    print("Lancement de la vérification du programme 3")
    print("---------------------------------------------")
    print(" 1 : while X <= 0 :\n \
    then 2 :\n \
           if Y <= 0 :\n \
           then 3 : X := X - Y\n \
           else 4 : X := X + Y\n \
5 : then : return X, Y")
    print("---------------------------------------------\n")


def test_programme_3(jeu_test=[{'x': 4, 'y': -2}, {'x': -2, 'y': 4}, {'x': -2, 'y': 2}, {'x': -2, 'y': -2}, {'x': -2, 'y': -4}]):
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

    # Tests sur les critères
    print("Jeu de test : ", jeu_test)
    print("Toutes les affectations : ", model.toutes_affectations(jeu_test))
    print("Toutes les décisions : ", model.toutes_decisions(jeu_test))
    print("Toutes les 2-chemins : ", model.tous_k_chemins(jeu_test, k=2))
    print("Toutes les 4-chemins : ", model.tous_k_chemins(jeu_test, k=4))
    print("Toutes les 1-boucle : ", model.toutes_boucles(jeu_test, i=1))
    print("Toutes les 2-boucles : ", model.toutes_boucles(jeu_test, i=2))
    print("Toutes les définitions : ", model.toutes_les_def(jeu_test))
    print("Toutes les utilisations : ", model.toutes_les_utilisations(jeu_test))
    print("Tous les DU-chemins : ", model.tous_les_DU_chemins(jeu_test))
    print("Toutes les conditions : ", model.toutes_les_conditions(jeu_test))


if __name__ == '__main__':
    test_programme_3()