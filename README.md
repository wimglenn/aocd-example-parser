Advent-of-Code-Data Example Parser
==================================

The annual programming challenge [Advent of Code](https://adventofcode.com/) frequently provides some example data (and solutions) for you to test your code against, which are usually scaled-down versions of the real input data you're supposed to be solving with each day.

Although the real puzzle inputs and answers differ by user, the example data is written directly in the puzzle prose and is available to unauthenticated users too.

To illustrate what this means, the first puzzle of 2022 was [`--- Day 1: Calorie Counting ---`](https://adventofcode.com/2022/day/1) and it has the following example data (54 bytes):

```
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
```

The correct answers corresponding to this sample data were `24000` for part a, and `45000` for part b. The example data text was found in the first `<pre>` tag, and the answers were found in the last `<code>` blocks from each of the two `<article>` sections in the puzzle page HTML. Note that the first half of the puzzle must be solved before the second `<article>` tag shows up, so the second article is not visible to unauthenticated users.

In 2022, this same pattern of example data locations in the HTML was repeated for four more days, consecutively, before varying on [`--- Day 6: Tuning Trouble ---`](https://adventofcode.com/2022/day/6).


What is this package?
---------------------

This package provides an implementation of an [aocd example parser](https://github.com/wimglenn/advent-of-code-data/blob/main/aocd/examples.py) plugin, which attempts to parse the sample data and corresponding answers automatically from the puzzle prose.

An aocd example parser plugin is an [entry-point](https://packaging.python.org/en/latest/specifications/entry-points/) in the `"adventofcode.examples"` group. It must be a callable accepting two arguments, like this:

```python
from aocd.examples import Example
from aocd.examples import Page

def my_plugin(page: Page, datas: list[str]) -> list[Example]:
    """my example parser implementation"""
    ...
    # given the puzzle html found in "page", and a list of real user inputs found in
    # "datas" for potential comparison, the plugin function should scrape and return
    # a list of Example instances. Note that "datas" might be an empty list, if aocd
    # doesn't have any real user inputs cached locally.
    return result
```

This callable must return a list of `Example` instances. If no examples can be parsed, you should return an empty list `[]`, rather than `None`.

Any package providing an example parser should register an entry point in the `"adventofcode.examples"` group within the package metadata, by adding something like this in your `pyproject.toml` file:
```toml
[project.entry-points."adventofcode.examples"]
my_example_parser = "my_module:my_plugin"
```

See the [Entry points](https://peps.python.org/pep-0621/#entry-points) section in [_PEP 621 – Storing project metadata in pyproject.toml_](https://peps.python.org/pep-0621) for more information.

How to use/select a parser plugin?
----------------------------------

When an example parser package is correctly installed alongside [advent-of-code-data >= 2.0.0](https://github.com/wimglenn/advent-of-code-data), it will show up as a choice in `aoce --help`:

```bash
$ aoce --help
usage: aoce [-h] [-e {reference,simple}] [-y 2015+ [2015+ ...]] [-v]

options:
  -h, --help            show this help message and exit
  -e {reference,simple}, --example-parser {reference,simple}
                        plugin to use for example extraction testing (default: reference)
  -y 2015+ [2015+ ...], --years 2015+ [2015+ ...]
                        years to run the parser against (can specify multiple)
  -v, --verbose         increased logging (-v INFO, -vv DEBUG)
```

And it should be selectable for use/verification with

```bash
$ aoce --plugin=my_example_parser
```

To print the actual results produced by a parser against a single puzzle, you may use `aocd --example-parser`. To demonstrate using the results for [`--- Day 1: Calorie Counting ---`](https://adventofcode.com/2022/day/1) again:

```bash
$ aocd 2022 1 --example-parser=reference
                        --- Day 1: Calorie Counting ---
                      https://adventofcode.com/2022/day/1
------------------------------- Example data 1/1 -------------------------------
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
--------------------------------------------------------------------------------
answer_a: 24000
answer_b: 45000
--------------------------------------------------------------------------------
```


Why a plugin? Wouldn't it be simpler to write a parser in aocd directly?
------------------------------------------------------------------------

I've created this package, and the corresponding tester `aoce` in `advent-of-code-data`, to open it up to the community to try and come up with a better parser.
This package exemplifies the interface that a parser should work with, so to speak, and `aocd` uses this plugin for [dogfooding](https://en.wikipedia.org/wiki/Eating_your_own_dog_food). As an added benifit, it means the example parsing can be frequently updated to ensure correct results are returned for previous puzzles, without requiring a new release of `aocd` itself.

There are so many creative and smart people hacking on AoC that I'm sure several of you can come up with something much better than I was able to!
The default implementation from `aocd` fails more than 40% of the time, so you don't have a very high bar to beat.
If someone comes up with a better-performing parser than "_take the first pre as input data, take answers from the last codeblocks in each article_", I will make their implementation the new default in a future version of `aocd`.

If you're considering writing an example parser, it's not advisable to strive for 100% success rate, that will be super-difficult if not _impossible_.
Some of the puzzles have [many examples](https://adventofcode.com/2020/day/15), some are [really tricky to parse](https://adventofcode.com/2018/day/15), and some offer [no example at all](https://adventofcode.com/2018/day/21).
But difficulty aside, the main reason is that you needn't "overfit" to previous puzzles.
This is because `advent-of-code-data` always intends to return correct example data _for past puzzles_ by hardcoding the [relevant code-block locations](https://github.com/wimglenn/aocd-example-parser/blob/main/aocd_example_parser/examples.json). The unwritten rule is that `aocd-example-parser` versions 2023.* will return verified results for Advent of Code <= 2022, and unverified best-effort result for 2023+.

**The only thing that matters for a parser plugin is how well it can perform for a never-before seen puzzle**.
That is, the goal is to maximize the _probability_ that your parser will somehow find the right result at the instant a new puzzle unlocks.


How well does the default implementation perform?
-------------------------------------------------

It depends on the year.
The locations got a lot more consistent in recent years, so it has performed better more recently.
The final line that `aoce` script prints out is a rough percentage the parser got right.

```bash
$ for YEAR in {2015..2022};
do echo -n "$YEAR " && aoce -e simple -y $YEAR | tail -1;
done
2015 plugin 'simple' scored 78/336 (23.2%)
2016 plugin 'simple' scored 53/159 (33.3%)
2017 plugin 'simple' scored 85/221 (38.5%)
2018 plugin 'simple' scored 69/212 (32.5%)
2019 plugin 'simple' scored 43/204 (21.1%)
2020 plugin 'simple' scored 67/183 (36.6%)
2021 plugin 'simple' scored 82/152 (53.9%)
2022 plugin 'simple' scored 71/120 (59.2%)
```

Averaging across all years, we're currently right about a third of the time:

```bash
$ aoce -e simple | tail -1
plugin 'simple' scored 548/1587 (34.5%)
```

Of course, the "reference" plugin is always correct _for historical puzzles_.

```bash
$ aoce -e reference | tail -1
plugin 'reference' scored 1587/1587 (100.0%)
```
