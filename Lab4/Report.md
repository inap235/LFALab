# Laboratory Work 4: Regular Expressions

### Course: Formal Languages & Finite Automata
### Author: Pancenco Ina, FAF-242

----

## Overview

This laboratory focuses on regular expressions and dynamic generation of valid words from regex patterns.
The selected assignment is **Variant 3**, which contains three complex regular expressions.

A key requirement is that the solution must **interpret regex dynamically**, not hardcode string templates for each pattern. To satisfy this, I implemented a parser + generator pipeline based on an abstract syntax tree (AST).

Because `*` and `+` may generate infinitely many words, a maximum repetition limit of **5** is applied.

## Objectives

1. Explain what regular expressions are and where they are used.
2. Implement a dynamic generator that receives regex patterns as input and outputs valid words.
3. Respect repetition limits for unbounded quantifiers (`*`, `+`) to avoid extremely long outputs.
4. Implement a bonus feature that shows the sequence of regex processing steps.

## What Are Regular Expressions

Regular expressions (regex) are symbolic notations used to define sets of strings over an alphabet.
They are used in:

- lexical analysis and tokenization
- input validation
- search/match engines
- compiler front-ends
- data extraction and filtering

In formal language theory, regex describe **regular languages**, which are equivalent in expressive power to **finite automata**.

### Operators used in this lab

| Operator | Meaning |
|---|---|
| `|` | alternation (choice) |
| `()` | grouping |
| concatenation | sequence of symbols/subexpressions |
| `*` | zero or more repetitions |
| `+` | one or more repetitions |
| `?` | optional (zero or one) |
| `^n` | exact repetition (lab notation) |

## Variant 3 Regular Expressions

1. `O(P|Q|R)^+2(3|4)`
2. `A*B(C|D|E)F(G|H|I)^2`
3. `J^+K(L|M|N)*O?(P|Q)`

The implemented generator supports these expressions directly and can process other expressions using the same operators.

## Implementation

Files:

- `regex_generator.py` - parser, AST nodes, generator, trace function
- `main.py` - demonstration for Variant 3, output, and validation

### 1. Dynamic parsing

The regex is transformed into an AST by a recursive-descent parser:

- `expression -> alternation`
- `alternation -> concatenation ('|' concatenation)*`
- `concatenation -> repetition+`
- `repetition -> primary quantifier*`
- `primary -> '(' expression ')' | literal`

This means the program does not depend on the concrete Variant 3 structure; it interprets syntax rules and builds a structure that can be evaluated for any compatible regex.

### 2. AST nodes and generation

Main node types:

- `LiteralNode`
- `ConcatNode`
- `AlternateNode`
- `RepeatNode`

Generation is done by recursively evaluating nodes:

- `LiteralNode` appends one symbol
- `ConcatNode` concatenates child results
- `AlternateNode` selects one option randomly
- `RepeatNode` chooses a repetition count and repeats the child

### 3. Repetition limit

For `*` and `+`, the upper bound is set to `MAX_REPEAT = 5`.

- `*` -> repetitions in `[0, 5]`
- `+` -> repetitions in `[1, 5]`

For exact exponent notation `^n`, repetition is fixed to `n`.

### 4. Bonus: processing sequence

The function `explain_generation(...)` returns:

- generated word
- ordered list of processing steps

This makes the generation process transparent and easy to present during lab defense.

## Example Run (Variant 3)

For each of the three expressions, the script prints 10 generated words.

Examples of valid outputs (will vary because generation is random):

- Regex 1: `OPP23`, `ORQR24`, `OQQQ23`
- Regex 2: `BCFGG`, `AAABDFHH`, `AAAAABEFGI`
- Regex 3: `JJKMP`, `JKOP`, `JJJJKNLP`

The script also validates generated words against Python `re.fullmatch` (after converting `^n` to `{n}`), confirming correctness.

## Sequence Example (Bonus)

Pattern: `J+K(L|M|N)*O?(P|Q)`

Typical processing trace:

1. Apply `+` on `J` -> choose count in `[1, 5]`
2. Append literal `K`
3. Apply `*` on `(L|M|N)` -> choose count in `[0, 5]`
4. For each repetition, choose one of `L`, `M`, `N`
5. Apply `?` on `O` -> include or skip
6. Choose one of `P`, `Q`
7. Concatenate all produced fragments

Result example: `JJJKMOP`

## Difficulties Encountered

1. Designing dynamic interpretation instead of hardcoded templates.
2. Correctly handling precedence and associativity of regex operators.
3. Supporting lab notation `^n` together with standard operators.
4. Preventing unbounded growth from `*` and `+` by introducing a limit.
5. Producing understandable processing traces for demonstration.

## Conclusion

The laboratory objectives were completed:

- regular expressions were explained from both practical and formal-language perspectives;
- a dynamic regex parser and generator was implemented;
- unbounded repetitions are limited to 5 as requested;
- bonus processing sequence functionality was implemented.

The final solution is reusable and can generate valid words for any regex built from the supported operators, not only the three Variant 3 expressions.
