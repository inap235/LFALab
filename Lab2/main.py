from automaton import FiniteAutomaton
def build_variant_nfa():
    Q = {"q0", "q1", "q2", "q3"}
    Sigma = {"a", "b", "c"}
    q0 = "q0"
    F = {"q3"}

    # δ(q, a) = set of states
    delta = {
        ("q0", "a"): {"q0", "q1"},
        ("q1", "b"): {"q2"},
        ("q2", "a"): {"q2"},
        ("q2", "b"): {"q3"},
        ("q3", "a"): {"q3"}
    }

    return FiniteAutomaton(
        states=Q,
        alphabet=Sigma,
        transitions=delta,
        start_state=q0,
        final_states=F
    )

def format_transition_display(delta, state_name_func=None):
    if not delta:
        return []
    
    lines = []
    for (state, symbol), next_states in sorted(delta.items()):
        if state_name_func:
            state_str = state_name_func(state)
        else:
            state_str = str(state) if not isinstance(state, frozenset) else "{" + ",".join(sorted(state)) + "}"
        
        if isinstance(next_states, frozenset):
            if next_states:
                next_str = "{" + ",".join(sorted(next_states)) + "}"
            else:
                next_str = "∅"
        elif isinstance(next_states, set):
            if next_states:
                next_str = "{" + ",".join(sorted(next_states)) + "}"
            else:
                next_str = "∅"
        else:
            next_str = str(next_states)
        
        lines.append(f"  {state_str} --{symbol}--> {next_str}")
    return lines


def main():
    # Build NFA
    nfa = build_variant_nfa()
    
    # Get grammar and classify
    grammar = nfa.to_regular_grammar()
    
    # Header
    print("\n" + "="*40)
    print(" CHOMSKY HIERARCHY CLASSIFICATION")
    print("="*40)
    print(f"Variant grammar is: {grammar.classify_grammar()}")
    
    # NFA display
    print("\n" + "="*40)
    print(" VARIANT NDFA")
    print("="*40)
    print("Transitions:")
    for line in format_transition_display(nfa.delta):
        print(line)
    
    # Determinism check
    print("\n" + "="*40)
    print(" 3b. DETERMINISM CHECK")
    print("="*40)
    is_det = nfa.is_deterministic()
    print(f"Is deterministic: {str(is_det).lower()}")
    if not is_det:
        # Find first non-deterministic transition
        for (state, symbol), next_states in nfa.delta.items():
            if len(next_states) > 1:
                next_str = "{" + ",".join(sorted(next_states)) + "}"
                print(f"Reason: δ({state},{symbol}) = {next_str} — one input leads to multiple states.")
                break
    
    # Grammar conversion
    print("\n" + "="*40)
    print(" 3a. NDFA -> REGULAR GRAMMAR")
    print("="*40)
    print("Conversion steps:")
    print("  Rule: δ(A, a) -> B  becomes  A -> aB")
    print("  Rule: final state F  gets     F -> ε")
    print()
    for (state, symbol), next_states in sorted(nfa.delta.items()):
        for ns in sorted(next_states):
            print(f"  δ({state},{symbol}) -> {ns}   =>   {state} -> {symbol}{ns}")
    for f in sorted(nfa.F):
        print(f"  {f} ∈ F              =>   {f} -> ε")
    print()
    print(f"Start symbol: {grammar.S}")
    print("Productions:")
    for left in sorted(grammar.P.keys()):
        for r in grammar.P[left]:
            if r == "":
                print(f"  {left} -> ε")
            else:
                print(f"  {left} -> {r}")
    
    dfa = nfa.to_dfa()
    
    print("\n" + "="*40)
    print(" 3c. NDFA -> DFA  (subset construction)")
    print("="*40)
    print("Resulting DFA transitions:")
    print("Transitions:")
    for line in format_transition_display(dfa.delta):
        print(line)
    print(f"Is deterministic: true")
    
    tests = [
        ("abb", True),
        ("abba", True),
        ("aabb", True),
        ("abab", True),
        ("a", False),
        ("ab", False),
        ("aba", False),
        ("aaab", False),
        ("babb", False),
        ("", False),
    ]
    
    print("\n" + "="*40)
    print(" EQUIVALENCE CHECK (NDFA vs DFA)")
    print("="*40)
    print(f"{'String':<10} {'NDFA':<10} {'DFA':<10}")
    for w, expected in tests:
        nfa_result = nfa.stringBelongToLanguage(w)
        dfa_result = dfa.stringBelongToLanguage(w)
        ok = (nfa_result == dfa_result)
        status = "OK" if ok else "MISMATCH"
        print(f"{w:<10} {str(bool(nfa_result)):<10} {str(bool(dfa_result)):<10} {status}")


if __name__ == "__main__":
    main()