
# Solveur à contraintes pour trouver des sets de test

from pyscipopt import Model, quicksum
from programme_1 import *
import numpy as np

def a_oppose(dict_etat):
    dict_etat['x'] = - dict_etat['x']
    return dict_etat

def d_inf_0(dict_etat):
    if dict_etat['x'] <= 0:
        return True
    return False



def test_value_generator(graphe_controle, dict_etat):
    
    model = Model("test_value_generator")
    var = {key: [] for key in dict_etat.keys()}
    i = 0

    for chemin in graphe_controle.parcours_tous_chemins().values():
        for arete in chemin: 
            if arete in graphe_controle.arete_decision:
                for key in dict_etat.keys():
                    var[key].append( model.addVar("{}[{}]".format(key, i), lb=-100, vtype="I") )

                    fct = graphe_controle.G.edges[arete[0], arete[1]]['bexp']
                    model.addCons(fct(dict_etat))

            elif arete in graphe_controle.arete_affectation:
                fct = graphe_controle.G.edges[i, node]['cexp'](dict_etat)

        model.setObjective(x)
        model.optimize()
                
        if model.getStatus() != 'optimal':
            print('LP is not feasible!')
        else:
            print("Optimal value: %f" % model.getObjVal())
            print("x: = %f" % model.getVal(x))

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

    test_value_generator(prog1_graph, {'x': 2})