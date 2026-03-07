# Laboratory Work 3: Lexer & Scanner

### Course: Formal Languages & Finite Automata
### Author: Pancenco Ina, FAF-242

----

## Overview

Lexical analysis is the first phase of a compiler or interpreter pipeline, responsible for converting a raw sequence of characters into a structured stream of tokens. A lexer (also called a scanner or tokenizer) reads the input string character by character, groups characters into meaningful units called lexemes, classifies each lexeme into a token type, and produces a sequence of tokens that can be consumed by subsequent phases such as parsing. This laboratory implements a lexer for a mathematical and physics expression language — a domain-specific language (DSL) capable of tokenizing formulas such as `F = m * a`, `E = m * c^2`, and `y = sin(theta) * v^2 / g`.

## Objectives

1. Understand what lexical analysis is.

2. Get familiar with the inner workings of a lexer/scanner/tokenizer.

3. Implement a token data structure and a lexer program that could be used as the first phase of a front-end for a compiler/interpreter for a simple mathematical/physics expression language.

## Theory

### Lexical Analysis

Lexical analysis is the process of converting a sequence of characters into a sequence of tokens. A token is a pair consisting of a token type (a symbolic name identifying a category of lexical unit) and a lexeme (the actual substring from the input). For example, given the input `F = m * a`, the lexer produces tokens like `VARIABLE(F)`, `ASSIGN(=)`, `VARIABLE(m)`, `MULTIPLY(*)`, `VARIABLE(a)`.

The lexer operates by scanning the input from left to right, one character at a time, using a set of rules to determine how characters should be grouped and classified. Whitespace is typically discarded (unless it is significant in the language), and each recognized group of characters is emitted as a token. If the lexer encounters a character that does not match any rule, it raises an error.

### Token Types

Each token belongs to a category that defines its role in the language. Common categories include literals (numbers, strings), identifiers (variable names), operators (arithmetic and logical), delimiters (parentheses, braces), and keywords (reserved words with special meaning). The set of token types defines the lexical grammar of the language.

### Finite Automata and Lexers

There is a deep connection between lexical analysis and finite automata. Each token recognition rule can be expressed as a regular expression, and every regular expression corresponds to a finite automaton. In practice, a lexer is essentially a collection of finite automata running in parallel: at each character, the lexer determines which automaton (i.e., which token rule) is active and transitions accordingly. When an automaton reaches an accepting state, a token is emitted. This is why lexical analysis is studied alongside formal languages and finite automata — the lexer is a direct application of the theory developed in previous laboratories.

## Language Description

The mathematical/physics expression DSL supports the following elements:

### Variables

Physics and math variable names such as `F`, `m`, `a`, `v`, `t`, `x`, `y`, `theta`, `v0`, `v_x`. Identifiers start with a letter and may contain letters, digits, and underscores.

### Numbers

Both integers and floating-point numbers: `10`, `3.14`, `0.001`, `0.5`.

### Operators

| Operator | Meaning        | Token Type |
|:--------:|:--------------:|:----------:|
| `+`      | Addition       | PLUS       |
| `-`      | Subtraction    | MINUS      |
| `*`      | Multiplication | MULTIPLY   |
| `/`      | Division       | DIVIDE     |
| `^`      | Power          | POWER      |

### Assignment

The `=` symbol is used for assignment (`F = m * a`), with token type `ASSIGN`.

### Parentheses

`(` and `)` are used for grouping and function arguments, with token types `LPAREN` and `RPAREN`.

### Mathematical Functions

Built-in functions recognized as special tokens: `sin`, `cos`, `tan`, `sqrt`, `log`. These are classified as `FUNCTION` tokens.

### Physical Constants

Reserved names recognized as constants: `pi`, `e`, `g`, `c`. These are classified as `CONSTANT` tokens.

### Complete Token Type Table

