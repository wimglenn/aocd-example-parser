from aocd.examples import extract_examples
from aocd.examples import Example
from aocd.examples import Page


def plugin(page: Page, datas: list[str]) -> list[Example]:
    """
    Example parser implementation which always uses the aocd default locators.
    These are currently:

      "default_locators": {
        "input_data": "a_pre[0]",
        "answer_a":   "a_code[-1].split()[-1]",
        "answer_b":   "b_code[-1].split()[-1]",
        "extra":      null
      },

    The text of the first <pre> tag, if any, is the input data.
    The last <code> block of the first <article> contains the part a answer.
    The last <code> block of the second <article> contains the part b answer.
    The extra context is nothing.
    """
    return extract_examples(page.raw_html, use_default_locators=True)


def hardcoded_locations(page: Page, datas: list[str]) -> list[Example]:
    """
    Example parser implementation which always uses the pre-calculated locators.
    This implementation will always return correct results for puzzles which are
    published in the past. It can be used as a reference to compare the results of
    other example parser implementations against. For puzzles that hadn't been released
    yet, the results are the same as the "default locators" plugin defined above.
    """
    return extract_examples(page.raw_html)
