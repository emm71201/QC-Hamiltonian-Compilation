from pstring import *

def pauli_to_numercal(pauli):

    """convert a Pauli string from I,X,Y,Z notation to integer notation
    For example 'IXYZ' is converted to '123' """

    res = ""
    for p in pauli:
        if p == "I":
            res += "0"
        if p == "X":
            res += "1"
        if p == "Y":
            res += "2"
        if p == "Z":
            res += "3"

    return res

def read_hamiltonian(filepath):
    """Reads the Hamiltonian
    filepath : The path to the file containing the Hamiltonian"""

    pstrings = []
    with open(filepath, "r") as f:
        for line in f:
            tmp = line.split(",")
            pauli = tmp[0]
            coef = tmp[1]
            try:
                coef = float(coef)
            except:
                print("The coefficient of the Pauli strings must be numerical.")
                print("Check the coefficients from the Hamiltonian file")
                return

            if pauli != "I"*len(pauli):
                pstrings.append(pstring(pauli_to_numercal(pauli),coef))

    return pstrings
