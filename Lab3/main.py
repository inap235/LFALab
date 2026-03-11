from collections import Counter

from lexer import Lexer


def tokenize_expression(expression):
    lexer = Lexer(expression)
    return lexer.tokenize()


def print_tokens_table(tokens):
    print(f"  {'#':<4} {'Type':<12} {'Value':<20}")
    print(f"  {'-' * 4} {'-' * 12} {'-' * 20}")
    for index, token in enumerate(tokens, start=1):
        print(f"  {index:<4} {token.type.name:<12} {str(token.value):<20}")


def print_token_counts(tokens):
    counts = Counter(token.type.name for token in tokens)
    print("\n  Token counts:")
    print(f"  {'Type':<12} {'Count':<5}")
    print(f"  {'-' * 12} {'-' * 5}")
    for token_type in sorted(counts):
        print(f"  {token_type:<12} {counts[token_type]:<5}")


def demo(expression, title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print(f"  Input: {expression}\n")
    tokens = tokenize_expression(expression)
    print_tokens_table(tokens)
    print_token_counts(tokens)


print("=" * 60)
print("  PHYSICS EXPRESSION LEXER - DEMONSTRATION")
print("=" * 60)

predefined_cases = [
    ("E = m * c^2", "Case 1: Energy-Mass Relation"),
    ("F = G * m1 * m2 / r^2", "Case 2: Gravitational Force"),
    ("x = v0 * t + 0.5 * a * t^2", "Case 3: Uniformly Accelerated Motion"),
]

for expression, title in predefined_cases:
    demo(expression, title)

custom_expression = input("\nEnter your own physics expression (or press Enter to skip): ").strip()
if custom_expression:
    demo(custom_expression, "Custom Case")


print("\n" + "=" * 60)
print("  TOKEN SUMMARY TABLE")
print("=" * 60)
print(f"  {'Token Type':<15} {'Example':<15}")
print(f"  {'-' * 15} {'-' * 15}")
print(f"  {'NUMBER':<15} {'3.14':<15}")
print(f"  {'VARIABLE':<15} {'v, theta':<15}")
print(f"  {'FUNCTION':<15} {'sin, cos':<15}")
print(f"  {'CONSTANT':<15} {'pi, g, c':<15}")
print(f"  {'PLUS':<15} {'+':<15}")
print(f"  {'MINUS':<15} {'-':<15}")
print(f"  {'MULTIPLY':<15} {'*':<15}")
print(f"  {'DIVIDE':<15} {'/':<15}")
print(f"  {'POWER':<15} {'^':<15}")
print(f"  {'ASSIGN':<15} {'=':<15}")
print(f"  {'LPAREN':<15} {'(':<15}")
print(f"  {'RPAREN':<15} {')':<15}")
print(f"  {'EOF':<15} {'(end)':<15}")
