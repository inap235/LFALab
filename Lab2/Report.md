# Laboratory Work 2: Determinism in Finite Automata. Conversion from NDFA to DFA. Chomsky Hierarchy

### Course: Formal Languages and Finite Automata
### Author: Pancenco Ina, FAF-242

----

## Overview

This laboratory work extends the previous project with functionality around determinism, conversions between representations, and grammar classification. A nondeterministic finite automaton (NFA) is converted to a deterministic finite automaton (DFA) using subset construction, and the NFA is also converted to a regular grammar. The resulting grammar is classified in the Chomsky hierarchy.

## Objectives

1. Provide a function in the Grammar class to classify a grammar in the Chomsky hierarchy.
2. Use the same repository and project from the previous lab.
3. For the assigned variant, implement:
	 - Conversion of a finite automaton to a regular grammar.
	 - Determinism check for the FA.
	 - Conversion from NDFA to DFA.


## Variant Definition

Finite automaton variant used in the implementation:

- States: Q = {q0, q1, q2, q3}
- Alphabet: Sigma = {a, b, c}
- Start state: q0
- Final states: F = {q3}
- Transition function delta:
	- delta(q0, a) = {q0, q1}
	- delta(q1, b) = {q2}
	- delta(q2, a) = {q2}
	- delta(q2, b) = {q3}
	- delta(q3, a) = {q3}

## Implementation Description

### Determinism check

The automaton is deterministic if and only if every transition leads to a single next state. The method `is_deterministic()` scans the transition map and returns False if any transition has more than one destination state.

```python
def is_deterministic(self):
	for key in self.delta:
		if len(self.delta[key]) > 1:
			return False
	return True
```

### FA to regular grammar

The conversion from finite automaton to regular grammar is implemented as follows:

- Each state becomes a nonterminal.
- Alphabet symbols become terminals.
- For each transition q --a--> r, add a production q -> a r.
- For each final state f, add an epsilon production f -> epsilon.

This preserves the accepted language.

```python
def to_regular_grammar(self):
	from grammar import Grammar
	VN = set(self.Q)
	VT = set(self.Sigma)
	S = self.q0
	P = {}

	for (state, symbol), next_states in self.delta.items():
		for next_state in next_states:
			right = symbol + next_state
			P.setdefault(state, []).append(right)

	for f in self.F:
		P.setdefault(f, []).append("")

	return Grammar(VN, VT, P, S)
```

### Grammar classification

The `classify_grammar()` method checks grammar productions and reports:

- Type 3 (Regular) if all productions are of the form A -> a or A -> aB or A -> epsilon.
- Type 2 (Context-Free) if every left-hand side is a single nonterminal.
- Type 1 (Context-Sensitive) if productions are length non-decreasing.
- Type 0 otherwise.

```python
def classify_grammar(self):
	is_regular = True
	for left, rights in self.P.items():
		if left not in self.VN:
			is_regular = False
			break
		for right in rights:
			if right == "":
				continue
			# Find terminal prefix
			terminal = None
			for t in sorted(self.VT, key=len, reverse=True):
				if right.startswith(t):
					terminal = t
					break
			if terminal is None:
				is_regular = False
				break
			rest = right[len(terminal):]
			if rest != "" and rest not in self.VN:
				is_regular = False
				break

	if is_regular:
		return "Type 3 - Regular grammar"

	is_cfl = all(left in self.VN for left in self.P.keys())
	if is_cfl:
		return "Type 2 - Context-Free grammar"

	is_csl = True
	for left, rights in self.P.items():
		for right in rights:
			if len(right) < len(left):
				is_csl = False
				break
		if not is_csl:
			break

	if is_csl:
		return "Type 1 - Context-Sensitive grammar"

	return "Type 0 - Unrestricted grammar"
```

### NDFA to DFA

The subset construction algorithm is implemented in `to_dfa()`:

- Each DFA state is a set of NFA states.
- The DFA start state is the set containing the NFA start state.
- For each DFA state and symbol, compute the union of NFA transitions to get the next DFA state.
- Any DFA state containing an NFA final state is marked as final.

```python
def to_dfa(self):
	start = frozenset({self.q0})
	dfa_states = {start}
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
```

## Testing and Verification

The `main.py` client:

- Builds the NFA for the variant.
- Prints the automaton details.
- Checks determinism.
- Converts the FA to a regular grammar and prints productions.
- Classifies the grammar.
- Converts the NFA to a DFA and prints its transitions.
- Tests a small set of input words on the DFA.

These steps demonstrate the correctness of the conversions and show the expected behavior for determinism and language acceptance.

## Conclusions

The implementation provides a full workflow from NFA to DFA, with determinism detection and conversion to a regular grammar. The grammar is classified in the Chomsky hierarchy, completing the theoretical requirements.
