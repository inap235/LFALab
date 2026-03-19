import re
from typing import List
from regex_generator import RegexWordGenerator, explain_generation
VARIANT_3_REGEXES = [
    "O(P|Q|R)^+2(3|4)",
    "A*B(C|D|E)F(G|H|I)^2",
    "J^+K(L|M|N)*O?(P|Q)",
]

MAX_REPEAT = 5
SAMPLES_PER_REGEX = 10


def to_python_regex(pattern: str) -> str:
    no_spaces = "".join(pattern.split())
    no_spaces = no_spaces.replace("^+", "+")
    no_spaces = no_spaces.replace("^*", "*")
    no_spaces = no_spaces.replace("^?", "?")
    converted = re.sub(r"\^(\d+)", r"{\1}", no_spaces)
    return f"^{converted}$"


def verify_words(pattern: str, words: List[str]) -> bool:
    py_pattern = to_python_regex(pattern)
    return all(re.fullmatch(py_pattern, word) is not None for word in words)


def print_words(title: str, words: List[str]) -> None:
    print(f"\n{title}")
    print("{" + ", ".join(words) + "}")


def main() -> None:
    print("=" * 70)
    print("Regular Expressions Generator - Lab 4 (Variant 3)")
    print("=" * 70)
    print(f"Repetition limit for '*' and '+': {MAX_REPEAT}\n")

    all_valid = True

    for index, pattern in enumerate(VARIANT_3_REGEXES, start=1):
        generator = RegexWordGenerator(pattern=pattern, max_repeat=MAX_REPEAT)
        words = generator.generate_many(SAMPLES_PER_REGEX, seed=100 + index)
        valid = verify_words(pattern, words)
        all_valid = all_valid and valid

        print(f"Regex {index}: {pattern}")
        print_words("Generated words:", words)
        print(f"Validation against Python regex: {'OK' if valid else 'FAILED'}")
        print("-" * 70)

    print("\nBonus: sequence of processing example")
    trace_pattern = VARIANT_3_REGEXES[2]
    word, steps = explain_generation(trace_pattern, max_repeat=MAX_REPEAT, seed=7)
    print(f"Regex: {trace_pattern}")
    for step_number, step in enumerate(steps, start=1):
        print(f"Step {step_number}: {step}")
    print(f"Result: {word}")

    print("\nSummary:")
    print("All generated samples valid." if all_valid else "Some samples were invalid.")


if __name__ == "__main__":
    main()
