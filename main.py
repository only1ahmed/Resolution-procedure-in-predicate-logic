# Quantifier ( knows the variable under its tree )
# Operation
# Predicate
# Atom

class Quant:
    def __init__(self, name , var, tree = []):
        self.name = name
        self.var = var
        self.tree = tree
    
class Op:
    def __init__(self, name , var = None, tree = []):
        self.name = name
        self.var = var
        self.tree = tree

class Pred:
    def __init__(self, name , var = None, tree = []):
        self.name = name
        self.var = var
        self.tree = tree

class Atom:
    def __init__(self, name , is_constant = False):
        self.name = name
        self.is_constant = is_constant


# Eliminate Implication and Bi-implication //Op
def eliminate_implication(T):
    # traverse the tree
    for branch in T:
        if type(branch) is Op:
            if branch.name == "→":
                branch.name = "∨"
                branch.tree = [Op("¬",tree = [branch.tree[0]]),branch.tree[1]]
            elif branch.name == "↔":
                branch.name = "∧"
                branch.tree = [Op("→",tree = [branch.tree[0],branch.tree[1]]),Op("→",tree = [branch.tree[1],branch.tree[0]])]
        
        if type(branch) is not Atom:
            eliminate_implication(branch.tree)


# Move negations inside // Quant and Op
def move_negations_inside(T, parent = None):
    # traverse the tree
    for branch in T:
        if type(branch) is Op and branch.name == "¬":

            # Operations
            if type(branch.tree[0]) is Op:
                # De Morgan's Law for OR
                if branch.tree[0].name == "∨":
                    branch.name = "∧"
                    next_tree = []
                    for b in branch.tree[0].tree:
                        next_tree.append(Op("¬",tree = [b]))
                    branch.tree = next_tree
                # De Morgan's Law for AND
                elif branch.tree[0].name == "∧":
                    branch.name = "∨"
                    next_tree = []
                    for b in branch.tree[0].tree:
                        next_tree.append(Op("¬",tree = [b]))
                    branch.tree = next_tree
                # Double Negation
                elif branch.tree[0].name == "¬":
                    branch.name = branch.tree[0].tree[0].name
                    branch.tree = branch.tree[0].tree[0].tree
            
            # Quantifier
            elif type(branch.tree[0]) is Quant:
                temp_name = branch.tree[0].name
                temp_tree = branch.tree[0].tree 
                temp_var = branch.tree[0].var
                if(temp_name == "∀"):
                    branch.name = "∃"
                else:
                    branch.name = "∀"
                branch.var = temp_var
                branch.tree = [[Op("¬",tree = temp_tree)]]

        if type(branch) is not Atom:
            move_negations_inside(branch.tree,branch)


# Standardize variables // Quant
def standardize_variables(T):
    pass
# Move all quantifiers to the left // Quant
def move_quantifiers_left(T):
    pass
# Skolemization // Quant
def skolemization(T):
    pass
# Drop universal quantifiers // Quant
def drop_universal_quantifiers(T):
    pass
# Convert to CNF using the distributive laws // Op
def distribute(T):
    pass

def convert_to_cnf(tree):
    
    pass


def print_tree(tree):
    for branch in tree:
        if type(branch) is Atom:
            print(branch.name , branch.is_constant)
        elif type(branch) is Op:
            print(branch.name)
            print_tree(branch.tree)
        elif type(branch) is Quant:
            print(branch.name, branch.var.name)
            print_tree(branch.tree)
        elif type(branch) is Pred:
            print(branch.name)
            print_tree(branch.tree)

def main():
    all_tree = []

    # Example: ∀x(¬(T(x) → ¬M(x)))
    x = Atom("x",False)
    T = Pred("T",tree = [x])
    M = Pred("M",tree = [x])
    not_M = Op("¬",tree = [M])
    
    T_implies_not_M = Op("→",tree = [T,not_M])
    
    not_T_implies_not_M = Op("¬",tree = [T_implies_not_M])
    all_tree.append(Quant("∀",x, tree = [not_T_implies_not_M]))
    
    # print(all_tree.var.name)
    # print(convert_to_cnf(all_tree))
    eliminate_implication(all_tree[0].tree)
    move_negations_inside(all_tree[0].tree)
    print_tree([all_tree[0]])
    # print_tree(all_tree)




# Run
if __name__ == "__main__":
    main()

