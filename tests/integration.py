#!/usr/bin/env python3
import argparse
import ast
import pathlib
import sys

from testfixtures import compare

from aocd.models import Puzzle


here = pathlib.Path(__file__).parent
input_dir = here.parent.parent / "advent-of-code-wim" / "tests"


def split_trailing_comments(lines):
    extra = []
    while lines and (not lines[-1].strip() or lines[-1].startswith("#")):
        extra.append(lines.pop())
    if len(lines) and "#" in lines[-1]:
        line, comment = lines[-1].split("#", 1)
        lines[-1] = line.strip()
        extra.append(comment.strip())
    if len(lines) > 1 and "#" in lines[-2]:
        line, comment = lines[-2].split("#", 1)
        lines[-2] = line.strip()
        extra.append(comment.strip())
    extra = [x.strip() for x in extra if x.strip()]
    return extra


def parse_extra_context(extra):
    result = {}
    for line in extra:
        equals = line.count("=")
        commas = line.count(",")
        if equals and equals == commas + 1:
            for part in line.split(","):
                k, v = part.strip().split("=")
                k = k.strip()
                v = v.strip()
                try:
                    v = ast.literal_eval(v)
                except ValueError:
                    pass
                if k in result:
                    raise NotImplementedError(f"Duplicate key {k!r}")
                result[k] = v
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    rc = 0
    for puzzle in Puzzle.all():
        date = f"{puzzle.year}/{puzzle.day:02d}"
        example_dir = input_dir / date
        egs = [x.name.split(".")[0] for x in example_dir.glob("*.txt")]
        n_examples_expected = max([1 + int(x) for x in egs if x.isdigit()], default=0)
        if len(puzzle.examples) != n_examples_expected:
            print(f"{date} {n_examples_expected=} but {len(puzzle.examples)=}")
            rc += 1
        for i, example in enumerate(puzzle.examples):
            example_file = example_dir / f"{i}.txt"
            if not example_file.is_file():
                try:
                    [example_file] = example_dir.glob(f"{i}.*.txt")
                except ValueError:
                    print(f"missing example {i} {date}")
                    rc += 1
                    continue
            lines = example_file.read_text(encoding="utf-8").splitlines()
            extra = split_trailing_comments(lines)
            expected_extra = parse_extra_context(extra)
            *lines, expected_answer_a, expected_answer_b = lines
            expected_input_data = "\n".join(lines).rstrip()
            diff = compare(
                actual=example.input_data.rstrip(),
                expected=expected_input_data.rstrip(),
                raises=False
            )
            if diff is not None:
                print(f"incorrect example data ({i}) for", puzzle.url, diff)
                rc += 1
            for part in "ab":
                diff = compare(
                    actual=getattr(example, f"answer_{part}") or "-",
                    expected=locals()[f"expected_answer_{part}"],
                    raises=False,
                )
                if diff is not None:
                    print(f"incorrect answer {part} ({i}) for", puzzle.url, diff)
                    rc += 1
            if example.extra or expected_extra:
                diff = compare(
                    actual=example.extra,
                    expected=expected_extra,
                    raises=False,
                )
                if diff is not None:
                    print(f"incorrect extra ({i}) for", puzzle.url, diff)
                    rc += 1
            if args.verbose:
                print("OK", example_file)
    sys.exit(rc)


if __name__ == "__main__":
    main()
