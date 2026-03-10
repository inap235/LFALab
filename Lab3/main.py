from lexer import Lexer
def demo(expression):
    print(f"\nInput: {expression}")
    print("-" * 40)
    lexer = Lexer(expression)
    while True:
        token = lexer.get_next_token()
        print(f"  {token}")
        if token.type.name == "EOF":
            break


print("=" * 50)
print("  PHYSICS EXPRESSION LEXER - DEMONSTRATION")
print("=" * 50)

# Input of the expression
demo(input("Enter a physics expression: "))


print("\n" + "=" * 50)
print("  TOKEN SUMMARY TABLE")
print("=" * 50)
print(f"  {'Token Type':<15} {'Example':<15}")
print(f"  {'-'*15} {'-'*15}")
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
