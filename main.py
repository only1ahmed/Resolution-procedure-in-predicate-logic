# Quantifier ( knows the variable under its children )
# Operation
# Predicate
# Atom

from OurResolution import *

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
    
    cnf_clauses = convert_to_cnf(knowledge_base)

    print("Knowledge Base:")
    for sentence in cnf_clauses:
        print("Sentence:")
        print(len(sentence), sentence[1].name)



# Run
if __name__ == "__main__":
    main()
