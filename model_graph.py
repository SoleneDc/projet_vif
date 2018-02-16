# 08/02/2018 Solène Duchamp - Charles Jacquet

# Module contenant une classe qui crée le graphe associé au programme 
# et possède les méthodes nécessaire pour les vérifications

import networkx as nx
import matplotlib.pyplot as plt
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
        """ Parcours tous les chemins partant du noeud racine jusqu'au noeud final. Le chemin contiendra
        exactement j tours de chaque boucle s'il y en a.
        :param j: nombre de tours de boucle souhaité
        :return: Dictionaire de chemins possibles dans le graphe
         """
        buffer = []
        L = [] #liste des arêtes à parcourir
        T = {1:[]} #dictionnaire contenant tous les chemins commencant en 1 et terminant au noeud final
        i = 1 #numero du chemin en cours
        
        def visit(noeud):
            nonlocal L
            nonlocal T
            nonlocal buffer
            nonlocal i
            
            voisins = list(self.G.adj[noeud])                                       #   stocke les noeuds adjacents
            voisins_aretes = list(zip([noeud]*len(voisins), voisins))               #   donne les arêtes adjacantes

            L += voisins_aretes

            if len(voisins) > 1:                                #   si il y a plus d'un chemin...
                buffer += list(T[i])                            #   ...alors on stocke le chemin parcouru dans un buffer
            elif len(voisins) == 0 and L and L[-1][0] != 1:     #   si on arrive au noeud final du chemin et que le dernier élément de L, s'il existe (liste d'éléments à parcourir)
                                                                #   ... n'est pas le noeud de départ alors on passe au chemin suivant...
                if (i>1 and T[i] == T[i-1]) or (i>2 and T[i] == T[i-2]) or (i>3 and T[i] == T[i-3]):  # // si le chemin qu'on a créé est identique à un chemin précédent, 
                    #print("loop (next not 1)")                                                       # // ... alors c'est une boucle
                    T[i].clear()                                                                      # // ... donc on supprime le chemin actuel car doublon
                    L.pop()                                                                           # // ... et le dernier élément des éléments à visiter
                else:
                    i += 1                                     
                    T[i] = list(buffer)                             #   ...et on ajoute au début de ce chemin le buffer
            elif len(voisins) == 0 and L and L[-1][0] == 1 :        #   Si le dernier élément de L est une arête commençant par 1, on passe au chemin suivant
                if (i>1 and T[i] == T[i-1]) or (i>2 and T[i] == T[i-2]) or (i>3 and T[i] == T[i-3]):  
                    #print("loop (next 1)")               
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
        to_clean = {key: chemin for key, chemin in T.items() if chemin and chemin[0][0] != 1 }
        for elt in to_clean.values():
            node_to_link = elt[0][0]
            to_add = [edge for edge in (self.arete_affectation + self.arete_decision) if edge[1] == node_to_link]
            for edge in to_add:
                i += 1
                clean[i] = [edge] + elt

        #détecte les boucles dans les chemins et crée des circuits avec j tours de boucle
        for key, chemin in clean.items():
            noeuds_visites = []
            for j, edge in enumerate(chemin): 
                if edge[0] not in noeuds_visites: 
                    noeuds_visites.append(edge[0])
                else:                                                               # si on passe par un noeud déjà visité, alors c'estune boucle
                    start = noeuds_visites.index(edge[0])
                    boucle = chemin[start:j]
                    # print("found loop :", boucle)

                    insert_index = chemin.index(boucle[-1])+1                       # On découpe chemin : on prend la dernière arête de la boucle
                    rest = list(chemin[insert_index:])                              # ... puis le reste
                    clean[key] = list(chemin[:insert_index]) + boucle * (j-1) + rest  # ... et on insère entre j-1 fois la boucle

        return clean

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
        nx.draw_networkx(self.G, with_labels=True, arrowstyle ='-->', arrowsize=10)
        plt.show()

