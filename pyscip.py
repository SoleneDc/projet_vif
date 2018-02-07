
# Solveur à contraintes pour trouver des sets de test

from pyscipopt import Model, quicksum
import numpy as np

def a_oppose(dict_etat):
    dict_etat['x'] = - dict_etat['x']
    return dict_etat

model = Model("try")

x = model.addVar("x", lb = -100, vtype = "I")
model.setObjective(x)
model.addCons(x <= 0)
model.addCons(-x == 1)
# model.addCons(a_oppose({'x': x})['x'] == -1)
model.optimize()

if model.getStatus() != 'optimal':
    print('LP is not feasible!')
else:
    print("Optimal value: %f" % model.getObjVal())
    print("x: = %f" % model.getVal(x))