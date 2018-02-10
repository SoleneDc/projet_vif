
# Solveur à contraintes pour trouver des sets de test

from pyscipopt import Model, quicksum
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
                    var[key].append( model.addVar("{}[{}]".format(key, i), lb = -100, vtype = "I") )

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