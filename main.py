# Quantifier ( knows the variable under its children )
# Operation
# Predicate
# Atom
import random
import string
import copy


class Node:
    '''
    Types of Nodes:
    1. Quantifier
    2. Operation
    3. Predicate
    '''

    def __init__(self, name, var=None, children=[]):
        self.name = name
        self.var = var
        self.children = []
        if (len(children) != 0):
            for child in children:
                temp = child
                self.children.append(copy.deepcopy(child))
        self.parent = None
        self.type = None
        # Determine the type of the node
        if (self.name == '∀' or self.name == '∃'):
            self.type = "Quant"
        elif (self.name == '¬' or self.name == 'V' or self.name == '∧' or self.name == '→' or self.name == '↔'):
            self.type = "Op"
        else:
            self.type = "Pred"

        # Set the parent of the children
        for branch in self.children:
            branch.parent = self


class Atom:
    def __init__(self, name, is_constant=False):
        self.name = name
        self.parent = None
        self.is_constant = is_constant


# Eliminate Implication and Bi-implication //Op
def eliminate_implication(root):
    T = root.children
    # traverse the children
    for branch in T:
        if type(branch) == Node and branch.type == 'Op':
            if branch.name == "→":
                branch.name = "V"
                branch.children = [
                    Node("¬", children=[branch.children[0]]), branch.children[1]]
            elif branch.name == "↔":
                branch.name = "∧"
                branch.children = [Node("→", children=[branch.children[0], branch.children[1]]), Node(
                    "→", children=[branch.children[1], branch.children[0]])]

        if type(branch) is not Atom:
            eliminate_implication(branch)


# Move negations inside // Quant and Op
def move_negations_inside(root, parent=None):
    T = root.children
    # traverse the children
    for branch in T:
        if type(branch) == Node and branch.type == 'Op' and branch.name == "¬":

            # Operations
            if branch.children[0].type == 'Op':
                # De Morgan's Law for OR
                if branch.children[0].name == "V":
                    branch.name = "∧"
                    next_children = []
                    for b in branch.children[0].children:
                        next_children.append(Node("¬", children=[b]))
                    branch.children = next_children
                # De Morgan's Law for AND
                elif branch.children[0].name == "∧":
                    branch.name = "V"
                    next_children = []
                    for b in branch.children[0].children:
                        next_children.append(Node("¬", children=[b]))
                    branch.children = next_children
                # Double Negation
                elif branch.children[0].name == "¬":
                    branch.name = branch.children[0].children[0].name
                    branch.children = branch.children[0].children[0].children

            # Quantifier
            elif branch.children[0].type == 'Quant':
                temp_name = branch.children[0].name
                temp_children = branch.children[0].children
                temp_var = branch.children[0].var
                if (temp_name == "∀"):
                    branch.name = "∃"
                else:
                    branch.name = "∀"
                branch.var = temp_var
                branch.children = [[Node("¬", children=temp_children)]]

        if type(branch) != Atom:
            move_negations_inside(branch, branch)


# Standardize variables // Quant
def standardize_variables(root, new_atom=None, old_atom=None):
    if type(root) == Atom and new_atom != None:
        if old_atom.name == root.name:
            # Be careful of the reference here
            return new_atom
        return root
    if type(root) == Atom:
        return root

    for branch in range(len(root.children)):
        if root.type == "Quant":
            instance = Atom(generate_random_string(2), root.var.is_constant)
            root.children[branch] = standardize_variables(
                root.children[branch], instance, root.var)
            root.var = instance

        root.children[branch] = standardize_variables(
            root.children[branch], new_atom, old_atom)
    return root

# Move all quantifiers to the left // Quant


def move_quantifiers_left(root):
    T = root.children

    pass
# Skolemization // Quant


def skolemization(T):
    pass
# Drop universal quantifiers // Quant


def drop_universal_quantifiers(T, parent=None):
    # if type(T) is Quant:
    #     if T.name == "∀":
    #         T.name = ""
    #         T.var = None
    #         T.children = T.children[0]
    pass

# Convert to CNF using the distributive laws // Op


def distribute(T):
    pass


def convert_to_cnf(T):

    pass


def generate_random_string(n):
    return ''.join(random.choices(string.ascii_lowercase, k=n))


def print_children(root):
    if type(root) == Atom:
        print(root.name, root.is_constant)
        return
    elif root.type == "Quant":
        print(root.name, root.var.name)
    elif root.type == "Pred":
        print(root.name)
        for branch in root.children:
            print(branch.name)
    else:
        print(root.name)
    for branch in root.children:
        if type(branch) == Node:
            print_children(branch)


def main():
    knowledge_base = []

    # Example: ∀x(¬(T(x) → ¬M(x)))
    x = Atom("x", False)
    T = Node("T", children=[x])
    M = Node("M", children=[x])
    not_M = Node("¬", children=[M])

    T_implies_not_M = Node("→", children=[T, not_M])

    not_T_implies_not_M = Node("¬", children=[T_implies_not_M])
    first_sentence = Node("∀", x, children=[not_T_implies_not_M])
    knowledge_base.append(first_sentence)

    # (∀x p(x)) v (∃x q(x))

    x = Atom("x", False)
    y = Atom("y", False)

    P = Node("P", children=[x])
    Q = Node("Q", children=[x])
    left = Node("∀", x, children=[P])
    right = Node("∧", children=[
                 P, Node("Q", children=[y])])
    right = Node("∃", y, children=[right])
    right = Node("∃", x, children=[right])
    left_or_right = Node("V", children=[left, right])
    knowledge_base.append(left_or_right)

    # print(knowledge_base.var.name)
    # print(convert_to_cnf(knowledge_base))
    eliminate_implication(knowledge_base[1])
    move_negations_inside(knowledge_base[1])
    standardize_variables(knowledge_base[1])
    print_children(left_or_right)
    # drop_universal_quantifiers(knowledge_base[0])
    # print_children([knowledge_base[0]])
    # print_children(knowledge_base)


# Run
if __name__ == "__main__":
    main()