| Token Type | Examples           | Description                  |
|:----------:|:------------------:|:----------------------------:|
| NUMBER     | `3.14`, `2`, `0.5` | Numeric literals             |
| VARIABLE   | `F`, `theta`, `v0` | User-defined variable names  |
| FUNCTION   | `sin`, `cos`, `log`| Built-in math functions      |
| CONSTANT   | `pi`, `g`, `c`     | Physical/math constants      |
| PLUS       | `+`                | Addition operator            |
| MINUS      | `-`                | Subtraction operator         |
| MULTIPLY   | `*`                | Multiplication operator      |
| DIVIDE     | `/`                | Division operator            |
| POWER      | `^`                | Exponentiation operator      |
| ASSIGN     | `=`                | Assignment operator          |
| LPAREN     | `(`                | Left parenthesis             |
| RPAREN     | `)`                | Right parenthesis            |
| EOF        | —                  | End of input                 |

## Implementation Description

The implementation is split across three files: `token_types.py` defines the token categories, `token.py` defines the token data structure, and `lexer.py` contains the scanning logic.

### Token Types (token_types.py)

Token types are defined using Python's `Enum` class, which provides type safety and clear semantics. Each enum member represents a distinct token category.

```python
from enum import Enum

class TokenType(Enum):
    NUMBER = "NUMBER"
    VARIABLE = "VARIABLE"
    FUNCTION = "FUNCTION"
    CONSTANT = "CONSTANT"

    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    POWER = "^"

    ASSIGN = "="

    LPAREN = "("
    RPAREN = ")"

    EOF = "EOF"
```

### Token Object (token.py)

The `Token` class pairs a token type with its lexeme value. The `__repr__` method provides a readable representation for debugging and demonstration output.

```python
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type.name}: {self.value}"
```

### Lexer (lexer.py)

The `Lexer` class is the core component. It maintains a pointer (`pos`) into the input string and tracks the current character (`current_char`). The lexer processes the input character by character, using pattern-matching logic to classify and extract tokens.

#### Initialization and Character Navigation

The lexer is initialized with the input text. The `advance()` method moves the pointer forward by one position. When the end of input is reached, `current_char` is set to `None`, signaling termination.

```python
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[0] if text else None

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
```

#### Whitespace Handling

The `skip_whitespace()` method advances past any whitespace characters. Spaces, tabs, and newlines are not meaningful in mathematical expressions and are simply discarded.

```python
def skip_whitespace(self):
    while self.current_char is not None and self.current_char.isspace():
        self.advance()
```

#### Number Recognition

The `number()` method accumulates consecutive digit and decimal-point characters to form a numeric literal. This handles both integers (`42`) and floating-point numbers (`3.14`). The accumulated string is converted to a `float` and wrapped in a `NUMBER` token.

```python
def number(self):
    result = ""
    while self.current_char and (self.current_char.isdigit() or self.current_char == "."):
        result += self.current_char
        self.advance()
    return Token(TokenType.NUMBER, float(result))
```

#### Identifier Recognition

The `identifier()` method reads a sequence of alphanumeric characters and underscores, then classifies the result. The classification follows a priority chain: if the lexeme matches a known function name (`sin`, `cos`, `tan`, `sqrt`, `log`), it is classified as `FUNCTION`; if it matches a known constant (`pi`, `e`, `g`, `c`), it is classified as `CONSTANT`; otherwise, it is a user-defined `VARIABLE`. This approach effectively implements reserved-word recognition without a separate keyword table.

```python
def identifier(self):
    result = ""
    while self.current_char and (self.current_char.isalnum() or self.current_char == "_"):
        result += self.current_char
        self.advance()

    if result in ["sin", "cos", "tan", "sqrt", "log"]:
        return Token(TokenType.FUNCTION, result)

    if result in ["pi", "e", "g", "c"]:
        return Token(TokenType.CONSTANT, result)

    return Token(TokenType.VARIABLE, result)
```

#### Main Tokenization Loop

The `get_next_token()` method is the heart of the lexer. It examines the current character and dispatches to the appropriate handler: whitespace is skipped, digits trigger number recognition, letters trigger identifier recognition, and single-character operators and delimiters are returned directly. If an unrecognized character is encountered, an exception is raised. When the input is exhausted, an `EOF` token is returned to signal the end of the token stream.

