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

    # (∀x p(x)) v (∃x q(x))
    x = Atom("x", False)
    P = Node("P", children=[x])
    Q = Node("Q", children=[x])
    left_or_right = Node("V", children=[Node("∀", x, children=[P]), Node("∃", x, children=[Q])])
    knowledge_base.append(left_or_right)

    # (∀x ∃y p(x,y) V q(x))
    x = Atom("x", False)
    y = Atom("y", False)
    P = Node("P", children=[x, y])
    Q = Node("Q", children=[x])
    left_or_right = Node("∧", children=[Node("∀", x, children=[Node("∃", y, children=[P])]), Q])
    knowledge_base.append(left_or_right)

    cnf_clauses = convert_to_cnf(knowledge_base)

    print("Knowledge Base:")
    for sentence in cnf_clauses:
        print("Sentence:")
        print_children(sentence)



# Run
if __name__ == "__main__":
    main()
