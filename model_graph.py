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
        if u == 1:
            return self.variables
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

    def parcourir_boolean(self, dict_etat):
        """ Fonction permettant de parcourir le graphe, en fonction d'une valuation initiale \n
        :param dict_etat: valuation initiale \n
        :return: deux listes (vrai/faux) avec les arêtes de décisions parcourues """
        aretes_vraies = []
        aretes_fausses = []
        i = 1  # ou on est sur le graphe
        while i < self.nodes_number:
            self.G.nodes[i]['etat'] = dict_etat
            noeuds_voisins = list(self.G.adj[i])
            node_to_go = []
            for node in noeuds_voisins:
                if not self.G.edges[i, node]['bexp'](dict_etat):
                    aretes_fausses += [(i, node)]
                elif self.G.edges[i, node]['bexp'](dict_etat):
                    aretes_vraies += [(i, node)]
                    self.G.edges[i, node]['cexp'](dict_etat)
                    node_to_go += [node]
            if len(node_to_go) > 1:
                raise EnvironmentError
            i = node_to_go[0]
        for edge in aretes_vraies:
            if edge not in self.arete_decision:
                aretes_vraies.remove(edge)
        for edge in aretes_fausses:
            if edge not in self.arete_decision:
                aretes_fausses.remove(edge)
        return aretes_vraies, aretes_fausses

    def parcours_tous_chemins(self, j=1):
        """ Parcours tous les chemins partant du noeud racine jusqu'au noeud final. Le chemin contiendra
        exactement j tours de chaque boucle s'il y en a.
        :param j: nombre de tours de boucle souhaité
        :return: Dictionaire de chemins possibles dans le graphe
         """
        buffer = []
        L = []  # liste des arêtes à parcourir
        T = {1: []}  # dictionnaire contenant tous les chemins commencant en 1 et terminant au noeud final
        i = 1  # numero du chemin en cours

        def visit(noeud):
            nonlocal L
            nonlocal T
            nonlocal buffer
            nonlocal i

            voisins = list(self.G.adj[noeud])  # stocke les noeuds adjacents
            voisins_aretes = list(zip([noeud] * len(voisins), voisins))  # donne les arêtes adjacantes

            L += voisins_aretes

            if len(voisins) > 1:  # si il y a plus d'un chemin...
                buffer += list(T[i])  # ...alors on stocke le chemin parcouru dans un buffer
            elif len(voisins) == 0 and L and L[-1][
                0] != 1:  # si on arrive au noeud final du chemin et que le dernier élément de L, s'il existe (liste d'éléments à parcourir)
                #   ... n'est pas le noeud de départ alors on passe au chemin suivant...
                if (i > 1 and T[i] == T[i - 1]) or (i > 2 and T[i] == T[i - 2]) or (i > 3 and T[i] == T[
                        i - 3]):  # // si le chemin qu'on a créé est identique à un chemin précédent,
                    # print("loop (next not 1)")                                                       # // ... alors c'est une boucle
                    T[i].clear()  # // ... donc on supprime le chemin actuel car doublon
                    L.pop()  # // ... et le dernier élément des éléments à visiter
                else:
                    i += 1
                    T[i] = list(buffer)  # ...et on ajoute au début de ce chemin le buffer
            elif len(voisins) == 0 and L and L[-1][
                0] == 1:  # Si le dernier élément de L est une arête commençant par 1, on passe au chemin suivant
                if (i > 1 and T[i] == T[i - 1]) or (i > 2 and T[i] == T[i - 2]) or (i > 3 and T[i] == T[i - 3]):
                    # print("loop (next 1)")
                    T[i].clear()
                    L.pop()
                else:
                    i += 1
                    T[i] = []
                    buffer.clear()

        visit(1)
        while L:
            nv = L.pop()
            T[i].append(nv)
            visit(nv[1])
            # print("elt à parcourir:", L, "\nchemins:",T, "\ndict_nb_visites", visited_edges)

        # nettoie les chemins, enlève les chemins vides et isole les chemins ne commençant pas par 1
        clean = {key: chemin for key, chemin in T.items() if chemin and chemin[0][0] == 1}
        to_clean = {key: chemin for key, chemin in T.items() if chemin and chemin[0][0] != 1}
        for elt in to_clean.values():
            node_to_link = elt[0][0]
            to_add = [edge for edge in (self.arete_affectation + self.arete_decision) if edge[1] == node_to_link]
            for edge in to_add:
                i += 1
                clean[i] = [edge] + elt

        # détecte les boucles dans les chemins et crée des circuits avec j tours de boucle
        for key, chemin in clean.items():
            noeuds_visites = []
            for nb, edge in enumerate(chemin):
                if edge[0] not in noeuds_visites:
                    noeuds_visites.append(edge[0])
                else:  # si on passe par un noeud déjà visité, alors c'estune boucle
                    start = noeuds_visites.index(edge[0])
                    boucle = chemin[start:nb]
                    # print("found loop :", boucle)

                    insert_index = chemin.index(
                        boucle[-1]) + 1  # On découpe chemin : on prend la dernière arête de la boucle
                    rest = list(chemin[insert_index:])  # ... puis le reste
                    clean[key] = list(chemin[:insert_index]) + boucle * (
                    j - 1) + rest  # ... et on insère entre j-1 fois la boucle

        return clean

    def parcours_tous_chemins_pour_solene(self, j=1):
        """ A partir d'une liste d'arêtes, renvoie les chemins sous forme de string """
        T = self.parcours_tous_chemins(j)
        L = []
        for i in range(len(T)):
            L += ['']
        i = 0
        for key in T.keys():
            for edge in T[key]:
                u, v = edge
                if L[i] == '':
                    L[i] += str(u)
                L[i] += str(v)
            i += 1
        print(L)
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
            return f"{100}%"
        chemins_jeu_test = []
        for dict_test in jeu_test:
            chemins_jeu_test += [self.parcourir(dict_test)[0]]

        print(chemins_jeu_test)


        chemins =[]
        for k in range(1, i+1):
            dict_chemins = self.parcours_tous_chemins(j=k)
            for path in dict_chemins.values():
                if path not in chemins:
                    chemins += [path]
        print(chemins)
        chemins_to_still_do = list(chemins)
        for chemin in chemins:
            if chemin in chemins_jeu_test:
                chemins_to_still_do.remove(chemin)

        if len(chemins_to_still_do) == 0:
            return f"{100}%"
        else:
            return f"{round((1 - len(chemins_to_still_do)/ len(chemins))*100)} %, missing path {chemins_to_still_do}"
    
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
        def_nodes = {}
        to_cover = {}
        for var in variables:                                       # Ici on récupère pour chaque variable les noeuds tels
            path_between[var] = {}                                  # que var dans def(node) et var dans ref(node)
            path_between[var]['nodes_from'] = []
            path_between[var]['nodes_to'] = []
            for node in range(1, self.nodes_number+1):
                if var in self.def_function(node):
                    path_between[var]['nodes_from'] += [node]
                if var in self.ref_function(node):
                    path_between[var]['nodes_to'] += [node]
            def_nodes[var] = list(path_between[var]['nodes_from'])
            to_cover[var] = len(def_nodes[var])

        print(path_between)
        all_testing_path = []

        for dict_test in jeu_test:                                  # on génère les chemins des données de test
            all_testing_path += [self.travel_with_path(dict_test)]
        for var in variables:
            print ('def nodes', def_nodes)
            for u in path_between[var]['nodes_from']:
                for v in path_between[var]['nodes_to']:
                    if v > u and u in def_nodes[var] and not self.is_loop():
                        for path_to_test in all_testing_path:
                            if str(u) in path_to_test:
                                following_path = path_to_test.split(str(u))[1]
                                if str(v) in following_path:
                                    def_nodes[var].remove(u)
                                    print(def_nodes)

                    elif self.is_loop():                            # ici on doit quand même considérer les noeuds tq u > v !
                        if u in def_nodes[var]:
                            for path_to_test in all_testing_path:
                                if str(u) in path_to_test:
                                    following_path = path_to_test.split(str(u))[1]
                                    print(path_to_test, following_path)
                                    if str(v) in following_path:
                                        print(u, v, def_nodes)
                                        def_nodes[var].remove(u)
                                        break

        summ = 0
        sum_to_cover = 0
        for var in variables:
            summ += len(def_nodes[var])
            sum_to_cover += to_cover[var]
        if sum_to_cover == 0:
            return f"{100}%"
        elif summ/ sum_to_cover != 0:
            return f"{round((1 - summ/ sum_to_cover)*100)} %, missing nodes {def_nodes}"
        else:
            return f"{round((1 - summ/ sum_to_cover)*100)} %"

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
        path_between_to_cover = {}
        for var in variables:                                             # On créé les couples (node1, node2) tels qu'il existe
            path_between_to_cover[var] = []                               # un chemin passant par node1 puis node2
            nodes_from = path_between[var]['nodes_from']
            nodes_to = path_between[var]['nodes_to']
            for u in nodes_from:
                for v in nodes_to:
                    if v > u and not self.is_loop():
                        for path in available_path:
                            if str(u) in path and str(v) in path:
                                if str(v) in path.split(str(u))[1] and (u, v) not in path_between_to_cover[var]:
                                    nodes_between = self.nodes_between(u, v, available_path)
                                    path_between_to_cover[var] += [(u, v)]
                                    for path_of_nodes in nodes_between:     # si la variable est redéfinie entre u et v, pas besoin de considérer ce couple
                                        for node_between in path_of_nodes:
                                            w = int(node_between)
                                            if var in self.def_function(w) and (u, v) in path_between_to_cover[var]:
                                                path_between_to_cover[var].remove((u, v))
                    else:
                        for path in available_path:
                            if str(u) in path and str(v) in path:
                                if str(v) in path.split(str(u))[1] and (u, v) not in path_between_to_cover[var]:
                                    nodes_between = self.nodes_between(u, v, available_path)
                                    path_between_to_cover[var] += [(u, v)]
                                    for path_of_nodes in nodes_between:
                                        for node_between in path_of_nodes:
                                            w = int(node_between)
                                            if var in self.def_function(w) and (u, v) in path_between_to_cover[var]:
                                                path_between_to_cover[var].remove((u, v))

        all_testing_path = []
        path_to_confirm = {}
        for dict_test in jeu_test:                                  # on génère les chemins des données de test
            all_testing_path += [self.travel_with_path(dict_test)]
        for var in variables:                                       # pour chaque (node1, node2) on vérifie qu'il existe
            path_between_to_cover[var] = list(set(path_between_to_cover[var]))
            path_to_confirm[var] = list(path_between_to_cover[var])
            for tuple in path_between_to_cover[var]:                       # un chemin dans nos données de test passant par node1
                    for path_to_test in all_testing_path:           # puis node2
                        if tuple in path_to_confirm[var]:
                            u, v = tuple[0], tuple[1]
                            if str(u) in path_to_test:
                                list_following_path = path_to_test.split(str(u))[1:]
                                for following_path in list_following_path:
                                    if str(v) in following_path and (u, v) in path_to_confirm[var]:
                                        path_to_confirm[var].remove((u, v))

        summ = 0
        sum_to_cover = 0
        for var in variables:
            summ += len(path_to_confirm[var])
            sum_to_cover += len(path_between_to_cover[var])
        if sum_to_cover == 0:
            return f"{100}%"
        elif summ/ sum_to_cover != 0:
            return f"{round((1 - summ/ sum_to_cover)*100)} %, missing uses {path_to_confirm}"
        else:
            return f"{round((1 - summ/ sum_to_cover)*100)} %"

    def tous_les_DU_chemins(self, jeu_test=[{'x': -1}, {'x': 5}]):

        path_between = {}
        variables = self.variables
        available_path = self.parcours_tous_chemins_pour_solene(j=1)
        print(available_path)

        for var in variables:                                       # on récupère les variables du graphe
            path_between[var] = {}
            path_between[var]['nodes_from'] = []                    # nodes_from : var dans def(node)
            path_between[var]['nodes_to'] = []                      # nodes_to : var dans ref(node)
            for node in range(1, self.nodes_number+1):
                if var in self.def_function(node):
                    path_between[var]['nodes_from'] += [node]
                if var in self.ref_function(node):
                    path_between[var]['nodes_to'] += [node]
        path_between_to_cover = {}                                  # ici on va stocker les chemins partiels entre u et v pour chaque variable
        for var in variables:
            path_between_to_cover[var] = []
            nodes_from = path_between[var]['nodes_from']
            nodes_to = path_between[var]['nodes_to']
            for u in nodes_from:
                for v in nodes_to:
                    chemins_partiels = self.chemins_partiels(u, v, available_path)
                    for path in chemins_partiels:
                        path_between_to_cover[var] += [path]
                        in_between = path.split(str(u))[1].split(str(v))[0]
                        if in_between != '':
                            for node in in_between:                 # on s'assure que var n'est pas redéfinie entre u et v
                                w = int(node)
                                if var in self.def_function(w) and path in path_between_to_cover[var]:
                                    path_between_to_cover[var].remove(path)

        print('path to cover', path_between_to_cover)
        all_testing_path = []                                       # stocke les chemins du jeu de test
        path_to_confirm = {}                                        # contient les chemins à couvrir pas encore validés
        for dict_test in jeu_test:                                  # on génère les chemins des données de test
            all_testing_path += [self.travel_with_path(dict_test)]
        print('testing path', all_testing_path)

        for var in variables:                                       # ici on enlève les chemins validés par les données test
            path_to_confirm[var] = list(path_between_to_cover[var])
            for path in path_between_to_cover[var]:
                for testing_path in all_testing_path:
                    if path in testing_path and path in path_to_confirm[var]:
                        u = path[0]
                        v = path[-1]
                        split = testing_path.split(path)
                        if len(split) == 2 and u not in split[0] and v not in split[1]:
                            path_to_confirm[var].remove(path)

        summ = 0
        sum_to_cover = 0
        for var in variables:
            summ += len(path_to_confirm[var])
            sum_to_cover += len(path_between_to_cover[var])
        if sum_to_cover == 0:
            return f"{100}%"
        elif summ/ sum_to_cover != 0:
            return f"{round((1 - summ/ sum_to_cover)*100)} %, missing uses {path_to_confirm}"
        else:
            return f"{round((1 - summ/ sum_to_cover)*100)} %"

    def toutes_les_conditions(self, jeu_test=[{'x': -1}, {'x': 5}]):

        aretes_decisions = list(self.arete_decision)
        aretes_vraies = []
        aretes_fausses = []
        for dict_test in jeu_test:
            parcourir = self.parcourir_boolean(dict_test)
            aretes_vraies += parcourir[0]
            aretes_fausses += parcourir[1]

        aretes_vraies = set(aretes_vraies)
        aretes_fausses = set(aretes_fausses)

        summ_covered = len(aretes_vraies) + len(aretes_fausses)
        sum_to_cover = 2*len(aretes_decisions)
        aretes_decisions = set(aretes_decisions)


        if sum_to_cover == 0:
            return f"{100}%"
        elif summ_covered / sum_to_cover != 1:
            return f"{round((summ_covered/ sum_to_cover)*100)} %, missing true edges {aretes_decisions-aretes_vraies}, missing false edges {aretes_decisions-aretes_fausses}"
        else:
            return f"{round((summ/ sum_to_cover)*100)} %"


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

    def loop_edges(self):
        if not self.is_loop():
            raise AssertionError
        affectation_edges = self.arete_affectation
        loop_edges = []
        for u, v in affectation_edges:
            if u >= v:
                loop_edges += [(u,v)]
        return loop_edges

    def chemins_partiels(self, u, v, available_path):
        chemins = []
        for path in available_path:
            if str(u) in path:
                path_split = path.split(str(u))
                if len(path_split) == 2:
                    remaining_path = path_split[1]
                    if str(v) in remaining_path:
                        path_between = remaining_path.split(str(v))[0]
                        chemins += [str(u) + path_between + str(v)]
                else:
                    if str(v) in path_split[2]:
                        path_between = path_split[1] + str(u) + path_split[2].split(str(v))[0]
                        chemins += [str(u) + path_between + str(v)]
        return list(set(chemins))







    
    def show_graph(self):
        """ Pour afficher le graphe dans une nouvelle fenêtre """
        nx.draw(self.G, with_labels=True)
        plt.show()


    def testing_generation(self):
        pass

