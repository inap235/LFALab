class FiniteAutomaton:
    def __init__(self, alphabet, transitions, states, start , final):
        self.alphabet = alphabet
        self.transitions = transitions  
        self.states = states
        self.start = start
        self.final = final
        
    def stringBelongToLanguage(self, inputString):
        current_states = {self.start}
        
        for symbol in inputString:
            next_states = set()
            
            for state in current_states:
                key = (state, symbol)
                if key in self.transitions:
                    next_states |= self.transitions[key]
                    
            current_states = next_states
            
            if not current_states:
                return False
            
        return bool(current_states & self.final)
                
        