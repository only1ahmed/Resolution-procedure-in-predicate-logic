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

        self.setParent()

    def setParent(self):
        # Set the parent of the children
        for branch in self.children:
            if type(branch) == Atom:
                branch.parents.append(self)
            else:
                branch.parent = self
        


class Atom:
    def __init__(self, name, is_constant=False):
        self.name = name
        self.parents = []
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

def collect_quantifiers(root, list_of_quantifiers):
    if type(root) == Atom:
        return
    if root.type == "Quant":
        list_of_quantifiers.append(root)
    for branch in root.children:
        collect_quantifiers(branch, list_of_quantifiers)

def move_quantifiers_left(root):
    list_of_quantifiers = [] 
    collect_quantifiers(root, list_of_quantifiers)
    
    for q in list_of_quantifiers:
        cur_par = q.parent
        cur_children = q.children
        while cur_par.type == 'Quant':
            cur_par = cur_par.parent
        cur_par.children.remove(q)
        cur_par.children = cur_par.children + cur_children
    
    list_of_quantifiers.reverse()
    new_root = root
    for q in list_of_quantifiers:
        new_root = Node(q.name, q.var, [new_root])
        
    return new_root
    
def set_all_parents(root):
    if root.type == "Quant":
        root.var.parents.append(root)

    for branch in root.children:
        if type(branch) == Atom:
            branch.parents.append(root)
        else:
            branch.parent = root
            set_all_parents(branch)


def collect_atoms(root, list_of_atoms):
    if type(root) == Atom:
        list_of_atoms.append(root)
        return
    if root.type == "Quant":
        list_of_atoms.append(root.var)

    for branch in root.children:
        collect_atoms(branch, list_of_atoms)

def replace_atom_with(root, atom, constant):
    if type(root) == Atom:
        if root.name == atom.name:
            return constant
        return root
    for i in range(len(root.children)):
        root.children[i] = replace_atom_with(root.children[i], atom, constant)
    return root


# Skolemization // Quant
def skolemization(root):
    CONSTANT_NO_NAME = 0
    CONSTANT_PREDICATE = 0

    set_all_parents(root)
    
    list_of_atoms = []
    list_of_quantifiers = []
    
    collect_atoms(root, list_of_atoms)
    collect_quantifiers(root, list_of_quantifiers)

    list_of_atoms.sort(key=lambda atom: atom.name)
    
    universal_flag = False
    list_of_variables = set()
    for i in range(len(list_of_quantifiers)):
        if list_of_quantifiers[i].name == "∀":
            list_of_variables.add(list_of_quantifiers[i].var.name)
            universal_flag = True
        
        if universal_flag:
            if list_of_quantifiers[i].name == "∃":
                new_atoms = []
                for atom in list_of_atoms:
                    if atom.name not in list_of_variables:
                        new_atoms.append(Atom(atom.name, False))
                new_predicate = Node('F'+ str(CONSTANT_PREDICATE), children=new_atoms)
                CONSTANT_PREDICATE += 1
                root = replace_atom_with(root, list_of_quantifiers[i].var, new_predicate)

        else:
            if list_of_quantifiers[i].name == "∃":
                new_constant_atom = Atom("CONST" + str(CONSTANT_NO_NAME), True)
                CONSTANT_NO_NAME += 1
                root = replace_atom_with(root, list_of_quantifiers[i].var, new_constant_atom)


# Drop universal quantifiers // Quant


def drop_universal_quantifiers(root, parent=None):
    # if type(T) is Quant:
    #     if T.name == "∀":
    #         T.name = ""
    #         T.var = None
    #         T.children = T.children[0]
    pass

# Convert to CNF using the distributive laws // Op


def distribute(root):
    if type(root) == Atom:
        return
    if root.name == 'V':
        for i in range(len(root.children)):
            if root.children[i].name == '∧':
                temp = copy.deepcopy(root.children)
                root.name = '∧'
                root.children[0] = Node(
                    "V", children=[temp[(i + 1) % 2], temp[i].children[0]])
                root.children[1] = Node(
                    "V", children=[temp[(i + 1) % 2], temp[i].children[1]])
                break
        for child in root.children:
            distribute(child)


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
        print(root.name, end=" ")
        for branch in root.children:
            print(branch.name , end=" ")
        print()
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
    P = Node("P", children=[x])
    Q = Node("Q", children=[x])

    left_or_right = Node("V", children=[Node("∀", x, children=[P]), Node("∃", x, children=[Q])])

    
    knowledge_base.append(left_or_right)

    # print(knowledge_base.var.name)
    # print(convert_to_cnf(knowledge_base))
    eliminate_implication(knowledge_base[1])
    move_negations_inside(knowledge_base[1])
    standardize_variables(knowledge_base[1])
    knowledge_base[1] = move_quantifiers_left(knowledge_base[1])
    skolemization(knowledge_base[1])
    print_children(knowledge_base[1])



# Run
if __name__ == "__main__":
    main()
