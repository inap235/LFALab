import random
class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = VN 
        self.VT = VT
        self.P = P #productions list
        self.S = S #start symbol
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
    def classify_grammar(self):
        """
        Returns the Chomsky type:
        Type 3  Regular
        Type 2 Context-Free
        Type 1  Context-Sensitive
        Type 0 Unrestricted
        """
        is_regular = True
        for left, rights in self.P.items():
            if left not in self.VN:
                is_regular = False
                break

            for right in rights:
                if right == "":
                    continue

                # Try to match: one terminal followed by an optional non-terminal
                # Find the terminal prefix (first char(s) that form a terminal)
                terminal = None
                for t in sorted(self.VT, key=len, reverse=True):
                    if right.startswith(t):
                        terminal = t
                        break

                if terminal is None:
                    # right doesn't start with a terminal
                    is_regular = False
                    break

                rest = right[len(terminal):]

                if rest == "":
                    # A -> a  (terminal only)
                    pass
                elif rest in self.VN:
                    # A -> aB (terminal + non-terminal)
                    pass
                else:
                    is_regular = False
                    break

            if not is_regular:
                break

        if is_regular:
            return "Type 3 – Regular grammar"

        #Type 2
        is_cfl = True
        for left in self.P.keys():
            if left not in self.VN:
                is_cfl = False
                break

        if is_cfl:
            return "Type 2 – Context-Free grammar"

        #Type 1
        is_csl = True

        for left, rights in self.P.items():
            for right in rights:
                if len(right) < len(left):
                    is_csl = False
                    break
            if not is_csl:
                break

        if is_csl:
            return "Type 1 – Context-Sensitive grammar"

        return "Type 0 – Unrestricted grammar"
