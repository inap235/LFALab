import re

from token_model import Token
from token_types import TokenType


class LexerError(Exception):
    pass


class Lexer:
    TOKEN_SPECIFICATION = [
        ("NUMBER", r"(?:\d+\.\d+|\d+|\.\d+)"),
        ("FUNCTION", r"(?:sin|cos|tan|sqrt|log)\b"),
        ("CONSTANT", r"(?:pi|e|g|c)\b"),
        ("VARIABLE", r"[A-Za-z_][A-Za-z0-9_]*"),
        ("PLUS", r"\+"),
        ("MINUS", r"-"),
        ("MULTIPLY", r"\*"),
        ("DIVIDE", r"/"),
        ("POWER", r"\^"),
        ("ASSIGN", r"="),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("SKIP", r"[ \t\n\r]+"),
        ("MISMATCH", r"."),
    ]

    TOKEN_REGEX = re.compile(
        "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECIFICATION)
    )

    TYPE_MAP = {
        "NUMBER": TokenType.NUMBER,
        "VARIABLE": TokenType.VARIABLE,
        "FUNCTION": TokenType.FUNCTION,
        "CONSTANT": TokenType.CONSTANT,
        "PLUS": TokenType.PLUS,
        "MINUS": TokenType.MINUS,
        "MULTIPLY": TokenType.MULTIPLY,
        "DIVIDE": TokenType.DIVIDE,
        "POWER": TokenType.POWER,
        "ASSIGN": TokenType.ASSIGN,
        "LPAREN": TokenType.LPAREN,
        "RPAREN": TokenType.RPAREN,
    }

    def __init__(self, text):
        self.text = text

    def tokenize(self):
        tokens = []
        position = 0

        for match in self.TOKEN_REGEX.finditer(self.text):
            if match.start() != position:
                raise LexerError(f"Unexpected character at position {position}")

            kind = match.lastgroup
            lexeme = match.group()
            position = match.end()

            if kind == "SKIP":
                continue

            if kind == "MISMATCH":
                raise LexerError(f"Invalid character: '{lexeme}' at position {match.start()}")

            token_type = self.TYPE_MAP[kind]
            value = float(lexeme) if token_type == TokenType.NUMBER else lexeme
            tokens.append(Token(token_type, value))

        if position != len(self.text):
            raise LexerError(f"Unexpected character at position {position}")

        tokens.append(Token(TokenType.EOF, None))
        return tokens
