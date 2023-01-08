
# Author: Eidson Murairi
# Date: January 4th, 2023

# Implement the Hamiltonian diagonalization algorithm developed by the authors
# The Hamiltonian is represented as a linear combination of Pauli operators (Pauli strings)
# We are given commuting Pauli operstors to diagonalize
# We represent the Paulis in Tableau
# We select the independent Pauli strings
# A basis that diagonalizes the independent Pauli strings also diagonalizes the whole set of commuting strings
# The columns of the tableau for independent commuting Pauli strings are linearly dependent.
# Therefore, the tableau for commuting Pauli strings has a non-trivial null space.
# We use the basis of the null space as instructions for diagonalization.
# See the paper for more details.

from tableau import *
from tableau_operations import *
import copy as cp

def mask_column(x,z,col, qmap):

    """This function mask a column, meaning that we will not consider such a column
    during the diagonalization.
    We will use it to mask columns that are already diagonal """
    n = x.shape[1]

    #update qmap
    for c in range(col, n-1):

        qmap[c] = qmap[c+1]
    del qmap[n-1]

    x = numpy.delete(x, col, 1)
    z = numpy.delete(z, col, 1)
    ind_pstrings = getIndependentPauliStrings(x,z)
    x,z,_,_ = tableau(ind_pstrings)

    return x,z,qmap

def mask_diagonal_columns(x,z,qmap):

    """This function finds all the columns that are already diagonal and mask them """

    n = x.shape[1]
    col = 0
    while col < n:

        if not x[:,col].any():

            x,z,qmap = mask_column(x,z,col,qmap)
            col -= 1
            n -= 1

        col += 1

    return x,z,qmap

def choose_basis_vector(nullspace):

    """We pick one of the basis vectors of the null space """
    """We will use this basis to diagonalize one of the columns """

    min_weight = min(numpy.count_nonzero(numpy.array(nullspace), axis=1))

    for basis in nullspace:

        if numpy.count_nonzero(numpy.array(basis)) == min_weight:

            return basis

    #we should never get here
    return

def reduce_column(basis, qmap, x,z, X,Z,S,U):

    """We use the basis vector to diagonalize one column """


    ntmp = len(basis)//2
    u = QuantumCircuit(ntmp)
    s = GF(numpy.zeros(x.shape[0], dtype=int))

    pivots = []
    for j in range(ntmp):

        a = basis[j]
        b = basis[j + ntmp]
        if a == 1 or b == 1:

            pivots.append(j)

        if a == 0 and b == 1:

            # apply h gate on the main circuit
            X,Z,S,U = hgate(X,Z,S,U, qmap[j])

            # apply h gate on the dummy circuit
            x,z,s,u = hgate(x,z,s,u, j)

        if a == 1 and b == 1:

            # apply s and h on the main circuit
            X,Z,S,U = sgate(X,Z,S,U, qmap[j])
            X,Z,S,U = hgate(X,Z,S,U, qmap[j])

            # apply s and h on the dummy circuit
            x,z,s,u = sgate(x,z,s,u, j)
            x,z,s,u = hgate(x,z,s,u, j)

    # now, if pivots has only one entry, we don't need to apply cnot gates and we can exit.
    # the pivots[0]-th column of x is already Zero
    if len(pivots) == 1:
        return X,Z,S,U, x,z, pivots[0]

    # otherwise, we should go perform cnot gates. We choose that it is the column pivots[0]
    # that we will diagonalize

    p1 = pivots[0]
    for p2 in pivots[1:]:

        # cnot on the main circuit
        X,Z,S,U = cxgate(X,Z,S,U, qmap[p2], qmap[p1])

        # cnot on the dummy citcuit
        x,z,s,u = cxgate(x,z,s,u, p2,p1)

    return X,Z,S,U, x,z, pivots[0]

def main_diagonalizer(pstrings):

    """This is the main diagonalization loop """

    X,Z,S,Coefs = tableau(pstrings)
    # check that the dimensions are right
    assert X.shape == Z.shape
    assert S.shape == Coefs.shape
    assert X.shape[0] == S.shape[0]

    # initialize
    n = X.shape[1]
    U = QuantumCircuit(n)
    qmap = {j:j for j in range(n)}

    if not X.any():
        return X,Z,S,U

    x = cp.deepcopy(X)
    z = cp.deepcopy(Z)
    x,z, qmap = mask_diagonal_columns(x,z,qmap)

    # start the loop
    for bb in range(n):

        # if there is only one column (qubit), I should diagonalize immediately
        if x.shape[1] == 1:

            if x[:,0].any():

                if not z[:,0].any():

                    # x is 1 and z is 0 ---> The pauli matrix is X
                    X,Z,S,U = hgate(X,Z,S,U, qmap[0])

                else:
                    # x is 1 and z is 1 ---> The pauli matrix is Y
                    X,Z,S,U = sgate(X,Z,S,U, qmap[0])
                    X,Z,S,U = hgate(X,Z,S,U, qmap[0])

            return X,Z,S,U


        nullspace = makeTableauMatrix(x,z).null_space()
        basis = choose_basis_vector(nullspace)
        X,Z,S,U, x,z, pivot = reduce_column(basis, qmap, x,z, X,Z,S,U)
        x,z,qmap = mask_column(x,z,pivot,qmap)


    return X, Z, S, U
