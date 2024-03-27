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
                elif branch.name == "¬":
                    branch.name = branch.children[0].children[0].name
                    branch.children = branch.children[0].children[0].children
                    branch.type = 'Pred'     
                    branch.setParent()

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
                branch.setParent()

        if type(branch) != Atom:
            move_negations_inside(branch, root)


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
        # skips the quantifier if it is already on the top
        if(cur_par == None):
            continue
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


CONSTANT_NO_NAME = 0
CONSTANT_PREDICATE = 0
# Skolemization // Quant
def skolemization(root):
    global CONSTANT_NO_NAME , CONSTANT_PREDICATE
    set_all_parents(root)
    
    list_of_atoms = []
    list_of_quantifiers = []
    
    collect_atoms(root, list_of_atoms)
    collect_quantifiers(root, list_of_quantifiers)

    list_of_atoms.sort(key=lambda atom: atom.name)
    
    universal_flag = False
    list_of_variables = set()
    # Replacing the EXIST's variables with either constants or skolem functions
    for i in range(len(list_of_quantifiers)):
        if list_of_quantifiers[i].name == "∀":
            list_of_variables.add(list_of_quantifiers[i].var.name)
            universal_flag = True
        
        if universal_flag:
            if list_of_quantifiers[i].name == "∃":
                new_atoms = []
                for atom_name in list_of_variables:
                    new_atoms.append(Atom(atom_name, False))
                    
                new_predicate = Node('F'+ str(CONSTANT_PREDICATE), children=new_atoms)
                CONSTANT_PREDICATE += 1
                root = replace_atom_with(root, list_of_quantifiers[i].var, new_predicate)

        else:
            if list_of_quantifiers[i].name == "∃":
                new_constant_atom = Atom("CONST" + str(CONSTANT_NO_NAME), True)
                CONSTANT_NO_NAME += 1
                root = replace_atom_with(root, list_of_quantifiers[i].var, new_constant_atom)

    # Deleting all EXIST Quants
    for q in list_of_quantifiers:
        if q.name == "∃":
            par = q.parent
            par.children.append(q.children[0])
            par.children.remove(q)

# Drop universal quantifiers // Quant
def drop_universal_quantifiers(root):
    if type(root) == Atom:
        return root
    if root.type == "Quant" and root.name == "∀":
        return drop_universal_quantifiers(root.children[0])
    for i in range(len(root.children)):
        root.children[i] = drop_universal_quantifiers(root.children[i])
    return root



        

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




def generate_random_string(n):
    return ''.join(random.choices(string.ascii_lowercase, k=n))


def print_children(root):
    if(root == None):
        return
    if type(root) == Atom:
        print(root.name, root.is_constant)
        return
    elif root.type == "Quant":
        print(root.name,'(', root.var.name,')')
    elif root.type == "Pred":
        print(root.name, end=" ( ")
        for branch in root.children:
            print(branch.name , end=",")
        print(' )')
    else:
        print(root.name)
    for branch in root.children:
        if type(branch) == Node:
            print_children(branch)

def convert_to_cnf(KB):
    cnf = []
    for sentence in KB:
        eliminate_implication(sentence)
        move_negations_inside(sentence)
        standardize_variables(sentence)
        sentence = move_quantifiers_left(sentence)
        skolemization(sentence)
        sentence = drop_universal_quantifiers(sentence)
        distribute(sentence)
        sentence = tree_to_clauses(sentence)
        cnf.append(sentence)
    return cnf


def tree_to_clauses(sentence):
    clauses = []
    if sentence.name == "∧":
        for child in sentence.children:
            clauses.append(child)
    else:
        clauses.append(sentence)
    
    return clauses

def resolve(clause1, clause2):
    resolved_clauses = []

    for literal1 in clause1:
        for literal2 in clause2:

            if isinstance(literal1.children[0], Atom) and isinstance(literal2.children[0], Atom):
                if literal1.name == literal2.name and literal1.is_constant != literal2.is_constant:
                    new_clause = [copy.deepcopy(lit) for lit in clause1 + clause2 if lit != literal1 and lit != literal2]
                    resolved_clauses.append(new_clause)

    return resolved_clauses

def resolution(knowledge_base):
    new_clauses = []
    for i, clause1 in enumerate(knowledge_base):
        for j, clause2 in enumerate(knowledge_base):
            if i != j:
                new_clauses.extend(resolve(clause1, clause2))
    return new_clauses