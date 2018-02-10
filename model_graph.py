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
        self.nodes_number = nodes_nb
        self.G.add_nodes_from(list(range(1, nodes_nb+1)))
        self.arete_decision = []
        self.arete_affectation = []

    def add_arete_decision(self, noeud_sortant, noeud_recevant, fonction):
        self.G.add_edges_from([(noeud_sortant, noeud_recevant,{'bexp': fonction, 'cexp': self.skip})])
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
        while i < self.nodes_number:
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

    def def_function(self, u):
        neighbors = list(self.G.adj[u])
        for node in neighbors:
            edge =

    def parcours_tous_chemins(self):
        """ Parcours tous les chemins partant du noeud racine jusqu'au noeud final """
        buffer = []
        L = [] #liste des arêtes à parcourir
        T = {1:[]} #dictionnaire contenant tous les chemins commencant en 1 et terminant au noeud final
        i = 1 #numero du chemin en cours
        
        def visit(noeud):
            nonlocal L
            nonlocal T
            nonlocal buffer
            nonlocal i
            voisins = list(self.G.adj[noeud])                   #   stocke les noeuds adjacants
            L += zip([noeud]*len(voisins), voisins)             #   donne les arêtes adjacantes
            try:
                if len(voisins) > 1:                            #   si il y a plus d'un chemin...
                    buffer += list(T[i])                        #   alors on stocke le chemin parcouru dans un buffer
                elif len(voisins) == 0 and L[len(L)-1][0] != 1: #   si on arrive au noeud final et que mon dernier élément
                                                                #   à parcourir n'est pas le noeud de départ...
                    i += 1                                      #   alors on passe au chemin suivant
                    T[i] = list(buffer)                         #   et on ajoute au début de ce chemin le buffer
                elif len(voisins) == 0 and L[len(L)-1][0] == 1:
                    i += 1
                    T[i] = []
                    buffer = []
            except:
                pass
                
        visit(1)
        while L:
            nv = L.pop(len(L)-1)
            T[i].append(nv)
            visit(nv[1])
        return T


    # Fonctions génériques
    def skip(self, dict_etat):
        return dict_etat
    def ret_true(self, dict_etat):
        return True

    def toutes_affectations(self, jeu_test=[{'x': -1, 'y': 3}, {'x': 2, 'y': 1}, {'x': -30, 'y': -2}]):
        """ Fonction vérifiant le critère "toutes les affectations" \n
        :param jeu_test: jeu de test à vérifier \n 
        :return: true or false 
        """
        arete_visite = []
        for elt in jeu_test:
            dict_etat = dict(elt)
            arete_visite += self.parcourir(dict_etat)[0]

        return set(self.arete_affectation).issubset(set(arete_visite))
    
    def toutes_decisions(self, jeu_test=[{'x': -1, 'y': 3}, {'x': 2, 'y': 1}, {'x': -30, 'y': -2}]):
        """ Fonction vérifiant le critère "toutes les décisions" \n
        :param jeu_test: jeu de test à vérifier \n 
        :return: true or false 
        """
        arete_visite = []
        for elt in jeu_test:
            dict_etat = dict(elt)
            arete_visite += self.parcourir(dict_etat)[0]

        return set(self.arete_decision).issubset(set(arete_visite))

    def toutes_boucles(self, jeu_test, i = 2):
        """ Fonction vérifiant le critère "toutes les i-boucles" \n
        :param jeu_test: jeu de test à vérifier \n
        :return: true or false
        """
        for elt in jeu_test:
            arete_visite = []
            dict_arete_visite = {}
            dict_etat = elt
            arete_visite += self.parcourir(dict_etat)[0]
            for arete in arete_visite:
                if arete in dict_arete_visite.keys():
                    dict_arete_visite[arete] += 1
                else:
                    dict_arete_visite[arete] = 1
            for k in dict_arete_visite.values():
                if k >= i:
                    return False
        return True
    
    def tous_k_chemins(self, jeu_test=[{'x' : -1},{'x' : 5}], k=2):
        """ Fonction vérifiant le critère "toutes les k-chemins" \n
        :param jeu_test: jeu de test à vérifier \n       
        :param k: longueur du chemin \n 
        :return: true or false 
        """ 
        chemins_visite = []
        for elt in jeu_test :
            dict_etat = dict(elt)
            chemin = tuple(self.parcourir(dict_etat)[0][:k])
            if chemin not in chemins_visite:
                chemins_visite.append( chemin )

        chemins_possibles = []
        for chemin in self.parcours_tous_chemins().values():
            if tuple(chemin[:k]) not in chemins_possibles:
                chemins_possibles.append(tuple(chemin[:k]))

        return set(chemins_possibles).issubset(set(chemins_visite))

    
    def show_graph(self):
        """ Pour afficher le graphe dans une nouvelle fenêtre """
        nx.draw(self.G, with_labels=True)
        plt.show()


    def testing_generation(self):
        pass

