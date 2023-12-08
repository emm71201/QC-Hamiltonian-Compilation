# Author: Edison Murairi & Michael J. Cervia
# Last edited: Nov 16th, 2023

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
from qiskit.circuit import Parameter
import numpy as np
sys.path.append("binary_tree_traversal_circuit_construction")

## Handle potentially missing dependencies.
# import subprocess
# if not "galois" in sys.modules:
#     print("Installing Galois")
#     subprocess.check_call([sys.executable, "-m", "pip", "install", "galois"])
# if not "qiskit" in sys.modules:
#     print("Installing Qiskit")
#     subprocess.check_call([sys.executable, "-m", "pip", "install", "qiskit"])
# if not "numpy" in sys.modules:
#     print("Installing Numpy")
#     subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
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
from qiskit import QuantumCircuit,qpy

def save_circuit(filename, circuit):

    with open(filename, "wb") as qpy_file_write:
        qpy.dump(circuit, qpy_file_write)

def compile_diagonal_cluster(dt, X,Z,S,Coefs, sorting= None):

    """Return the quantum circuit simulating the time evolution of diagonal pauli strings"""

    #check the pauli strings are diagonal
    if X.any():
        print("This set is not diagonal")
        return


    n = X.shape[1]
    root = load_tree(numpy.array(Z),numpy.array(S), numpy.array(Coefs), sorting=sorting)
    qc = QuantumCircuit(n)
    qc = algorithm(root, qc, n, dt)

    return qc

def tebd1(dt, cluster_QCs):
    
    QC = cluster_QCs[0]
    for section in cluster_QCs[1:]:
        QC = QC.compose(section)
    
    phi = list(cluster_QCs[0].parameters)[0]
    QC = QC.assign_parameters({phi:dt})
    
    return QC
    
def tebd2(dt, cluster_QCs):

    delta2 = Parameter('delta2')

    QC_forward = tebd1(delta2, cluster_QCs)
    QC_backward = tebd1(delta2, cluster_QCs[::-1])
    
    QC = QC_backward.compose( QC_forward )
    QC.barrier()
    
    QC.assign_parameters({delta2: dt/2},inplace=True)
    
    return QC
    
def tebd4(dt, cluster_QCs):

    deltaA = dt / (4-np.cbrt(4))
    deltaB = dt * (1-4/(4-np.cbrt(4)))

    delta4 = Parameter('delta4')
    QC_proto = tebd2(delta4, cluster_QCs)
    
    QCA = QC_proto.assign_parameters({delta4:deltaA})
    QCA.barrier()
    QCA = QCA.compose(QCA)
    
    QCB = QC_proto.assign_parameters({delta4:deltaB})
    QCB.barrier()
    
    QC = QCA.compose(QCB)
    QC = QC.compose(QCA)
    
    return QC

def tebd2N(dt, cluster_QCs, N):
    
    p = 2
    
    for m in range(1,N+1):
    
        a = np.power( (2*p), 1/(2*m+1) )
        factor = 1 / ( 2*p - a )
        deltaA = dt * factor
        deltaB = dt * ( 1 - 2 * p * factor )
        
        
        if m==1:
            delta = Parameter('delta')
            QC_proto = tebd2(delta, cluster_QCs)
        else:
            QC_proto = QC.copy()
            delta = list(QC_proto.parameters)[0]
        
        QCA = QC_proto.assign_parameters({delta:deltaA})
        QCA.barrier()
        QCAA = QCA.copy()
        for i in range(p-1):
            QCAA = QCAA.compose(QCA)
        
        QCB = QC_proto.assign_parameters({delta:deltaB})
        QCB.barrier()
        
        QC = QCAA.compose(QCB)
        QC = QC.compose(QCAA)
    
    return QC


