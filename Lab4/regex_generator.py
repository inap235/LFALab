import random
from dataclasses import dataclass
from typing import List, Optional, Tuple


class RegexSyntaxError(ValueError):
    """for errors"""


@dataclass
class GenerationContext:
    max_repeat: int
    rng: random.Random
    trace_enabled: bool
    steps: List[str]

    def log(self, message: str) -> None:
        if self.trace_enabled:
            self.steps.append(message)


class Node:
    def generate(self, context: GenerationContext) -> str:
        raise NotImplementedError


@dataclass
class LiteralNode(Node):
    value: str

    def generate(self, context: GenerationContext) -> str:
        context.log(f"Append literal '{self.value}'")
        return self.value


@dataclass
class ConcatNode(Node):
    parts: List[Node]

    def generate(self, context: GenerationContext) -> str:
        result = []
        for part in self.parts:
            result.append(part.generate(context))
        return "".join(result)


@dataclass
class AlternateNode(Node):
    options: List[Node]

    def generate(self, context: GenerationContext) -> str:
        index = context.rng.randrange(len(self.options))
        context.log(f"Choose alternative {index + 1}/{len(self.options)}")
        return self.options[index].generate(context)


@dataclass
class RepeatNode(Node):
    node: Node
    min_repeat: int
    max_repeat: Optional[int]
    label: str

    def generate(self, context: GenerationContext) -> str:
        effective_max = self.max_repeat
        if effective_max is None:
            effective_max = context.max_repeat

        if effective_max < self.min_repeat:
            raise ValueError(
                f"Invalid repeat bounds for {self.label}: "
                f"min={self.min_repeat}, max={effective_max}"
            )

        count = context.rng.randint(self.min_repeat, effective_max)
        context.log(
            f"Apply quantifier '{self.label}': repeat {count} time(s)"
        )

        chunks = []
        for _ in range(count):
            chunks.append(self.node.generate(context))
        return "".join(chunks)


class RegexParser:
    def __init__(self, pattern: str) -> None:
        self.pattern = pattern
        self.index = 0

    def parse(self) -> Node:
        node = self._parse_expression()
        self._skip_spaces()
        if not self._at_end():
            raise RegexSyntaxError(
                f"Unexpected character '{self._peek()}' at position {self.index}"
            )
        return node

    def _parse_expression(self) -> Node:
        return self._parse_alternation()

    def _parse_alternation(self) -> Node:
        options = [self._parse_concatenation()]

        self._skip_spaces()
        while self._peek() == "|":
            self._advance()  # consume '|'
            options.append(self._parse_concatenation())
            self._skip_spaces()

        if len(options) == 1:
            return options[0]
        return AlternateNode(options)

    def _parse_concatenation(self) -> Node:
        parts = []

        self._skip_spaces()
        while not self._at_end() and self._peek() not in ")|":
            parts.append(self._parse_repetition())
            self._skip_spaces()

        if not parts:
            # Empty group () is allowed and generates epsilon.
            return ConcatNode([])

        if len(parts) == 1:
            return parts[0]
        return ConcatNode(parts)

    def _parse_repetition(self) -> Node:
        node = self._parse_primary()

        while True:
            self._skip_spaces()
            token = self._peek()

            if token == "*":
                self._advance()
                node = RepeatNode(node=node, min_repeat=0, max_repeat=None, label="*")
                continue

            if token == "+":
                self._advance()
                node = RepeatNode(node=node, min_repeat=1, max_repeat=None, label="+")
                continue

            if token == "?":
                self._advance()
                node = RepeatNode(node=node, min_repeat=0, max_repeat=1, label="?")
                continue

            if token == "^":
                self._advance()
                power_token = self._peek()

                if power_token == "+":
                    self._advance()
                    node = RepeatNode(
                        node=node,
                        min_repeat=1,
                        max_repeat=None,
                        label="^+",
                    )
                    continue

                if power_token == "*":
                    self._advance()
                    node = RepeatNode(
                        node=node,
                        min_repeat=0,
                        max_repeat=None,
                        label="^*",
                    )
                    continue

                if power_token == "?":
                    self._advance()
                    node = RepeatNode(
                        node=node,
                        min_repeat=0,
                        max_repeat=1,
                        label="^?",
                    )
                    continue

                number = self._parse_integer()
                node = RepeatNode(
                    node=node,
                    min_repeat=number,
                    max_repeat=number,
                    label=f"^{number}",
                )
                continue

            break

        return node

    def _parse_primary(self) -> Node:
        self._skip_spaces()

        if self._at_end():
            raise RegexSyntaxError("Unexpected end of pattern")

        token = self._peek()

        if token == "(":
            self._advance()  # consume '('
            node = self._parse_expression()
            self._skip_spaces()
            if self._peek() != ")":
                raise RegexSyntaxError(
                    f"Missing closing ')' at position {self.index}"
                )
            self._advance()  # consume ')'
            return node

        if token in "|)*+?^":
            raise RegexSyntaxError(
                f"Unexpected token '{token}' at position {self.index}"
            )

        self._advance()
        return LiteralNode(token)

    def _parse_integer(self) -> int:
        self._skip_spaces()
        start = self.index
        while not self._at_end() and self._peek().isdigit():
            self._advance()

        if start == self.index:
            raise RegexSyntaxError(
                f"Expected integer after '^' at position {self.index}"
            )

        return int(self.pattern[start:self.index])

    def _skip_spaces(self) -> None:
        while not self._at_end() and self._peek().isspace():
            self._advance()

    def _peek(self) -> Optional[str]:
        if self._at_end():
            return None
        return self.pattern[self.index]

    def _advance(self) -> None:
        self.index += 1

    def _at_end(self) -> bool:
        return self.index >= len(self.pattern)


class RegexWordGenerator:
    def __init__(self, pattern: str, max_repeat: int = 5) -> None:
        self.pattern = pattern
        self.max_repeat = max_repeat
        parser = RegexParser(pattern)
        self.tree = parser.parse()

    def generate(self, with_trace: bool = False, seed: Optional[int] = None):
        rng = random.Random(seed)
        context = GenerationContext(
            max_repeat=self.max_repeat,
            rng=rng,
            trace_enabled=with_trace,
            steps=[],
        )
        word = self.tree.generate(context)

        if with_trace:
            return word, context.steps
        return word

    def generate_many(self, count: int, seed: Optional[int] = None) -> List[str]:
        rng = random.Random(seed)
        words = []
        for _ in range(count):
            context = GenerationContext(
                max_repeat=self.max_repeat,
                rng=rng,
                trace_enabled=False,
                steps=[],
            )
            words.append(self.tree.generate(context))
        return words


def explain_generation(
    pattern: str,
    max_repeat: int = 5,
    seed: Optional[int] = None,
) -> Tuple[str, List[str]]:
    generator = RegexWordGenerator(pattern=pattern, max_repeat=max_repeat)
    word, steps = generator.generate(with_trace=True, seed=seed)
    return word, steps
