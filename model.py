# 08/02/2018 Solène Duchamp - Charles Jacquet

# Module contenant une classe qui crée le graphe associé au programme 
# et possède les méthodes nécessaire pour les vérifications

import networkx as nx
import matplotlib.pyplot as plt
from pyscipopt import Model


class graphe_controle():
    """ Classe representant un graphe de controle pour un n'importe quel programme.
    Les etiquettes des aretes sont ajoutees par la suite avec les methodes :add_arete_XXX:\n
    :param nodes_nb: Nombres de noeuds du graphe 
    """

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

    def parcours_k_chemins(self, k=7):
        buffer = []
        L = []
        T = {1:[]}
        i = 1
        
        def visit(noeud, L, T, i, buffer):
            voisins = list(self.G.adj[noeud])
            L += zip([noeud]*len(voisins), voisins)
            if len(voisins) > 1 :
                buffer += list(T[i])
            elif len(voisins) == 0 and L[len(L)-1][0] != 1:
                print("add_buff")
                i += 1
                T[i] = list(buffer)
            elif len(voisins) == 0 and L[len(L)-1][0] == 1:
                print("incr_i, no_buff")
                i += 1
                buffer = []
                
        visit(1, L, T, i, buffer)
        while L :
            nv = L.pop(len(L)-1)
            
            if T:
                T[i].append(nv)
            else:
                T[i] = [nv]
                
            print(L, T, i, nv, buffer)
            visit(nv[1], L, T, i, buffer)
        return T


    # Fonctions génériques
    def skip(self, dict_etat):
        return dict_etat
    def ret_true(self, dict_etat):
        return True

    def toutes_affectations(self, jeu_test=[-1,5,10]):
        """ Fonction vérifiant le critère "toutes les affectations" \n
        :param jeu_test: jeu de test à vérifier \n 
        :return: true or false 
        """
        arete_visite = []
        for elt in jeu_test:
            dict_etat = {'x' : elt}
            arete_visite += self.parcourir(dict_etat)[0]

        return set(self.arete_affectation).issubset(set(arete_visite))
    
    def toutes_decisions(self, jeu_test=[-1,5,10]):
        """ Fonction vérifiant le critère "toutes les décisions" \n
        :param jeu_test: jeu de test à vérifier \n 
        :return: true or false 
        """
        arete_visite = []
        for elt in jeu_test:
            dict_etat = {'x' : elt}
            arete_visite += self.parcourir(dict_etat)[0]

        return set(self.arete_decision).issubset(set(arete_visite))
    
    def tous_k_chemins(self, jeu_test=[-1,5,10], k=2):
        """ Fonction vérifiant le critère "toutes les k-chemins" \n
        :param jeu_test: jeu de test à vérifier \n       
        :param k: longueur du chemin \n 
        :return: true or false 
        """ 
        arete_visite = []
        for elt in jeu_test:
            dict_etat = {'x' : elt}
            arete_visite += self.parcourir(dict_etat)[0]

        return list(nx.dfs_edges(self.G, 1))

        # intuition: faire un DFS à partir de 1

    
    def show_graph(self):
        """ Pour afficher le graphe dans une nouvelle fenêtre """
        nx.draw(self.G,with_labels=True)
        plt.show()


    def testing_generation(self):
        pass

