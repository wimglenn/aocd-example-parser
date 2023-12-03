#!/usr/bin/env python3
import pathlib
import sys

from testfixtures import compare

from aocd.models import Puzzle


here = pathlib.Path(__file__).parent
input_dir = here.parent.parent / "advent-of-code-wim" / "tests"


def remove_trailing_comments(lines):
    while lines and (not lines[-1].strip() or lines[-1].startswith("#")):
        lines.pop()
    if len(lines):
        lines[-1] = lines[-1].split("#")[0].strip()
    if len(lines) > 1:
        lines[-2] = lines[-2].split("#")[0].strip()


def main():
    rc = 0
    for puzzle in Puzzle.all():
        date = f"{puzzle.year}/{puzzle.day:02d}"
        example_dir = input_dir / date
        for i, example in enumerate(puzzle.examples):
            example_file = example_dir / f"{i}.txt"
            if not example_file.is_file():
                try:
                    [example_file] = example_dir.glob(f"{i}_*.txt")
                except ValueError:
                    print(f"missing example {i} {date}")
                    rc += 1
                    continue
            lines = example_file.read_text(encoding="utf-8").splitlines()
            remove_trailing_comments(lines)
            *lines, expected_answer_a, expected_answer_b = lines
            expected_input_data = "\n".join(lines).rstrip()
            result = [
                compare(example.input_data.rstrip(), expected_input_data.rstrip(), raises=False),
                compare(example.answer_a or "-", expected_answer_a, raises=False),
                compare(example.answer_b or "-", expected_answer_b, raises=False),
            ]
            for r in result:
                if r is not None:
                    print("incorrect", puzzle.url, r)
                    rc += 1
    sys.exit(rc)


if __name__ == "__main__":
    main()
