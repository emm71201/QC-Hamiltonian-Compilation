# We implement the cnot tableau operation on the binary tree
"""Because the binary tree compression assumes all the paulis are diagonal,
the X block of the tableau is assumed to be 0. Then, the only action of the
CNOT(a,b) is Z[i,a] = (Z[i,a] + Z[i,b]) % 2
a is the control qubit, and b is the target """

from node import *
from node_actions import *

def remove_sublist(lst, sublst):

    for item in sublst:
        if item in lst:
            lst.remove(item)

    return lst

def get_all_nodes(root):

    nodes = []

    def traversal(root):

        if root == None:
            return
        #print(root)
        nodes.append(root)
        traversal(root.left)
        traversal(root.right)

    traversal(root)

    return nodes


def get_level_nodes(all_nodes, level):

    """Helper function. This function returns all the nodes at a given level"""
    """arguments: all_nodes, level"""

    result = []

    for node in all_nodes:
        if node.qbit == level:
            result.append(node)

    return result


def CNOT(a,b, root, all_nodes):

    """CNOT tableau operation with control qubit a, and target b implemented on
    the binary tree data structure"""
    """we assume a > b """

    nodes_a = get_level_nodes(all_nodes, a)
    nodes_b = get_level_nodes(all_nodes, b)

    # update
    for nb in nodes_b:
        if nb.value == 0:
            pass
        else:

            desc = nb.descendants(nodes_a)

            processed = []

            for node in desc:
                if node in processed:
                    pass
                else:
                    parent = node.parent
                    sibling = node.sibling()

                    node.add_to_value(1)
                    if sibling != None:
                        sibling.add_to_value(1)

                    parent.switch_children()

                    processed.append(node)
                    processed.append(sibling)

def CNOT_v2(a,b, root, all_nodes):

    """CNOT tableau operation with control qubit a, and target b implemented on
    the binary tree data structure"""
    """we assume that a < b """

    # print("Before\n")
    # preorder(root, printNode)
    # print("\n")

    controllers = get_level_nodes(all_nodes, a)
    targets = get_level_nodes(all_nodes, b)

    # update
    for target in targets:
        if target.value == 0:
            pass

        else:

            controller = None
            for ctrl in controllers:
                if target.ancestor(ctrl):
                    controller = ctrl
                    print("The controller of {0} is {1}".format(target, controller))

            pivot = controller.pivot(target)
            pivot_gd_parent = pivot.parent.parent

            new_pivot_parent = Node(controller.qbit, 0)
            new_pivot_parent.add_child(pivot)
            pivot_gd_parent.add_child(new_pivot_parent)

            controller.remove_child(pivot)

    # print("After\n")
    # preorder(root, printNode)