def main_compiler(dt, file, output, grouping_strategy=None, sorting=None, tebd_order=1):

    pauli_strings = pstrs = helpers.read_hamiltonian(file)
    commuting_clusters = make_clusters(pauli_strings, strategy=grouping_strategy)
    n = len(pauli_strings[0].string)
    QC = QuantumCircuit(n)
    phi = Parameter('phi')

    ### Print a message before starting the main loop ####
    print("Number of Clusters (Sets) in which all the Pauli strings commute: {0}".format(len(commuting_clusters)))

    # Main loop: Iterate over the clusters of commuting pauli strings
    # 1. Construct a quantum circuit diagonalizing a cluster and insert the circuit into the main circuit QC
    # 2. Construct the circuit realizing the time evolution of the diagonalized cluster and insert into QC
    # 3  Insert the inverse of the diagonalizing circuit
    # 4. Take the next cluster and repeat until no cluster is left

    cluster_QCs = []
    for key in commuting_clusters:

        cluster = commuting_clusters[key]
        Coefs = numpy.array([pauli_string.coef for pauli_string in cluster])
        X,Z,S,U = diagonalize.main_diagonalizer(cluster)
        qc = compile_diagonal_cluster(phi, numpy.array(X),numpy.array(Z),numpy.array(S), Coefs, sorting= None)
        QC = U
        QC = QC.compose(qc)
        QC = QC.compose(U.inverse())
        QC.barrier()
        
        cluster_QCs.append(QC)

        # save the intermediate results
        cluster_path = os.path.join(output, "Cluster_{0}".format(key))
        os.mkdir(cluster_path)

        numpy.save(os.path.join(cluster_path, "commuting_pauli_strings.npy"), cluster)
        diagonalized_tableau_path = os.path.join(cluster_path, "diagonalized_pauli_strings_tableau.npy")
        numpy.save(diagonalized_tableau_path, {"X":X,"Z":Z,"S":S,"Coefs":Coefs})

        diagonalizing_circuit_path = os.path.join(cluster_path, "diagonalizing_circuit.qpy")
        #U.qasm(filename=diagonalizing_circuit_path)
        save_circuit(diagonalizing_circuit_path, U)

        time_evolution_circuit_path = os.path.join(cluster_path, "time_evolution_circuit.qpy")
        #qc.qasm(filename=time_evolution_circuit_path)
        save_circuit(time_evolution_circuit_path, QC)

        # Finished saving intermediate results

        print("Finished processing cluster {0}".format(key + 1))

    if tebd_order==1:
        QC = tebd1(dt, cluster_QCs)
    elif tebd_order==2:
        QC = tebd2(dt, cluster_QCs)
    elif tebd_order==4:
        QC = tebd4(dt, cluster_QCs)
    elif tebd_order>2 and tebd_order%2==0:
        iterations = tebd_order//2-1 # Number of Suzuki's fractal iterations
        QC = tebd2N(dt, cluster_QCs, iterations)
    else:
        print("TEBD at order {0} isn't supported yet. Returning the lowest-order circuit...".format(tebd_order))
        QC = tebd1(dt,cluster_QCs)

    return QC

if __name__=="__main__":

    # get the command line arguments
    file, output, grouping_strategy, dt, tebd_order = None, None, None, None, None
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

        if sys.argv[j] == "-dt":
            try:
                dt = float(sys.argv[j+1])
                print(f"dt value found = {dt}")
            except:
                print("No dt was provided. The circuit will be parametric with parameter 'dt'")
        
        if sys.argv[j] == "-tebd":
            try:
                tebd_order = int(sys.argv[j+1])
                print(f"TEBD at order {tebd_order}")
            except:
                print("A valid TEBD order wasn't specified.")
                print("The circuit will be compiled with <= second-order Trotter error")

    if file is None:
        print("No Hamiltonian was given")
    if output is None:
        output = file.split("/")
        output = output[-1].split(".")[0]
        output = "RESULTS_{0}".format(output)

    if grouping_strategy is None:
        grouping_strategy = "DSATUR"
    if dt is None:
        dt = Parameter('dt')
    if tebd_order is None:
        tebd_order = 1

    # Create folder to outoput the all the results
    #results_path = "RESULTS_{0}".format(output)
    results_path = output
    print(results_path)
    if os.path.exists(results_path):
        shutil.rmtree(results_path)
    os.mkdir(results_path)

    QC = main_compiler(dt, file, output, grouping_strategy=grouping_strategy, tebd_order=tebd_order)
    # save QC in the result folder
    save_circuit(os.path.join(results_path, "QC.qpy"), QC)
