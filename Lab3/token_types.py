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
