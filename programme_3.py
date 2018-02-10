# 08/02/2018 Solène Duchamp - Charles Jacquet

# Programme 1: programme de l'énoncé


from programme_1 import *


# Commandes (affectation)
def x_moins_y(dict_etat):
    dict_etat['x'] = dict_etat['x'] - dict_etat['y']
    return dict_etat
def x_plus_y(dict_etat):
    dict_etat['x'] = dict_etat['x'] + dict_etat['y']
    return dict_etat


# Booléen - décision
def x_inf_0(dict_etat):
    if dict_etat['x'] <= 0:
        return True
    return False

def x_sup_0(dict_etat):
    if dict_etat['x'] > 0:
        return True
    return False

def y_inf_0(dict_etat):
    if dict_etat['y'] <= 0:
        return True
    return False

def y_sup_0(dict_etat):
    if dict_etat['y'] > 0:
        return True
    return False

if __name__ == '__main__':
    model = graphe_controle(5)
    # ajout des aretes de décision
    model.add_arete_decision(1, 2, x_inf_0)
    model.add_arete_decision(2, 3, y_inf_0)
    model.add_arete_decision(2, 4, y_sup_0)
    model.add_arete_decision(1, 5, x_sup_0)

    # ajout des aretes d'affectation
    model.add_arete_affectation(3, 1, x_moins_y)
    model.add_arete_affectation(4, 1, x_plus_y)

    jeu_test =[{'x': -1, 'y': 3}, {'x': 2, 'y': 1}, {'x': -4, 'y': -2}]
    # print(model.show_graph())
    print("Jeu de test : ", jeu_test)
    print("Toutes les affectations : ", model.toutes_affectations(jeu_test))
    print("Toutes les décisions : ", model.toutes_affectations(jeu_test))
    print("Toutes les 5-boucles : ", model.toutes_boucles(jeu_test, i=5))
    print("Toutes les 15-boucles : ", model.toutes_boucles(jeu_test, i=15))
