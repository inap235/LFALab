from grammar import Grammar
def build_grammar() -> Grammar:
    VN = {"S", "A", "B", "C", "D"}
    VT = {"a", "b"}
    P = {
        "S": ["a B", "b A", "B"],
        "A": ["b", "a D", "A S", "b A B", "ε"],
        "B": ["a", "b S"],
        "C": ["A B"],
        "D": ["B B"],
    }
    return Grammar.from_dict(VN, VT, P, start_symbol="S")
def print_stage(title: str, grammar: Grammar) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    print(grammar.pretty())


def main() -> None:
    print("=" * 80)
    print("Lab 5 - Chomsky Normal Form (Variant 18)")
    print("=" * 80)

    g0 = build_grammar()
    print_stage("Initial grammar", g0)

    g1 = g0.eliminate_epsilon_productions()
    print_stage("1) After epsilon-production elimination", g1)

    g2 = g1.eliminate_unit_productions()
    print_stage("2) After renaming (unit-production) elimination", g2)

    g3 = g2.eliminate_inaccessible_symbols()
    print_stage("3) After inaccessible-symbol elimination", g3)

    g4 = g3.eliminate_nonproductive_symbols()
    print_stage("4) After nonproductive-symbol elimination", g4)

    g5 = g4.to_cnf()
    print_stage("5) Chomsky Normal Form", g5)

    print("\nFinal verification")
    print("CNF valid:", g5.is_cnf())


if __name__ == "__main__":
    main()
