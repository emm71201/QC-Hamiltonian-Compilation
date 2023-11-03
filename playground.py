import numpy as np
import helpers
from qiskit import QuantumCircuit

# reading the main circuit
QC = helpers.load_qpycircuit("RESULTS_OR/QC.qpy")
print("The number of gates in the main circuit: ", QC.count_ops())

# read the paulis in the first cluster
cluster1 = np.load("RESULTS_OR/Cluster_0/commuting_pauli_strings.npy", allow_pickle=True)
for pauli in cluster1:
    print(pauli)

# show the tableau after the pauli strings have been diagonalized
diagonalized_tableau = np.load("RESULTS_OR/Cluster_0/diagonalized_pauli_strings_tableau.npy", allow_pickle=True).item()
X = diagonalized_tableau["X"]
Z = diagonalized_tableau["Z"]
S = diagonalized_tableau["S"]
Coefs = diagonalized_tableau["Coefs"] # values of model coefficients.
print("The X matrix: should be all zero")
if X.any():
    print("The X matrix is not zero.")
else:
    print("And indeed it is")
print("The Z matrix:")
print(Z)