```python
def get_next_token(self):
    while self.current_char:
        if self.current_char.isspace():
            self.skip_whitespace()
            continue

        if self.current_char.isdigit():
            return self.number()

        if self.current_char.isalpha() or self.current_char == "_":
            return self.identifier()

        if self.current_char == "+":
            self.advance()
            return Token(TokenType.PLUS, "+")

        if self.current_char == "-":
            self.advance()
            return Token(TokenType.MINUS, "-")

        # ... (similar for *, /, ^, =, (, ))

        raise Exception(f"Invalid character: '{self.current_char}' at position {self.pos}")

    return Token(TokenType.EOF, None)
```

### Lexer Algorithm Summary

The lexer follows a straightforward algorithm that can be described in four steps:

1. **Read** the current character from the input.
2. **Identify** the token type based on the character (digit → number, letter → identifier, symbol → operator).
3. **Extract** the complete lexeme by consuming characters until the token boundary is reached.
4. **Return** the token with its type and value.

This process repeats until the entire input has been consumed, at which point an `EOF` token is emitted.

## Demonstration

### Example 1: Newton's Second Law

**Input:** `F = m * a`

**Output:**
```
VARIABLE: F
ASSIGN: =
VARIABLE: m
MULTIPLY: *
VARIABLE: a
EOF: None
```

### Example 2: Einstein's Mass-Energy Equivalence

**Input:** `E = m * c^2`

**Output:**
```
VARIABLE: E
ASSIGN: =
VARIABLE: m
MULTIPLY: *
CONSTANT: c
POWER: ^
NUMBER: 2.0
EOF: None
```

Note that `c` is correctly recognized as a `CONSTANT` (speed of light), not a variable.

### Example 3: Kinematics Velocity

**Input:** `v = v0 + a * t`

**Output:**
```
VARIABLE: v
ASSIGN: =
VARIABLE: v0
PLUS: +
VARIABLE: a
MULTIPLY: *
VARIABLE: t
EOF: None
```

The identifier `v0` is treated as a single variable token, since identifiers may contain digits after the initial letter.

### Example 4: Kinematics Displacement

**Input:** `x = v0 * t + 0.5 * a * t^2`

**Output:**
```
VARIABLE: x
ASSIGN: =
VARIABLE: v0
MULTIPLY: *
VARIABLE: t
PLUS: +
NUMBER: 0.5
MULTIPLY: *
VARIABLE: a
MULTIPLY: *
VARIABLE: t
POWER: ^
NUMBER: 2.0
EOF: None
```

### Example 5: Projectile Motion

**Input:** `y = sin(theta) * v^2 / g`

**Output:**
```
VARIABLE: y
ASSIGN: =
FUNCTION: sin
LPAREN: (
VARIABLE: theta
RPAREN: )
MULTIPLY: *
VARIABLE: v
POWER: ^
NUMBER: 2.0
DIVIDE: /
CONSTANT: g
EOF: None
```

This example demonstrates the lexer's ability to distinguish between function names (`sin`), variables (`theta`, `v`, `y`), and constants (`g`), as well as correctly tokenizing nested parenthesized expressions.

### Example 6: Trigonometric and Logarithmic Functions

**Input:** `x = log(t) + sqrt(y)`

**Output:**
```
VARIABLE: x
ASSIGN: =
FUNCTION: log
LPAREN: (
VARIABLE: t
RPAREN: )
PLUS: +
FUNCTION: sqrt
LPAREN: (
VARIABLE: y
RPAREN: )
EOF: None
```

## Conclusions

This laboratory work implements a complete lexer for a mathematical and physics expression language. The lexer successfully converts raw input strings into structured token streams, correctly distinguishing between numbers, variables, mathematical functions, physical constants, operators, and delimiters. The implementation demonstrates the core principles of lexical analysis: character-by-character scanning, pattern-based classification, and lexeme extraction.

The connection between lexical analysis and the formal language theory studied in previous laboratories is direct — each token recognition rule corresponds to a regular expression, and the lexer effectively implements a collection of finite automata that run in parallel over the input. The identifier classification logic (distinguishing functions, constants, and variables) shows how reserved-word handling extends the basic automaton model with a lookup step after the identifier is fully scanned.

The lexer handles a variety of real physics formulas, from simple expressions like `F = m * a` to complex ones involving trigonometric functions, exponentiation, and multiple variables, producing correct and readable token output in all cases. This implementation provides a solid foundation for extending the system with a parser in future work, completing the front-end pipeline of a compiler or interpreter.
