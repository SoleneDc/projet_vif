#Création d'un graphe

import networkx as nx
import matplotlib.pyplot as plt
from pyscipopt import Model


class graph_model():

    def __init__(self, nodes_nb = 1):
        self.G = nx.DiGraph()
        self.G.add_nodes_from(list(range(1,nodes_nb+1)))
        self.arete_decision = []
        self.arete_affectation = []

    def add_arete_decision(self, noeud_sortant, noeud_recevant, fonction):
        self.G.add_edges_from([(noeud_sortant, noeud_recevant,{'bexp': fonction , 'cexp': self.skip})])
        self.arete_decision.append((noeud_sortant, noeud_recevant))
    
    def add_arete_affectation(self, noeud_sortant, noeud_recevant, fonction):
        self.G.add_edges_from([(noeud_sortant, noeud_recevant,{'bexp': self.ret_true, 'cexp': fonction})])
        self.arete_affectation.append((noeud_sortant, noeud_recevant))

    def parcourir(self, dict_etat):
        """ Fonction permettant de parcourir le graphe, en fonction d'une valuation initiale \n
        :param dict_etat: valuation initiale \n 
        :return: les arêtes parcourues, l'état final """
        liste_noeud_parcouru=[1]
        aretes = []
        i = 1  # ou on est sur le graphe
        while i < 7:
            self.G.nodes[i]['etat'] = dict_etat
            noeuds_voisins = list(self.G.adj[i])
            for node in noeuds_voisins:

                if self.G.edges[i, node]['bexp'](dict_etat):
                    self.G.edges[i, node]['cexp'](dict_etat)
                    i = node
                    liste_noeud_parcouru.append(node)
                    break
        for i in range(len(liste_noeud_parcouru)-1):
            aretes.append((liste_noeud_parcouru[i], liste_noeud_parcouru[i+1]))
        return aretes, dict_etat

    # Fonctions génériques
    def skip(self, dict_etat):
        return dict_etat
    def ret_true(self, dict_etat):
        return True

    def toutes_affectation(self, jeu_test=[-1,5,10]):
        """ Fonction vérifiant le critère "toutes les affectations" \n
        :param jeu_test: jeu de test à vérifier \n 
        :return: true or false 
        """
        arete_visite = []
        for elt in jeu_test:
            dict_etat = {'x' : elt}
            arete_visite += self.parcourir(dict_etat)[0]

        return set(self.arete_affectation).issubset(set(arete_visite))
    
    def toutes_decision(self, jeu_test=[-1,5,10]):
        """ Fonction vérifiant le critère "toutes les décisions" \n
        :param jeu_test: jeu de test à vérifier \n 
        :return: true or false 
        """
        arete_visite = []
        for elt in jeu_test:
            dict_etat = {'x' : elt}
            arete_visite += self.parcourir(dict_etat)[0]

        return set(self.arete_decision).issubset(set(arete_visite))
    
    def show_graph(self):
        """ Pour afficher le graphe dans une nouvelle fenêtre """
        nx.draw(self.G,with_labels=True)
        plt.show()

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



def testing_generation():
    pass

if __name__ == '__main__':
    model = graph_model(7)
    
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

    jeu_test = [-1,- 2]
    print("Jeu de test : ", jeu_test)
    print("Toutes les affectations : ",model.toutes_affectation(jeu_test))
    print("Toutes les décisions : ",model.toutes_affectation(jeu_test))