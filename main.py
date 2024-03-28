# Quantifier ( knows the variable under its children )
# Operation
# Predicate
# Atom

from OurResolution import *

def main():
    knowledge_base = []


    # 1. ∀x graduating(x) =⇒ happy(x)
    x = Atom("x", False)
    graduating = Node("graduating", children=[x])
    happy = Node("happy", children=[x])
    graduating_implies_happy = Node("→", children=[graduating, happy])
    first_sentence = Node("∀", x, children=[graduating_implies_happy])
    knowledge_base.append(first_sentence)
    # 2. ∀x happy(x) =⇒ smiling(x)
    x = Atom("x", False)
    happy = Node("happy", children=[x])
    smiling = Node("smiling", children=[x])
    happy_implies_smiling = Node("→", children=[happy, smiling])
    second_sentence = Node("∀", x, children=[happy_implies_smiling])
    knowledge_base.append(second_sentence)
    # 3. graduating(JohnDoe)
    john_doe = Atom("JohnDoe", True)
    graduating = Node("graduating", children=[john_doe])
    third_sentence = graduating
    knowledge_base.append(third_sentence)
    # Assumption ¬smiling(JohnDoe)
    smiling = Node("smiling", children=[john_doe])
    assumption = Node("¬", children=[smiling])
    knowledge_base.append(assumption)

    cnf_clauses = convert_to_cnf(knowledge_base)
    print("CNF Clauses:")
    for clause in cnf_clauses:
        print("================")
        print_clause(clause)


    print("Resolution:")
    print(resolution(cnf_clauses))




# Run
if __name__ == "__main__":
    main()
