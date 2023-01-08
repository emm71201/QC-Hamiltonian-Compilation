## diagonalizer in Kawase
from pstring import *
from tableau import *
from tableau_operations import *
from qiskit import *
import copy as cp

def maximize_rank_of_x(x,z,s,u):

    assert x.shape == z.shape
    assert x.shape[0] == s.shape[0]

    r = rank(x)
    numrows, numcols = x.shape

    for bit in range(numcols):

        xtmp, ztmp, stmp, utmp = cp.deepcopy(x), cp.deepcopy(z), cp.deepcopy(s), cp.deepcopy(u)

        xtmp, ztmp, stmp, utmp = hgate(xtmp, ztmp, stmp, utmp, bit)

        rprime = rank(xtmp)

        if r < rprime:

            x,z,s = cp.deepcopy(xtmp), cp.deepcopy(ztmp), cp.deepcopy(stmp)
            u.h(bit)
            r = rprime

    return x,z,s,u

def zero_out_upper_xblock(x,z,s,u):

    assert x.shape == z.shape
    assert x.shape[0] == s.shape[0]

    numrows, numcols = x.shape

    for i in range(numcols):

        try:
            if x[i,i] == 0:

                for j in range(i+1, numrows):

                    try:
                        if x[j,i] == 1:

                            x,z,s = swaprows(x,z,s,j,i)
                    except:
                        pass
        except:
            pass


        for j in range(i+1, numcols):

            try:
                if x[i,j] == 1:

                    x,z,s,u = cxgate(x,z,s,u,i,j)
            except:
                pass

    return x,z,s,u

def zero_out_zblock(x,z,s,u):

    assert x.shape == z.shape
    assert x.shape[0] == s.shape[0]

    numrows, numcols = x.shape

    for i in range(min(numrows,numcols)):

        for j in range(min(numrows,numcols)):

            try:
                if z[i,j] == 1 and i != j:

                    x,z,s,u = czgate(x,z,s,u,i,j)
            except:
                pass
        try:
            if z[i,i] == 1:

                x,z,s,u = sgate(x,z,s,u,i)
        except:
            pass

    return x,z,s,u

def switch_x_z(x,z,s,u):

    assert x.shape == z.shape
    assert x.shape[0] == s.shape[0]
    numrows, numcols = x.shape

    for bit in range(numcols):

        if any(x[:,bit]):

            x,z,s,u = hgate(x,z,s,u, bit)

    return x,z,s,u

def diagonalize(pstrings):

    x,z,s,coefs= tableau(pstrings)

    assert x.shape == z.shape
    assert x.shape[0] == s.shape[0]
    u = QuantumCircuit(x.shape[1])

    x,z,s,u = maximize_rank_of_x(x,z,s,u)
    u.barrier()
    x,z,s,u = zero_out_upper_xblock(x,z,s,u)
    u.barrier()
    x,z,s,u = zero_out_zblock(x,z,s,u)
    u.barrier()
    x,z,s,u = switch_x_z(x,z,s,u)

    return x,z,s,u

# pstrs = [pstring("2010",1), pstring("0102",1), pstring("1323",1), pstring("2313",1), pstring("1020",1), pstring("0201",1), pstring("3132",1),pstring("3231",1)]
# x,z,s,coefs = tableau(pstrs)
# u = QuantumCircuit(4)
