from dataclasses import dataclass


class ASTNode:
    pass


@dataclass
class NumberNode(ASTNode):
    value: float


@dataclass
class VariableNode(ASTNode):
    name: str


@dataclass
class ConstantNode(ASTNode):
    name: str


@dataclass
class UnaryOpNode(ASTNode):
    operator: str
    operand: ASTNode


@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class FunctionCallNode(ASTNode):
    name: str
    argument: ASTNode


@dataclass
class AssignmentNode(ASTNode):
    target: VariableNode
    value: ASTNode


def format_ast(node, level=0):
    indent = "  " * level

    if isinstance(node, NumberNode):
        return f"{indent}Number({node.value})"

    if isinstance(node, VariableNode):
        return f"{indent}Variable({node.name})"

    if isinstance(node, ConstantNode):
        return f"{indent}Constant({node.name})"

    if isinstance(node, UnaryOpNode):
        lines = [f"{indent}UnaryOp({node.operator})"]
        lines.append(format_ast(node.operand, level + 1))
        return "\n".join(lines)

    if isinstance(node, BinaryOpNode):
        lines = [f"{indent}BinaryOp({node.operator})"]
        lines.append(format_ast(node.left, level + 1))
        lines.append(format_ast(node.right, level + 1))
        return "\n".join(lines)

    if isinstance(node, FunctionCallNode):
        lines = [f"{indent}FunctionCall({node.name})"]
        lines.append(format_ast(node.argument, level + 1))
        return "\n".join(lines)

    if isinstance(node, AssignmentNode):
        lines = [f"{indent}Assignment"]
        lines.append(format_ast(node.target, level + 1))
        lines.append(format_ast(node.value, level + 1))
        return "\n".join(lines)

    raise TypeError(f"Unsupported AST node: {type(node).__name__}")
