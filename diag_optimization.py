
def cnot_basis_count(basis):

    n = len(basis)//2
    res = 0

    for j in range(n):

        if basis[j] == 1 or basis[j+n]==1:

            res += 1

    return res

def minimize_cnot(nullspace):

    basis  = nullspace[0]
    count = cnot_basis_count(basis)

    for tmp_basis in nullspace[1:]:

        tmp_count = cnot_basis_count(tmp_basis)

        if tmp_count < count:

            basis = tmp_basis
            count = tmp_count

    return basis
