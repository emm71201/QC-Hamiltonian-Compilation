#import sys
#sys.path.append("/Users/emm712/Documents/qc_construction")
#from make_gates import *
from qiskit import *
from node import *
from cnot import *
from node_actions import *

def algorithm(node, qc, n, dt):

    cxgates = []
    trgt = n
    realtrgt = n
    nodes = get_all_nodes(node)

    def traversal(node, trgt, dt, realtrgt):

        if node == None:
            return

        if node.value == 1:

            ctrl = node.qbit
            realctrl = node.realqbitposition

            if trgt < ctrl:

                CNOT(ctrl, trgt,node, nodes)
                qc.cx(realctrl, realtrgt)

                gate_str = "qc.cx({0}, {1})".format(realctrl, realtrgt)
                #cxgates.insert(0,gate_str)

                if gate_str in cxgates:
                    cxgates.remove(gate_str)
                else:
                    cxgates.insert(0,gate_str)
            else:
                trgt = ctrl
                realtrgt = realctrl

        if isinstance(node, LeafNode):

            # otherwise, the p string is the indentity
            if realtrgt != n:
                coef = (-1)**node.s * abs(node.coef)
                qc.rz(2*coef*dt, realtrgt)


        traversal(node.left, trgt, dt, realtrgt)
        traversal(node.right, trgt, dt, realtrgt)

    traversal(node, trgt, dt, realtrgt)

    for cx in cxgates:
        exec(cx)

    return qc
