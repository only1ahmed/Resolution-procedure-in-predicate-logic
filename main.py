# Quantifier ( knows the variable under its tree )
# Operation
# Predicate
# Atom

class Quant:
    def __init__(self, type , var, tree = []):
        self.type = type
        self.var = var
        self.tree = tree
    
class Op:
    def __init__(self, type, tree = []):
        self.type = type
        self.tree = tree

class Pred:
    def __init__(self, name, tree = []):
        self.name = name
        self.tree = tree

class Atom:
    def __init__(self, name , is_constant = False):
        self.name = name
        self.is_constant = is_constant


def main():
    pass



# Run
if __name__ == "__main__":
    main()

