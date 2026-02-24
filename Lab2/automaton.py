class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.Q = set(states)
        self.Sigma = set(alphabet)
        self.delta = transitions      # (state, symbol) -> set(states)
        self.q0 = start_state
        self.F = set(final_states)
    
    def stringBelongToLanguage(self, inputString):
        current_states = {self.q0}
        for symbol in inputString:
            next_states = set()
            for state in current_states:
                key = (state, symbol)
                if key in self.delta:
                    result = self.delta[key]
                    # For NFA: result is a set of states, add all of them
                    # For DFA: result is a frozenset (single state), add as-is
                    if isinstance(result, frozenset):
                        next_states.add(result)
                    else:
                        next_states |= result
            current_states = next_states
            if not current_states:
                return False
        return len(current_states & self.F) > 0

    def is_deterministic(self):
        for key in self.delta:
            if len(self.delta[key]) > 1:
                return False
        return True

    def to_regular_grammar(self):
        from grammar import Grammar
        VN = set(self.Q)
        VT = set(self.Sigma)
        S = self.q0
        P = {}
        for (state, symbol), next_states in self.delta.items():
            for next_state in next_states:
                right = symbol + next_state

                if state not in P:
                    P[state] = []

                P[state].append(right)
        for f in self.F:
            if f not in P:
                P[f] = []
            P[f].append("")     # epsilon

        return Grammar(VN, VT, P, S)

    def to_dfa(self):

        start = frozenset({self.q0})
        dfa_states = set()
        dfa_states.add(start)
        unprocessed = [start]
        dfa_delta = {}

        while unprocessed:
            current = unprocessed.pop(0)

            for symbol in self.Sigma:
                next_set = set()

                for state in current:
                    key = (state, symbol)
                    if key in self.delta:
                        next_set |= self.delta[key]

                next_frozen = frozenset(next_set)

                dfa_delta[(current, symbol)] = next_frozen

                if next_frozen not in dfa_states:
                    dfa_states.add(next_frozen)
                    unprocessed.append(next_frozen)

        dfa_final_states = set()
        for state_set in dfa_states:
            if any(s in self.F for s in state_set):
                dfa_final_states.add(state_set)

        return FiniteAutomaton(
            states=dfa_states,
            alphabet=self.Sigma,
            transitions=dfa_delta,
            start_state=start,
            final_states=dfa_final_states
        )