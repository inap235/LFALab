class FiniteAutomaton:
    def __init__(self, alphabet, transitions, states, start , final):
        self.alphabet = alphabet
        self.transitions = transitions  
        self.states = states
        self.start = start
        self.final = final
        
        