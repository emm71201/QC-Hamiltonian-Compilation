from node import *

def printNode(node):
    print(node)

def remove_branch(node):

    if isinstance(node, LeafNode):
        node.remove(branch)

def getNode(node):

    return node

def detach_path(n1, n2):

    """Detach a path between node 1 and node 2 included"""
    """Assume there is a path between node 1 and node 2 """
    """Return the tree without the path and the path"""
    """The path is given by the first node """


    new_node1 = Node(n1.qbit, n1.value)
    new_node2 = Node(n2.qbit, n2.value)
    current = n2
    while current != n1:

        #print(current)

        tmp_parent = Node(current.parent.qbit, current.parent.value)
        tmp_parent.add_child(new_node2)

        new_node2 = tmp_parent
        new_current = current.parent
        new_current.remove_child(current)
        current = new_current

    return tmp_parent, n1
