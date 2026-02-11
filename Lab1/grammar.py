import random
class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S
    def generateWords(self, max_steps):
        current = self.S
        steps = 0

        while steps < max_steps:
            pos = -1
            
            for i, ch in enumerate(current):
                if ch in self.VN:
                    pos = i
                    break
            
            if pos == -1:  
                return current
            
            production = random.choice(self.P[current[pos]])
            current = current[:pos] + production + current[pos+1:]#combines the produced sequences
            steps += 1
        
        return None  
    
    def toAutomaton(self):
        from automaton import FiniteAutomaton
        states = set(self.VN)
        final_state = "X"
        states.add(final_state)
        
        alphabet = set(self.VT)
        transitions = {}
        
        for left, rights in self.P.items():
            for right in rights:
                symbol = right[0]
                # A -> aB
                if len(right)==2:
                    next_state = right[1]
                # A -> a
                elif len(right) ==1:
                    next_state = final_state
                else:
                    continue
                
                key = (left, symbol)
                if key not in transitions:
                    transitions[key] = set()

                transitions[key].add(next_state)
        
        return FiniteAutomaton(
            alphabet=alphabet,
            transitions=transitions,
            states=states,
            start=self.S,
            final={final_state}
        )
