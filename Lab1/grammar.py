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
        
        
