from lexer import Lexer, LexerError
from parser import Parser, ParserError
from ast_nodes import format_ast


def print_tokens(tokens):
    print(f"  {'#':<4} {'Type':<12} {'Value':<20}")
    print(f"  {'-' * 4} {'-' * 12} {'-' * 20}")
    for index, token in enumerate(tokens, start=1):
        print(f"  {index:<4} {token.type.name:<12} {str(token.value):<20}")


def run_case(expression, title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)
    print(f"  Input: {expression}\n")

    lexer = Lexer(expression)
    tokens = lexer.tokenize()
    print("  Tokens:")
    print_tokens(tokens)

    parser = Parser(tokens)
    ast = parser.parse()

    print("\n  AST:")
    print(format_ast(ast, level=1))


def main():
    print("=" * 70)
    print("  LAB 6 - PARSER & ABSTRACT SYNTAX TREE")
    print("=" * 70)

    examples = [
        ("E = m * c^2", "Case 1: Assignment with exponentiation"),
        ("x = v0 * t + 0.5 * a * t^2", "Case 2: Complex arithmetic expression"),
        ("y = sin(theta) * v^2 / g", "Case 3: Function and constants"),
        ("sqrt(4 + 5) * 2", "Case 4: Pure expression (no assignment)"),
    ]

    for expression, title in examples:
        run_case(expression, title)

    custom_expression = input("\nEnter an expression to parse: ").strip()
    if custom_expression:
        run_case(custom_expression, "Custom case")


if __name__ == "__main__":
    try:
        main()
    except (LexerError, ParserError) as error:
        print(f"\nError: {error}")
