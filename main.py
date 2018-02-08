# 08/02/2018 Solène Duchamp - Charles Jacquet

# Module pour créer les fonctions d'affectation et de décision à utiliser dans le graphe

from model import graphe_controle

# Commandes (affectation)

def a_oppose(dict_etat):
    dict_etat['x'] = - dict_etat['x']
    return dict_etat

def a_un_moins_x(dict_etat):
    dict_etat['x'] = 1 - dict_etat['x']
    return dict_etat

def a_un(dict_etat):
    dict_etat['x'] = 1
    return dict_etat

def a_x_plus_1(dict_etat):
    dict_etat['x'] = dict_etat['x'] + 1
    return dict_etat

# Booléen - décision
def d_inf_0(dict_etat):
    if dict_etat['x'] <= 0:
        return True
    return False

def d_sup_0(dict_etat):
    if dict_etat['x'] > 0:
        return True
    return False

def d_x_egal_un(dict_etat):
    if dict_etat['x'] == 1:
        return True
    return False

def d_x_not_un(dict_etat):
    if dict_etat['x'] != 1:
        return True
    return False

if __name__ == '__main__':
    model = graphe_controle(7)
    
    # ajout des aretes de décision
    model.add_arete_decision(1, 2, d_inf_0)
    model.add_arete_decision(1, 3, d_sup_0)
    model.add_arete_decision(4, 5, d_x_egal_un)
    model.add_arete_decision(4, 6, d_x_not_un)

    # ajout des aretes d'affectation
    model.add_arete_affectation(2, 4, a_oppose)
    model.add_arete_affectation(3, 4, a_un_moins_x)
    model.add_arete_affectation(5, 7, a_un)
    model.add_arete_affectation(6, 7, a_x_plus_1)

    jeu_test = [-1, 2]
    print("Jeu de test : ", jeu_test)
    print("Toutes les affectations : ",model.toutes_affectations(jeu_test))
    print("Toutes les décisions : ",model.toutes_affectations(jeu_test))
    print("Toutes les k-chemins : ",model.parcours_k_chemins(jeu_test))