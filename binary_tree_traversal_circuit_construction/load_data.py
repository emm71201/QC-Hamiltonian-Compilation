from node import *
from cnot import *
from numpy import *
import random
import copy
#from treelib import *

def load_branch(root, branch, s, coef, sorting=None):

    n = len(branch)
    j = 0
    parent = root

    if sorting != None:
        zipped = zip(sorting, branch)
        zpsorted = sorted(zipped)
        branch = array([x[1] for x in zpsorted])
        sortingSorted = [x[0] for x in zpsorted]

    while j < n:

        val = branch[j]

        if sorting != None:
            realqbit = sorting.index(sortingSorted[j])
        else:
            realqbit = j

        if j == n-1:
            if val == 0:
                if parent.left != None:
                    pass
                else:
                    parent.add_child(LeafNode(j,realqbit,val,s, coef))

                parent = parent.left

            else:
                if parent.right != None:
                    pass
                else:
                    parent.add_child(LeafNode(j,realqbit, val,s, coef))

                parent = parent.right
            j += 1

        else:
            if val == 0:
                if parent.left != None:
                    pass
                else:
                    parent.add_child(Node(j,realqbit,val))

                parent = parent.left

            else:
                if parent.right != None:
                    pass
                else:
                    parent.add_child(Node(j,realqbit, val))

                parent = parent.right
            j += 1

def load_tree(Z,S, Coefs, sorting=None):

    root = Node(None, None, None)

    for j in range(len(Z)):
        branch = Z[j]
        s = S[j]
        coef = Coefs[j]
        load_branch(root, branch,s, coef, sorting)

    return root

def tree_to_tableau(root):
    """get the tableau from the normal ordered tree """
    signs = []
    coefs = []
    z = []
    def trvrs(node, z, signs, coefs):
        if node == None:
            return

        if isinstance(node, LeafNode):
            z.append(node.get_paulis())
            signs.append(node.s)
            coefs.append(node.coef)

        trvrs(node.left, z, signs, coefs)
        trvrs(node.right, z, signs, coefs)
    trvrs(root, z, signs, coefs)
    z = array(z)
    signs = array(signs)
    coefs = array(coefs)

    return z,signs, coefs


def zscoresort(z):

    """ return the tree where the bits have been sorted according the zscore"""

    scores = z.sum(axis = 0)

    # decouple the identical entries in scores
    rd = linspace(0, 0.5, len(scores))

    scores = scores  + rd
    return scores

# def msb_sort(z):
#
#     """return the sorting according to the msb"""
#     msb_zero_score = []
#     #ztmp = copy.deepcopy(z)
#     n = len(z[0])
#     for ind in range(n):
#         cols = list(range(ind)) + list(range(ind+1,n))
#         tmp = z[:,cols]
#         msb_zero_score.append(count_nonzero(tmp==0))
#
#
#     return msb_zero_score + linspace(0, 0.5, len(msb_zero_score))

def sortqbit(root, srtarr):

    """ return the tree where the bits have been sorted according the sortarr"""
    z, signs, coefs = tree_to_tableau(root)

    labls = list(range(len(z[0])))
    labls_sorted = [x for _,x in sorted(zip(srtarr,labls))]

    zsorted = z[:, labls_sorted]
    newroot = load_tree(zsorted, signs, coefs)

    ## now I need to set the realqbitposition
    def trvrs(node):
        if node ==None:
            return
        if node.qbit != None:
            node.realqbitposition = labls_sorted[node.qbit]
        trvrs(node.left)
        trvrs(node.right)
    trvrs(newroot)

    return newroot
