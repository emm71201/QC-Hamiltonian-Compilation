# Author: Edison Murairi
# Date: January 6th, 2023

# Used the algorithms developed by the authors to compile a quantum circuit simulating
# the Hamiltonian time evolution.
# The Hamiltonian is represented as a linear combination of Pauli operators
# The first order Lie-Trotter product formula is used to decompose the unitary time evolution operator
# The Pauli operators are divided into clusters (Sets) of commuting operators
# Each cluster is diagonlized via the algorithm developed by the authors (see the paper: )
# Once diagonlized, the quantum circuit of the time evolution of the diagonal cluster is
# realized via the algorithm developed by the authors. See the paper
# https://journals.aps.org/prd/abstract/10.1103/PhysRevD.106.094504
import os
import sys
import shutil
sys.path.append("binary_tree_traversal_circuit_construction")

## Handle potentially missing dependencies.
import subprocess
if not "galois" in sys.modules:
    print("Installing Galois")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "galois"])
if not "qiskit" in sys.modules:
    print("Installing Qiskit")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "qiskit"])
if not "numpy" in sys.modules:
    print("Installing Numpy")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
######################################

from load_data import *
import itertools as it
from node_actions import *
from node import *
from cnot import *
from algorithm import *

import helpers
from grouping import *
import diagonalize
from tableau import *
from qiskit import QuantumCircuit

def compile_diagonal_cluster(X,Z,S,Coefs, sorting= None):

    """Return the quantum circuit simulating the time evolution of diagonal pauli strings"""

    #check the pauli strings are diagonal
    if X.any():
        print("This set is not diagonal")
        return


    n = X.shape[1]
    root = load_tree(numpy.array(Z),numpy.array(S), numpy.array(Coefs), sorting=sorting)
    qc = QuantumCircuit(n)
    qc = algorithm(root, qc, n, 1)

    return qc


def main_compiler(file, output, grouping_strategy=None, sorting=None):

    pauli_strings = pstrs = helpers.read_hamiltonian(file)
    commuting_clusters = make_clusters(pauli_strings, strategy=grouping_strategy)
    n = len(pauli_strings[0].string)
    QC = QuantumCircuit(n)

    ### Print a message before starting the main loop ####
    print("Number of Clusters (Sets) in which all the Pauli strings commute: {0}".format(len(commuting_clusters)))

    # Main loop: Iterate over the clusters of commuting pauli strings
    # 1. Construct a quantum circuit diagonalizing a cluster and insert the circuit into the main circuit QC
    # 2. Construct the circuit realizing the time evolution of the diagonalized cluster and insert into QC
    # 3  Insert the inverse of the diagonalizing circuit
    # 4. Take the next cluster and repeat until no cluster is left

    for key in commuting_clusters:

        cluster = commuting_clusters[key]
        Coefs = numpy.array([pauli_string.coef for pauli_string in cluster])
        X,Z,S,U = diagonalize.main_diagonalizer(cluster)
        qc = compile_diagonal_cluster(numpy.array(X),numpy.array(Z),numpy.array(S), Coefs, sorting= None)
        QC = QC.compose(U)
        QC = QC.compose(qc)
        QC = QC.compose(U.inverse())
        QC.barrier()

        # save the intermediate results
        cluster_path = os.path.join("RESULTS_{0}".format(output), "Cluster_{0}".format(key))
        os.mkdir(cluster_path)
        numpy.save(os.path.join(cluster_path, "commuting_pauli_strings.npy"), cluster)
        diagonalized_tableau_path = os.path.join(cluster_path, "diagonalized_pauli_strings_tableau.npy")
        numpy.save(diagonalized_tableau_path, {"X":X,"Z":Z,"S":S,"Coefs":Coefs})
        diagonalizing_circuit_path = os.path.join(cluster_path, "diagonalizing_circuit.qasm")
        U.qasm(filename=diagonalizing_circuit_path)
        time_evolution_circuit_path = os.path.join(cluster_path, "time_evolution_circuit.qasm")
        qc.qasm(filename=time_evolution_circuit_path)
        # Finished saving intermediate results

        print("Finished processing cluster {0}".format(key + 1))

    return QC

if __name__=="__main__":

    # get the command line arguments
    file, output, grouping_strategy = None, None, None
    for j in range(len(sys.argv)):
        if sys.argv[j] == "-f":
            try:
                file = sys.argv[j+1]
            except:
                print("After '-f', enter the name of the file containing the Hamiltonian")

        if sys.argv[j] == "-g":
            grouping_strategy = sys.argv[j+1]

        if sys.argv[j] == "-o":
            output = sys.argv[j+1]

    if file is None:
        print("No Hamiltonian was given")
    if output is None:
        output = file
    if grouping_strategy is None:
        grouping_strategy = "DSATUR"

    # Create folder to outoput the all the results
    results_path = "RESULTS_{0}".format(output)

    if os.path.exists(results_path):
        shutil.rmtree(results_path)
    os.mkdir(results_path)

    QC = main_compiler(file, output, grouping_strategy=grouping_strategy)
    # save QC in the result folder
    QC.qasm(filename=os.path.join(results_path, "QC.qasm"))
