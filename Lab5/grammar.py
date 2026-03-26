from itertools import combinations

EPSILON = "ε"
class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = set(VN)
        self.VT = set(VT)
        self.P = {left: set(rights) for left, rights in P.items()}
        self.S = S

    @staticmethod
    def from_dict(VN, VT, productions, start_symbol):
        parsed = {nt: set() for nt in VN}

        for left, rights in productions.items():
            parsed.setdefault(left, set())
            for right in rights:
                right = right.strip()
                if right in {"", EPSILON}:
                    parsed[left].add(())
                    continue

                symbols = tuple(right.split())
                if len(symbols) == 1 and symbols[0] == right and " " not in right:
                    # scrings going backward like aB or AB
                    symbols = tuple(right)
                parsed[left].add(symbols)

        return Grammar(set(VN), set(VT), parsed, start_symbol)

    def clone(self):
        return Grammar(
            VN=set(self.VN),
            VT=set(self.VT),
            P={left: set(rights) for left, rights in self.P.items()},
            S=self.S,
        )

    def _fresh_nonterminal(self, prefix="X"):
        index = 1
        while True:
            candidate = f"{prefix}{index}"
            if candidate not in self.VN and candidate not in self.VT:
                return candidate
            index += 1

    def _is_unit_rule(self, rhs):
        return len(rhs) == 1 and rhs[0] in self.VN

    def format_production(self, rhs):
        if len(rhs) == 0:
            return EPSILON
        return " ".join(rhs)

    def pretty(self):
        lines = []
        lines.append(f"VN = {{{', '.join(sorted(self.VN))}}}")
        lines.append(f"VT = {{{', '.join(sorted(self.VT))}}}")
        lines.append(f"S = {self.S}")
        lines.append("P:")

        production_index = 1
        for left in sorted(self.P):
            for rhs in sorted(self.P[left]):
                lines.append(
                    f"  {production_index:2d}. {left} -> {self.format_production(rhs)}"
                )
                production_index += 1

        return "\n".join(lines)

    def nullable_nonterminals(self):
        nullable = set()
        changed = True

        while changed:
            changed = False
            for left, rights in self.P.items():
                for rhs in rights:
                    if len(rhs) == 0 or all(symbol in nullable for symbol in rhs):
                        if left not in nullable:
                            nullable.add(left)
                            changed = True

        return nullable

    def eliminate_epsilon_productions(self):
        g = self.clone()
        nullable = g.nullable_nonterminals()

        new_productions = {left: set() for left in g.VN}

        for left, rights in g.P.items():
            for rhs in rights:
                if len(rhs) == 0:
                    continue

                new_productions[left].add(rhs)
                nullable_positions = [i for i, symbol in enumerate(rhs) if symbol in nullable]

                for count in range(1, len(nullable_positions) + 1):
                    for removed in combinations(nullable_positions, count):
                        removed_set = set(removed)
                        candidate = tuple(
                            symbol for i, symbol in enumerate(rhs) if i not in removed_set
                        )
                        if candidate:
                            new_productions[left].add(candidate)

        if g.S in nullable:
            new_productions[g.S].add(())

        g.P = new_productions
        return g

    def eliminate_unit_productions(self):
        g = self.clone()
        unit_closure = {}

        for nt in g.VN:
            closure = {nt}
            stack = [nt]
            while stack:
                current = stack.pop()
                for rhs in g.P.get(current, set()):
                    if self._is_unit_rule(rhs) and rhs[0] not in closure:
                        closure.add(rhs[0])
                        stack.append(rhs[0])
            unit_closure[nt] = closure

        rebuilt = {nt: set() for nt in g.VN}

        for left in g.VN:
            for reachable in unit_closure[left]:
                for rhs in g.P.get(reachable, set()):
                    if self._is_unit_rule(rhs):
                        continue
                    rebuilt[left].add(rhs)

        g.P = rebuilt
        return g

    def eliminate_inaccessible_symbols(self):
        g = self.clone()
        reachable = {g.S}
        queue = [g.S]

        while queue:
            left = queue.pop(0)
            for rhs in g.P.get(left, set()):
                for symbol in rhs:
                    if symbol in g.VN and symbol not in reachable:
                        reachable.add(symbol)
                        queue.append(symbol)

        g.VN = reachable
        g.P = {left: set(rights) for left, rights in g.P.items() if left in g.VN}

        return g

    def eliminate_nonproductive_symbols(self):
        g = self.clone()
        productive = set()

        changed = True
        while changed:
            changed = False
            for left, rights in g.P.items():
                for rhs in rights:
                    if all(
                        (symbol in g.VT)
                        or (symbol in productive)
                        for symbol in rhs
                    ):
                        if left not in productive:
                            productive.add(left)
                            changed = True

        g.VN = {nt for nt in g.VN if nt in productive}

        filtered = {nt: set() for nt in g.VN}
        for left in g.VN:
            for rhs in g.P.get(left, set()):
                if all(
                    (symbol in g.VT)
                    or (symbol in g.VN)
                    for symbol in rhs
                ):
                    filtered[left].add(rhs)

        g.P = filtered
        return g

    def to_cnf(self):
        g = self.clone()

        terminal_map = {}
        replaced = {left: set() for left in g.VN}

        for left, rights in g.P.items():
            for rhs in rights:
                if len(rhs) <= 1:
                    replaced[left].add(rhs)
                    continue

                replaced_rhs = []
                for symbol in rhs:
                    if symbol in g.VT:
                        if symbol not in terminal_map:
                            new_nt = g._fresh_nonterminal(prefix="T")
                            g.VN.add(new_nt)
                            replaced.setdefault(new_nt, set())
                            replaced[new_nt].add((symbol,))
                            terminal_map[symbol] = new_nt
                        replaced_rhs.append(terminal_map[symbol])
                    else:
                        replaced_rhs.append(symbol)

                replaced[left].add(tuple(replaced_rhs))

        g.P = replaced

        final_productions = {left: set() for left in g.VN}

        for left, rights in g.P.items():
            for rhs in rights:
                if len(rhs) <= 2:
                    final_productions[left].add(rhs)
                    continue

                chain = list(rhs)
                current_left = left
                while len(chain) > 2:
                    fresh = g._fresh_nonterminal(prefix="X")
                    g.VN.add(fresh)
                    final_productions.setdefault(fresh, set())
                    final_productions[current_left].add((chain[0], fresh))
                    current_left = fresh
                    chain = chain[1:]

                final_productions[current_left].add(tuple(chain))

        g.P = {left: rights for left, rights in final_productions.items() if rights}
        return g

    def is_cnf(self):
        for left, rights in self.P.items():
            if left not in self.VN:
                return False

            for rhs in rights:
                if len(rhs) == 0 and left == self.S:
                    continue
                if len(rhs) == 1 and rhs[0] in self.VT:
                    continue
                if len(rhs) == 2 and rhs[0] in self.VN and rhs[1] in self.VN:
                    continue
                return False

        return True
