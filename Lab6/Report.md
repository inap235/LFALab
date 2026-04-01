# Laboratory Work 6: Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Author: Pancenco Ina, FAF-242

----

## Overview

Parsing is the stage that follows lexical analysis. A parser receives a stream of tokens and reconstructs their syntactic structure according to grammar rules. The result is usually represented as a tree. In this laboratory, the parser builds an Abstract Syntax Tree (AST), which is a compact representation of the program structure that keeps only the meaningful constructs.

This lab extends the lexer from Lab 3 for a mathematical and physics expression language and adds two major components:

1. a regex-based lexical analyzer with explicit token categories;
2. a recursive-descent parser that creates AST nodes for assignments, arithmetic expressions, constants, variables, unary operators, and function calls.

## Objectives

1. Understand and implement basic parsing for expression syntax.
2. Build a structured AST for further semantic steps.
3. Reuse and improve the Lab 3 tokenization components.
4. Keep the implementation clear and testable with sample inputs.

## Language Elements

The parser supports:

- assignment: `x = expression`
- binary operators: `+`, `-`, `*`, `/`, `^`
- unary operators: `+`, `-`
- parentheses: `( ... )`
- numeric literals: `3`, `0.5`, `.25`
- identifiers as variables: `x`, `v0`, `theta`
- constants: `pi`, `e`, `g`, `c`
- unary function calls: `sin(expr)`, `cos(expr)`, `tan(expr)`, `sqrt(expr)`, `log(expr)`

## Grammar Used by the Parser

The recursive-descent parser follows this precedence-aware grammar:

```text
statement   -> VARIABLE ASSIGN expression | expression
expression  -> term ((PLUS | MINUS) term)*
term        -> power ((MULTIPLY | DIVIDE) power)*
power       -> unary (POWER power)?
unary       -> (PLUS | MINUS) unary | primary
primary     -> NUMBER
            | VARIABLE
            | CONSTANT
            | FUNCTION LPAREN expression RPAREN
            | LPAREN expression RPAREN
```

This gives the correct operator precedence and right-associative exponentiation.

## Why AST Instead of a Parse Tree

For this laboratory, an AST is more useful than a full parse tree because it stores the semantic shape of the expression without keeping every grammar helper nonterminal. A parse tree would include intermediate nodes such as `term` and `power` for each derivation step, which is useful for debugging a grammar but usually too verbose for later compiler stages.

The AST keeps only language constructs that matter for interpretation or code generation:

- assignment structure (`AssignmentNode`)
- operations (`BinaryOpNode`, `UnaryOpNode`)
- value-bearing leaves (`NumberNode`, `VariableNode`, `ConstantNode`)
- function application (`FunctionCallNode`)

This makes the tree easier to traverse for tasks like constant folding, variable checking, symbolic simplification, or direct evaluation.

## Parsing Strategy and Operator Rules

The parser is implemented with recursive descent. Each method is aligned with one precedence level in the expression grammar.

1. `parse_expression()` handles addition/subtraction.
2. `parse_term()` handles multiplication/division.
3. `parse_power()` handles exponentiation and keeps it right-associative.
4. `parse_unary()` handles unary plus/minus.
5. `parse_primary()` handles literals, identifiers, constants, parentheses, and function calls.

This decomposition guarantees the standard precedence relation:

$$
  ext{unary} > \text{power} > \text{multiply/divide} > \text{plus/minus}
$$

and exponentiation associativity:

$$
a^{b^c} = a^{(b^c)}
$$

### Example: associativity check

For input `2 ^ 3 ^ 2`, the parser builds:

```text
BinaryOp(^)
  Number(2.0)
  BinaryOp(^)
    Number(3.0)
    Number(2.0)
```

which is the expected right-nested structure.

## Implementation

The implementation is in [Lab6](Lab6):

- [Lab6/token_types.py](Lab6/token_types.py): token categories
- [Lab6/token_model.py](Lab6/token_model.py): token object
- [Lab6/lexer.py](Lab6/lexer.py): regex-based lexer
- [Lab6/ast_nodes.py](Lab6/ast_nodes.py): AST node structures and formatter
- [Lab6/parser.py](Lab6/parser.py): recursive-descent parser
- [Lab6/main.py](Lab6/main.py): demonstration runner

### Regex-Based Lexer

Unlike Lab 3's character-by-character token decisions, this lexer uses regular expressions for token class detection, as required.

A combined pattern with named groups is used:

- `NUMBER`, `FUNCTION`, `CONSTANT`, `VARIABLE`
- symbolic tokens (`PLUS`, `MINUS`, `MULTIPLY`, `DIVIDE`, `POWER`, `ASSIGN`, `LPAREN`, `RPAREN`)
- `SKIP` for whitespace
- `MISMATCH` for invalid characters

