#Création d'un graphe

import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_nodes_from(list(range(1,8)))


#Commandes
def skip(dict_etat):
    return dict_etat

def oppose(dict_etat):
    dict_etat['x'] = - dict_etat['x']
    return dict_etat

def un_moins_x(dict_etat):
    dict_etat['x'] = 1 - dict_etat['x']
    return dict_etat

def un(dict_etat):
    dict_etat['x'] = 1
    return dict_etat

def x_plus_1(dict_etat):
    dict_etat['x'] = dict_etat['x'] + 1
    return dict_etat

#Booléen
def inf_0(dict_etat):
    if dict_etat['x'] <= 0:
        return True
    return False

def sup_0(dict_etat):
    if dict_etat['x'] > 0:
        return True
    return False

def x_egal_un(dict_etat):
    if dict_etat['x'] == 1:
        return True
    return False

def x_not_un(dict_etat):
    if dict_etat['x'] != 1:
        return True
    return False

def ret_true(dict_etat):
    return True


G.add_edges_from([(1, 2,{'bexp': inf_0 , 'cexp': skip}),
                  (2, 4, {'bexp': ret_true, 'cexp': oppose}),
                  (1, 3,{'bexp': sup_0, 'cexp': skip}),
                  (3, 4, {'bexp': ret_true, 'cexp': un_moins_x}),
                  (4, 5, {'bexp': x_egal_un, 'cexp': skip}),
                  (4, 6,{'bexp': x_not_un, 'cexp': skip}),
                  (5, 7, {'bexp': ret_true, 'cexp': un}),
                  (6, 7,{'bexp': ret_true, 'cexp': x_plus_1})])

def parcourir(G, dict_etat):
    liste_noeud_parcouru=[1]
    i = 1  # ou on est sur le graphe
    while i < 7:
        G.nodes[i]['etat'] = dict_etat
        noeuds_voisins = list(G.adj[i])
        for node in noeuds_voisins:

            if G.edges[i, node]['bexp'](dict_etat):
                G.edges[i, node]['cexp'](dict_etat)
                i = node
                liste_noeud_parcouru.append(node)
                break

    return liste_noeud_parcouru, dict_etat



if __name__ == '__main__':
    nx.draw(G,with_labels=True)
    #plt.show()
    dict_etat = {'x': 5}
    print (parcourir(G,dict_etat))