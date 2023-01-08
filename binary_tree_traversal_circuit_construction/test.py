
from load_data import *
from numpy import *
import itertools as it
from node_actions import *
from node import *
from cnot import *
from algorithm import *
from tableau import *
from cross_sort import *
from qiskit import *
import random
from qiskit.quantum_info import Operator
#from algorithm2 import *


n = 4
Z = array(list(it.product([0,1], repeat=n)))
rdindx = random.sample(range(n**2),5)
#print(rdindx)
Z = Z[rdindx]
S = array([random.choice(range(2)) for j in range(len(Z))])
Coefs = ones(len(Z))
print(Z)


#build the tree
# print("\nThe circuit without Z-sorting")
# root = load_tree(Z,S, Coefs)
# qc = QuantumCircuit(n)
# qc = algorithm(root, qc, n, 1)
# print(qc)
# print(qc.count_ops())

# print("\nThe circuit with Z-sorting")
# scores = msb_sort(Z)
# print(scores)
# newroot = load_tree(Z,S, Coefs, sorting=list(scores))
# qc = QuantumCircuit(n)
# qc = algorithm(newroot, qc, n, 1)
# print(qc)
# print(qc.count_ops())
#
# msb_sort(Z)

# A, B = separate_strings(Z,1,3)
# print("A = ", A)
# print("B = ",B)
#eta = cross(Z,1,2)
eta = cross_top_sort(Z)
print(eta)
#print(cross(Z,2,1))
#print(cross_top_sort(Z))



newroot = load_tree(Z,S, Coefs, sorting=eta)
qc = QuantumCircuit(n)
qc = algorithm(newroot, qc, n, 1)
print(qc)
print(qc.count_ops())
