import helpers
from qiskit import QuantumCircuit

# qc = helpers.load_qpycircuit("RESULTS_or/QC.qpy")
# print(qc[0])

qc1 = helpers.load_qpycircuit("RESULTS_or/Cluster_0/time_evolution_circuit.qpy")
print(qc1)

print("diagonalizing circuit")
qc1 = helpers.load_qpycircuit("RESULTS_or/Cluster_0/diagonalizing_circuit.qpy")
print(qc1)