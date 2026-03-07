from token_types import TokenType
from token import Token


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

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ""
        while self.current_char and (self.current_char.isdigit() or self.current_char == "."):
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, float(result))

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

            if self.current_char == "*":
                self.advance()
                return Token(TokenType.MULTIPLY, "*")

            if self.current_char == "/":
                self.advance()
                return Token(TokenType.DIVIDE, "/")

            if self.current_char == "^":
                self.advance()
                return Token(TokenType.POWER, "^")

            if self.current_char == "=":
                self.advance()
                return Token(TokenType.ASSIGN, "=")

            if self.current_char == "(":
                self.advance()
                return Token(TokenType.LPAREN, "(")

            if self.current_char == ")":
                self.advance()
                return Token(TokenType.RPAREN, ")")

            raise Exception(f"Invalid character: '{self.current_char}' at position {self.pos}")

        return Token(TokenType.EOF, None)

    def tokenize(self):
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens