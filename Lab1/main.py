from grammar import Grammar
def main():
    VN = {"S", "A", "B", "C"}
    VT = {"a", "b"}
    P = {
        "S": ["aA", "aB"],
        "A": ["bS"],
        "B": ["aC"],
        "C": ["a", "bS"]
    }
    S = "S"
    grammar = Grammar(VN, VT, P, S)
    print("Generated strings:")
    generated = []
    while len(generated) < 5:
        w = grammar.generateWords(20)
        if w is not None:
            generated.append(w)

    for w in generated:
        print(w)
    automaton = grammar.toAutomaton()

    print("\nTesting generated strings:")
# Test with strings NOT in the language
    test_strings = [
    "b",        # Starts with b (grammar requires 'a')
    "ab",       # Invalid pattern
    "ba",       # Invalid pattern
    "aababaaa"  # Valid (already generated)
]

    for w in test_strings:
        print(w, "->", automaton.stringBelongToLanguage(w))
    """for w in generated:
        print(w, "->", automaton.stringBelongToLanguage(w))
"""

if __name__ == "__main__":
    main()
