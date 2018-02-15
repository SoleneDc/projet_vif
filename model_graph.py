# 08/02/2018 Solène Duchamp - Charles Jacquet

# Module contenant une classe qui crée le graphe associé au programme 
# et possède les méthodes nécessaire pour les vérifications

import networkx as nx
import matplotlib.pyplot as plt
from pyscipopt import Model
import inspect
import re



class graphe_controle():
    """ Classe representant un graphe de controle pour un n'importe quel programme.
    Les etiquettes des aretes sont ajoutees par la suite avec les methodes :add_arete_XXX:\n
    :param nodes_nb: Nombres de noeuds du graphe 
    """

    def __init__(self, nodes_nb=1):
        self.G = nx.DiGraph()
        self.nodes_number = nodes_nb
        self.G.add_nodes_from(list(range(1, nodes_nb+1)))
        self.arete_decision = []
        self.arete_affectation = []
        self.variables = []

    def add_variables(self, L):
        for var in L:
            self.variables += [var]

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
        edges = [(u, node) for node in neighbors]
        result_def = []
        result_ref = []
        for edge in edges:
            if edge in self.arete_affectation:
                lambda_function = inspect.getsource(self.G.edges[edge[0], edge[1]]['cexp'])
                lambda_function = str(re.split("{|}", lambda_function)[1:-1])
                decisions = lambda_function.split(':')
                for index, decision in enumerate(decisions):
                    for var in self.variables:
                        if var in decision and index % 2 == 0:
                            result_def += [var]
        return result_def

    def ref_function(self, u):
        neighbors = list(self.G.adj[u])
        edges = [(u, node) for node in neighbors]
        result_ref = []
        for edge in edges:
            if edge in self.arete_affectation:
                lambda_function = inspect.getsource(self.G.edges[edge[0], edge[1]]['cexp'])
                lambda_function = str(re.split("{|}", lambda_function)[1:-1])
                decisions = lambda_function.split(':')
                for index, decision in enumerate(decisions):
                    for var in self.variables:
                        if var in decision and index % 2 == 1:
                            result_ref += [var]
            elif edge in self.arete_decision:
                lambda_function = inspect.getsource(self.G.edges[edge[0], edge[1]]['bexp'])
                lambda_function = str(re.split("{|}", lambda_function)[1:-1])
                decisions = lambda_function.split(':')
                for index, decision in enumerate(decisions):
                    for var in self.variables:
                        if var in decision and index % 2 == 1:
                            result_ref += [var]
        return result_ref


    def parcours_tous_chemins(self, j=2):
        """ Parcours tous les chemins partant du noeud racine jusqu'au noeud final """
        buffer = []
        L = [] #liste des arêtes à parcourir
        T = {1:[]} #dictionnaire contenant tous les chemins commencant en 1 et terminant au noeud final
        i = 1 #numero du chemin en cours
        k = 1 #numéro de la boucle
        noeuds_visites = [1]
        loops = {}
        
        def visit(noeud):
            nonlocal L
            nonlocal T
            nonlocal buffer
            nonlocal i
            nonlocal k
            nonlocal loops
            nonlocal noeuds_visites
            if noeud in noeuds_visites:         # permet de créer un boucle si il y en a 
                noeuds_visites.append(noeud)
                loops[k] = []
                start = noeuds_visites.index(noeud)
                for _ in range(start, len(noeuds_visites)-1): # si on repasse par un sommet déjà viisté, alors c'est une boucle, on la met en buffer
                    loops[k].append( (noeuds_visites[_], noeuds_visites[_+1]) )
                k += 1
            else:
                noeuds_visites.append(noeud)
            
            voisins = list(self.G.adj[noeud])                                       #   stocke les noeuds adjacents
            voisins_aretes = list(zip([noeud]*len(voisins), voisins))               #   donne les arêtes adjacantes

            L += voisins_aretes
            
            try:
                if len(voisins) > 1:                            #   si il y a plus d'un chemin...
                    buffer += list(T[i])                        #   ...alors on stocke le chemin parcouru dans un buffer
                elif len(voisins) == 0 and L[-1][0] != 1:       #   si on arrive au noeud final du chemin et que le dernier élément de L (liste d'éléments à parcourir)
                                                                #   ... n'est pas le noeud de départ alors on passe au chemin suivant...
                    if i>1 and T[i] == T[i-1]:  
                        print("loop -> ", loops[k-1])               
                        del T[i]                                # (si il y a une boucle on supprime le chemin actuel car doublon)
                        L.pop()                                 # et le dernier élément des éléments à visiter)
                        loops[k-1]                              # et la boucle actuelle car doublon aussi)
                    else:
                        i += 1                                     
                        T[i] = list(buffer)                     #   ...et on ajoute au début de ce chemin le buffer
                elif len(voisins) == 0 and L[-1][0] == 1 :      #   Si le dernier élément de L est une arête commençant par 1, on passe au chemin suivant
                    if i>1 and T[i] == T[i-1]:     
                        print("loop ->", loops[k-1])               
                        del T[i]                               
                        L.pop()
                        del loops[k-1] 
                    else:
                        i += 1
                        T[i] = []
                        buffer.clear()
                        noeuds_visites = [1]
            except:
                pass
                
        visit(1)
        while L:
            nv = L.pop()
            T[i].append(nv)
            visit(nv[1])
            # print("elt à parcourir:", L, "\nchemins:",T, "\ndict_nb_visites", visited_edges)
        
        del loops[1]
        for boucle in loops.values():
            for _ in range(1, len(T)+1):
                if set(boucle).issubset(T[_]):                                  # Vérifie si il la boucle existe dans chaque chemin
                    insert_index = T[_].index(boucle[-1])+1                     # Si oui, on découpe la liste: on prend la dernière arête de la boucle
                    rest = list(T[_][insert_index:])                            # ... puis le reste
                    i += 1  
                    T[i] = list(T[_][:insert_index]) + boucle * (j-1) + rest    # ... et on insère entre j-1 fois la boucle

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

