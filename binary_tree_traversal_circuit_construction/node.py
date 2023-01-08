# We define the node object which will be used to construct the binary tree
# For our end goal, the leaf nodes are special. So, they will be defined here by inheritance from the node class

class Node():
    """ Node class  """

    def __init__(self, qbit, realqbit, value):

        self.qbit = qbit
        self.realqbitposition = realqbit
        self.value = value
        self.parent = None
        self.left = None
        self.right = None

    def get_parent(self):

        if self.parent == None:
            return

        return self.parent

    def add_child(self, child):

        child.parent = self
        if child.value == 0:
            self.left = child
        else:
            self.right = child

    def switch_children(self):

        left = self.left
        self.left = self.right
        self.right = left

    def add_to_value(self, input):

        """this function adds input to the value.
        The addition is done modulo 2"""

        self.value = (self.value + input)%2

    def change_value(self, new_value):

        self.value = new_value


    def ancestor(self, other):
        """check if other is an ancestor of self"""

        current = self
        while current.parent != None:

            if current.parent == other:
                return True
            current = current.parent
        return False

    def descendants(self, others):
        """return the nodes from others that are descendants of self"""
        desc = []
        for node in others:
            if node.ancestor(self):
                desc.append(node)

        return desc

    def sibling(self):

        if self.value == 0:
            return self.parent.right
        else:
            return self.parent.left

    def same_parent(self, other):

        if self.parent == other.parent:
            return True
        return False

    def pivot(self, other):
        """Find the first child of self which is also parent of other or  other itself"""

        if not other.ancestor(self):

            raise Exception("The node {0} is not a child of {1}".format(other, self))

        if self == other:
            return self

        if self.left == other or self.right == other:
            return other

        current = other
        while current.parent != self:

            current = current.parent

        return current

    def remove_node(self):

        if self.left != None or self.right != None:
            raise Exception("The node {0} to remove has a child".format(self))

        elif self.parent == None:
            raise Exception("This is the root of the tree")

        else:
            if self.value == 0:
                self.parent.left = None
            else:
                self.parent.right = None

    def remove_child(self, child):
        if not (self.left == child or self.right == child):
            raise Exception("The node {0} is not a child of the node {1}".format(child, self))

        if child.value == 0:
            self.left = None
        else:
            self.right = None

    def __str__(self):
        return "qbit = {0}, value = {1}".format(self.qbit, self.value)

class LeafNode(Node):
    """ Leaf Node class inheriting from the Node super class"""

    def __init__(self, qbit, realqbit, value, s, coef):

        Node.__init__(self, qbit, realqbit, value)
        self.s = s
        self.coef = coef

    def get_paulis(self):

        #paulis = [self.value]
        paulis = []

        current = self

        while current != None:

            if current.parent != None:
                paulis.insert(0, current.value)

            current = current.parent

        return paulis

    def get_hot_node(self):

        current = self

        while current != None:

            if current.parent != None:
                #paulis.insert(0, current.value)
                if current.value == 1:
                    return current

            current = current.parent

        return



def preorder(node, action):

    if node == None:
        return

    print(action(node))
    preorder(node.left, action)
    preorder(node.right, action)
