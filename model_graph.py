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

    def is_loop(self):
        edges = self.arete_affectation + self.arete_decision
        for u, v in edges:
            if v <= u:
                return True
        return False


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
        return list(set(result_def))

    def ref_function(self, u):
        if u == self.nodes_number:
            return self.variables
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
                lambda_function = str(re.split("lambda dic:", lambda_function)[1:])
                decisions = re.split("<=|>|==|!=", lambda_function)
                for decision in decisions:
                    for var in self.variables:
                        if var in decision:
                            result_ref += [var]
        return list(set(result_ref))

    #TODO :régler le cas des graphes avec cycle (ajouter un i pour les boucles !!)



    def parcours_tous_chemins(self, j=4):
        """ Parcours tous les chemins partant du noeud racine jusqu'au noeud final """
        buffer = []
        L = []  # liste des arêtes à parcourir
        T = {1: []}  # dictionnaire contenant tous les chemins commencant en 1 et terminant au noeud final
        i = 1  # numero du chemin en cours
        visited_edges = {}

        def visit(noeud):
            nonlocal L
            nonlocal T
            nonlocal buffer
            nonlocal i
            nonlocal visited_edges
            nonlocal j
            voisins = list(self.G.adj[noeud])  # stocke les noeuds adjacants
            L += zip([noeud] * len(voisins), voisins)  # donne les arêtes adjacantes
            for edge in L:
                if edge in visited_edges.keys():
                    if visited_edges[edge] > j:
                        L.remove(edge)
                    else:
                        visited_edges[edge] = visited_edges[edge]+1
                else:
                    visited_edges[edge] = 1
            try:
                if len(voisins) > 1:  # si il y a plus d'un chemin...
                    buffer += list(T[i])  # alors on stocke le chemin parcouru dans un buffer
                elif len(voisins) == 0 and :  # si on arrive au noeud final et que mon dernier élément
                    #   à parcourir n'est pas le noeud de départ...
                    i += 1  # alors on passe au chemin suivant
                    T[i] = list(buffer)  # et on ajoute au début de ce chemin le buffer
                elif len(voisins) == 0:
                    i += 1
                    T[i] = []
                    buffer = []
            except:
                pass

        visit(1)
        while L: # tant que L n'est pas vide
            nv = L.pop(len(L) - 1) # on prend le premier noeud de la liste des voisins
            T[i].append(nv)
            visit(nv[1])
        return T

    # def parcours_tous_chemins(self, j=4):
    #     """ Parcours tous les chemins partant du noeud racine jusqu'au noeud final """
    #     buffer = []
    #     L = []  # liste des arêtes à parcourir
    #     T = {1: []}  # dictionnaire contenant tous les chemins commencant en 1 et terminant au noeud final
    #     i = 1  # numero du chemin en cours
    #     visited_edges = {}
    #
    #     def visit(noeud):
    #         nonlocal L
    #         nonlocal T
    #         nonlocal buffer
    #         nonlocal i
    #         nonlocal visited_edges
    #         nonlocal j
    #         voisins = list(self.G.adj[noeud])  # stocke les noeuds adjacants
    #         L += zip([noeud] * len(voisins), voisins)  # donne les arêtes adjacantes
    #         for edge in L:
    #             if edge in visited_edges.keys():
    #                 if visited_edges[edge] > j:
    #                     L.remove(edge)
    #                 else:
    #                     visited_edges[edge] = visited_edges[edge]+1
    #             else:
    #                 visited_edges[edge] = 1
    #         try:
    #             if len(voisins) > 1:  # si il y a plus d'un chemin...
    #                 buffer += list(T[i])  # alors on stocke le chemin parcouru dans un buffer
    #             elif len(voisins) == 0 and :  # si on arrive au noeud final et que mon dernier élément
    #                 #   à parcourir n'est pas le noeud de départ...
    #                 i += 1  # alors on passe au chemin suivant
    #                 T[i] = list(buffer)  # et on ajoute au début de ce chemin le buffer
    #             elif len(voisins) == 0:
    #                 i += 1
    #                 T[i] = []
    #                 buffer = []
    #         except:
    #             pass
    #
    #     visit(1)
    #     while L: # tant que L n'est pas vide
    #         nv = L.pop(len(L) - 1) # on prend le premier noeud de la liste des voisins
    #         T[i].append(nv)
    #         visit(nv[1])
    #     return T

    def parcours_tous_chemins_pour_solene(self):
        """ A partir d'une liste d'arêtes, renvoie les chemins sous forme de string """
        T = self.parcours_tous_chemins()
        L = []
        for i in range(len(T)):
            L += ['']
        i = 0
        for key in T.keys():
            for edge in T[key]:
                u, v = edge
                if str(u) not in L[i]:
                    L[i] += str(u)
                L[i] += str(v)
            i += 1
        return L



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
        if not self.is_loop():
            return True
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

    def toutes_les_def(self, jeu_test=[{'x': -1}, {'x': 5}]):
        path_between = {}
        variables = self.variables
        available_path = self.parcours_tous_chemins_pour_solene()
        for var in variables:                                       # Ici on récupère pour chaque variable les noeuds tels
            path_between[var] = {}                                  # que var dans def(node) et var dans ref(node)
            path_between[var]['nodes_from'] = []
            path_between[var]['nodes_to'] = []
            for node in range(1, self.nodes_number+1):
                if var in self.def_function(node):
                    path_between[var]['nodes_from'] += [node]
                if var in self.ref_function(node):
                    path_between[var]['nodes_to'] += [node]

        all_testing_path = []
        def_nodes = list(path_between[var]['nodes_from'])
        for dict_test in jeu_test:                                  # on génère les chemins des données de test
            all_testing_path += [self.travel_with_path(dict_test)]
        for var in variables:
            for u in path_between[var]['nodes_from']:
                for v in path_between[var]['nodes_to']:
                    if v > u and u in def_nodes and not self.is_loop():
                        for path_to_test in all_testing_path:
                            if str(u) in path_to_test:
                                following_path = path_to_test.split(str(u))[1]
                                if str(v) in following_path:
                                    def_nodes.remove(u)
                                    if def_nodes == []:             # on s'arrête si notre liste de def_nodes est vide
                                        return True
                                    break
                    elif self.is_loop():
                        print('Attention')
                        ##TODO : ajouter le cas looop
                                                                    # si notre liste def_nodes n'est pas vide
        return False, def_nodes                                     # le critère n'est pas vérifié

    # def toutes_les_def(self, jeu_test=[{'x': -1}, {'x': 5}]):
    #
    #     path_between = {}
    #     variables = self.variables
    #     available_path = self.parcours_tous_chemins_pour_solene()
    #     for var in variables:                                       # Ici on récupère pour chaque variable les noeuds tels
    #         path_between[var] = {}                                  # que var dans def(node) et var dans ref(node)
    #         path_between[var]['nodes_from'] = []
    #         path_between[var]['nodes_to'] = []
    #         for node in range(1, self.nodes_number+1):
    #             if var in self.def_function(node):
    #                 path_between[var]['nodes_from'] += [node]
    #             if var in self.ref_function(node):
    #                 path_between[var]['nodes_to'] += [node]
    #     path_between_ok = {}
    #     for var in variables:                                       # On créé les couples (node1, node2) tels qu'il existe
    #         path_between_ok[var] = []                               # un chemin passant par node1 puis node2
    #         nodes_from = path_between[var]['nodes_from']
    #         nodes_to = path_between[var]['nodes_to']
    #         for u in nodes_from:
    #             for v in nodes_to:
    #                 if v > u:
    #                     for path in available_path:
    #                         if str(u) in path and str(v) in path:
    #                             if str(v) in path.split(str(u))[1] and (u, v) not in path_between_ok[var]:
    #                                 path_between_ok[var] += [(u, v)]
    #     all_testing_path = []
    #     for dict_test in jeu_test:                                  # on génère les chemins des données de test
    #         all_testing_path += [self.travel_with_path(dict_test)]
    #     for var in variables:                                       # pour chaque (node1, node2) on vérifie qu'il existe
    #         for u, v in path_between_ok[var]:                       # un chemin dans nos données de test passant par node1
    #                 for path_to_test in all_testing_path:           # puis node2
    #                     if str(u) in path_to_test:
    #                         following_path = path_to_test.split(str(u))[1]
    #                         if str(v) in following_path:
    #                             path_between_ok[var].remove((u, v))
    #     for var in variables:                                       # si il reste des couples (node1, node2) le critère
    #         if path_between_ok[var] != []:                          # n'est pas vérifié
    #             return False, path_between_ok
    #
    #     return True

    def toutes_les_utilisations(self, jeu_test=[{'x': -1}, {'x': 5}]):

        path_between = {}
        variables = self.variables
        available_path = self.parcours_tous_chemins_pour_solene()
        for var in variables:                                       # on récupère les variables tq
            path_between[var] = {}
            path_between[var]['nodes_from'] = []                    # var dans def(node) et var dans ref(node)
            path_between[var]['nodes_to'] = []
            for node in range(1, self.nodes_number+1):
                if var in self.def_function(node):
                    path_between[var]['nodes_from'] += [node]
                if var in self.ref_function(node):
                    path_between[var]['nodes_to'] += [node]
        path_between_ok = {}
        for var in variables:                                       # On créé les couples (node1, node2) tels qu'il existe
            path_between_ok[var] = []                               # un chemin passant par node1 puis node2
            nodes_from = path_between[var]['nodes_from']
            nodes_to = path_between[var]['nodes_to']
            for u in nodes_from:
                for v in nodes_to:
                    if v > u:                       #TODO: Attention on ne prend pas en compte les cycles
                        for path in available_path:
                            if str(u) in path and str(v) in path:
                                if str(v) in path.split(str(u))[1] and (u, v) not in path_between_ok[var]:
                                    nodes_between = self.nodes_between(u, v, available_path)
                                    path_between_ok[var] += [(u, v)]
                                    for path_of_nodes in nodes_between:
                                        for node_between in path_of_nodes:
                                            w = int(node_between)
                                            if var in self.def_function(w) and (u, v) in path_between_ok[var]:
                                                path_between_ok[var].remove((u, v))

        all_testing_path = []
        path_to_confirm = {}
        for dict_test in jeu_test:                                  # on génère les chemins des données de test
            all_testing_path += [self.travel_with_path(dict_test)]
        for var in variables:                                       # pour chaque (node1, node2) on vérifie qu'il existe
            path_between_ok[var] = list(set(path_between_ok[var]))
            path_to_confirm[var] = list(path_between_ok[var])
            for tuple in path_between_ok[var]:                       # un chemin dans nos données de test passant par node1
                    for path_to_test in all_testing_path:           # puis node2
                        if tuple in path_to_confirm[var]:
                            u, v = tuple[0], tuple[1]
                            if str(u) in path_to_test:
                                following_path = path_to_test.split(str(u))[1]
                                if str(v) in following_path and (u,v) in path_between_ok[var]:
                                    path_to_confirm[var].remove((u, v))
                                print(path_to_confirm, (u,v), 'removed')
        for var in variables:                                       # si il reste des couples (node1, node2) le critère
            if path_to_confirm[var] != []:                          # n'est pas vérifié
                return False, path_to_confirm

        return True








    def travel_with_path (self, dict_etat):
        """ Fonction permettant de parcourir le graphe, en fonction d'une valuation initiale \n
        :param dict_etat: valuation initiale \n
        :return: le chemin """
        path = '1'
        i = 1  # ou on est sur le graphe
        dict_etat_to_travel = dict(dict_etat)
        while i < self.nodes_number:
            self.G.nodes[i]['etat'] = dict_etat_to_travel
            noeuds_voisins = list(self.G.adj[i])
            for node in noeuds_voisins:
                if self.G.edges[i, node]['bexp'](dict_etat_to_travel):
                    self.G.edges[i, node]['cexp'](dict_etat_to_travel)
                    i = node
                    path += str(node)
                    break
        return path

    def nodes_between(self, u, v, available_path):
        nodes_between = []
        for path in available_path:
            if str(u) in path and str(v) in path and str(u)+str(v) not in path:
                path = path.split(str(u))[1]
                path = path.split(str(v))[0]
                nodes_between += [path]
        return list(set(nodes_between))




    
    def show_graph(self):
        """ Pour afficher le graphe dans une nouvelle fenêtre """
        nx.draw(self.G, with_labels=True)
        plt.show()


    def testing_generation(self):
        pass