The lexer converts numeric lexemes to `float` and appends `EOF` at the end.

Because the tokenization is regex-based, classification is explicit and deterministic. For example, lexemes like `sin` and `sqrt` are matched as `FUNCTION` before generic `VARIABLE`. Similarly, `pi` and `g` are matched as `CONSTANT` and not as normal identifiers. This avoids ambiguity and keeps the parser logic simpler.

The implementation also validates full input coverage. If a regex match does not start exactly at the current scanning position, a lexical error is raised. This prevents silent skipping of invalid characters and guarantees that each input character is either tokenized or rejected with a clear message.

### AST Data Structures

AST nodes are represented through dedicated classes:

- `NumberNode`
- `VariableNode`
- `ConstantNode`
- `UnaryOpNode`
- `BinaryOpNode`
- `FunctionCallNode`
- `AssignmentNode`

A `format_ast()` function prints the resulting tree in a readable hierarchical form.

### Parser

The parser is a recursive-descent parser that consumes the token stream and builds AST nodes directly. It performs syntax checks with explicit errors when an unexpected token is found.

The top-level parse result is either:

- an `AssignmentNode`, or
- an expression tree.

The parser includes two utility mechanisms that improve robustness:

1. `expect(token_type)` verifies strict syntax and raises a precise error when the token does not match.
2. `peek()` enables lookahead for distinguishing assignment statements from pure expressions.

For example, when input starts with a variable, lookahead checks whether the next token is `ASSIGN`:

- if yes, parse as statement `variable = expression`;
- if no, parse as ordinary expression.

This makes forms like `x = v + 1` and `x + 1` both valid entry points.

## Error Handling

Two explicit error classes are used:

- `LexerError` for invalid characters or broken tokenization coverage;
- `ParserError` for syntax violations.

Typical parser errors include:

- missing closing parenthesis, such as `sin(x + 2`
- invalid operator sequence, such as `a + * b`
- incomplete assignment, such as `x =`

The main program wraps execution in `try/except` and prints concise diagnostics. This keeps the demo user-friendly while preserving strict checks in the core components.

## Complexity Discussion

Let $n$ be the number of characters in the input and $k$ the number of produced tokens.

- Lexing runs in $O(n)$ for this token specification.
- Parsing runs in $O(k)$ because each token is consumed a constant number of times.
- AST size is $O(k)$.

Therefore, the end-to-end complexity is linear in input length, which is expected for a deterministic expression grammar.

## Example Results

Input:

```text
x = v0 * t + 0.5 * a * t^2
```

AST (simplified):

```text
Assignment
  Variable(x)
  BinaryOp(+)
    BinaryOp(*)
      Variable(v0)
      Variable(t)
    BinaryOp(*)
      BinaryOp(*)
        Number(0.5)
        Variable(a)
      BinaryOp(^)
        Variable(t)
        Number(2.0)
```

Input:

```text
y = sin(theta) * v^2 / g
```

AST contains:

- assignment target `y`
- multiplication and division binary nodes
- `FunctionCall(sin)` with argument `Variable(theta)`
- constant node `g`

### Additional example with unary operators

Input:

```text
z = -a + +b
```

AST shape:

```text
Assignment
  Variable(z)
  BinaryOp(+)
    UnaryOp(-)
      Variable(a)
    UnaryOp(+)
      Variable(b)
```

This confirms that unary operators are bound before binary addition/subtraction.

## Validation Notes

The implementation was tested with:

- assignment expressions from physics formulas;
- nested parentheses;
- function applications with expression arguments;
- pure expressions without assignment;
- unary and exponent operators in the same input.

All tested expressions generated valid token streams and well-formed ASTs.

## Limitations and Possible Extensions

Current parser scope is intentionally compact and focused on this lab requirement. It does not yet include:

- multi-argument functions;
- implicit multiplication (`2x` or `(a+b)(c+d)`);
- relational operators (`<`, `>`, `==`);
- multi-statement programs.

These can be added incrementally by extending the grammar and introducing new AST node types. The current design already separates lexer, parser, and AST model, so such extensions are straightforward.

## How to Run

From the repository root:

```bash
python Lab6/main.py
```

The script executes predefined examples and allows one custom expression.

## Conclusion

This laboratory completes the next stage after lexical analysis by implementing a full syntax phase for the same expression language and materializing the result as an AST. In practical terms, the work demonstrates how to go from raw text to structured meaning through two deterministic passes: tokenization and parsing.

The final architecture is modular and reusable: token definitions, lexer, parser, and AST are cleanly separated. The parser correctly enforces precedence and associativity rules, distinguishes assignments from expressions through lookahead, and reports syntax problems explicitly. The generated AST already has the structure required for the next compiler-oriented steps, including evaluation, semantic validation, and optimization experiments.
