
# Solveur à contraintes pour trouver des sets de test

from pyscipopt import Model, quicksum
from programme_1 import *
import numpy as np
import inspect
import re



def test_value_generator(graphe_controle, dict_etat):
    
    model = Model("test_value_generator")
    var = {key: [] for key in dict_etat.keys()}
    i = 0

    for chemin in graphe_controle.parcours_tous_chemins().values():
        for arete in chemin: 
            if arete in graphe_controle.arete_decision:
                for key in dict_etat.keys():
                    var[key].append( model.addVar("{}_{}".format(key, i), lb=-100, vtype="I") )

                    lambda_function = inspect.getsource(graphe_controle.G.edges[arete[0], arete[1]]['bexp'])
                    lambda_function = lambda_function.split("lambda dict: ")[-1][:-1]
                    print(lambda_function)
                    if "and" in lambda_function or "or" in lambda_function:
                        decisions = lambda_function.split("and").split("or")
                        for elt in decisions:
                            print(decision)             # il faut continuer à faire les dichotomies de cas 
                            if ">=" in elt :
                                op = elt.split(">=")
                                model.addCons(op[0] >= op[2])
                            elif "<=" in elt :
                                op = elt.split("<=")
                                model.addCons(op[0] <= op[2])
                            elif "!=" in elt:
                                pass
                            else: 
                                op = elt.split("<").split(">").split("==")
                                if 
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