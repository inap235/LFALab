import random
class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = VN
        self.VT = VT
        self.P = P
        self.S = S
    def generateWords (self , max):
        current = self.S
        steps = 0

        pos = -1
        symbol = None

        while steps < max:
            for i, ch in enumerate(current):
                if ch in self.VN:
                    pos = i #looks for the nonterminal symbol and its pos
                    symbol = ch
                    break

            if pos == -1:
                break
            
        production = random.choice(self.P[symbol])
        current = current[:pos] + production + current[pos+1:] #replaces the nonterminal sign to the production
        
        steps +=1 
        
        for ch in current:
           if any(ch in self.VN):
               return None
        return current
    
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
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            start_state=self.S,
            final_states={final_state}
        )
