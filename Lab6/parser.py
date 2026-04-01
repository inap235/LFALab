from ast_nodes import (
    AssignmentNode,
    BinaryOpNode,
    ConstantNode,
    FunctionCallNode,
    NumberNode,
    UnaryOpNode,
    VariableNode,
)
from token_types import TokenType


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position]

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]

    def peek(self):
        index = self.position + 1
        if index < len(self.tokens):
            return self.tokens[index]
        return None

    def expect(self, token_type):
        if self.current_token.type != token_type:
            raise ParserError(
                f"Expected {token_type.name}, got {self.current_token.type.name} ({self.current_token.value})"
            )
        token = self.current_token
        self.advance()
        return token

    def parse(self):
        node = self.parse_statement()
        self.expect(TokenType.EOF)
        return node

    def parse_statement(self):
        if (
            self.current_token.type == TokenType.VARIABLE
            and self.peek() is not None
            and self.peek().type == TokenType.ASSIGN
        ):
            target = VariableNode(self.expect(TokenType.VARIABLE).value)
            self.expect(TokenType.ASSIGN)
            value = self.parse_expression()
            return AssignmentNode(target=target, value=value)

        return self.parse_expression()

    def parse_expression(self):
        node = self.parse_term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.value
            self.advance()
            right = self.parse_term()
            node = BinaryOpNode(left=node, operator=operator, right=right)

        return node

    def parse_term(self):
        node = self.parse_power()

        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            operator = self.current_token.value
            self.advance()
            right = self.parse_power()
            node = BinaryOpNode(left=node, operator=operator, right=right)

        return node

    def parse_power(self):
        node = self.parse_unary()

        if self.current_token.type == TokenType.POWER:
            operator = self.current_token.value
            self.advance()
            right = self.parse_power()
            node = BinaryOpNode(left=node, operator=operator, right=right)

        return node

    def parse_unary(self):
        if self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            operator = self.current_token.value
            self.advance()
            operand = self.parse_unary()
            return UnaryOpNode(operator=operator, operand=operand)

        return self.parse_primary()

    def parse_primary(self):
        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)

        if token.type == TokenType.VARIABLE:
            self.advance()
            return VariableNode(token.value)

        if token.type == TokenType.CONSTANT:
            self.advance()
            return ConstantNode(token.value)

        if token.type == TokenType.FUNCTION:
            function_name = token.value
            self.advance()
            self.expect(TokenType.LPAREN)
            argument = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return FunctionCallNode(name=function_name, argument=argument)

        if token.type == TokenType.LPAREN:
            self.advance()
            expression = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expression

        raise ParserError(
            f"Unexpected token {token.type.name} ({token.value}) at position {self.position}"
        )
