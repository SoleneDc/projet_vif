# 08/02/2018 Solène Duchamp - Charles Jacquet

# Programme 1: programme de l'énoncé
# 1 : if X <= 0  
#     then 2 : X := -X  
#     else 3 : X = 1 - X;  
# 4 : if X = 1  
#     then 5 : X := 1  
#     else 6 : X = X + 1  

from model_graph import graphe_controle

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
    prog1_graph = graphe_controle(7)
    
    # ajout des aretes de décision
    prog1_graph.add_arete_decision(1, 2, d_inf_0)
    prog1_graph.add_arete_decision(1, 3, d_sup_0)
    prog1_graph.add_arete_decision(4, 5, d_x_egal_un)
    prog1_graph.add_arete_decision(4, 6, d_x_not_un)

    # ajout des aretes d'affectation
    prog1_graph.add_arete_affectation(2, 4, a_oppose)
    prog1_graph.add_arete_affectation(3, 4, a_un_moins_x)
    prog1_graph.add_arete_affectation(5, 7, a_un)
    prog1_graph.add_arete_affectation(6, 7, a_x_plus_1)

    jeu_test = [{'x': -1, 'y': 3}, {'x': 2, 'y': 1}, {'x': -30, 'y': -2}]
    print("Jeu de test : ", jeu_test)
    print("Toutes les affectations : ", prog1_graph.toutes_affectations(jeu_test))
    print("Toutes les décisions : ", prog1_graph.toutes_decisions(jeu_test))
    print("Tous les 2-chemins : ",prog1_graph.tous_k_chemins(jeu_test, 2))
    print("Tous les 4-chemins : ",prog1_graph.tous_k_chemins(jeu_test, 4))

    print(prog1_graph.parcours_tous_chemins())