from aocd.examples import Example
from aocd.examples import Page

from .extraction import extract_examples
from .util import real_datas_unused


__all__ = ["simple", "reference"]


@real_datas_unused
def simple(page: Page, datas: list[str]) -> list[Example]:
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
    return extract_examples(page, use_default_locators=True)


@real_datas_unused
def reference(page: Page, datas: list[str]) -> list[Example]:
    """
    Example parser implementation which always uses the pre-calculated locators.
    This implementation will always return correct results for puzzles which are
    published in the past. It can be used as a reference to compare the results of
    other example parser implementations against. For puzzles that hadn't been released
    yet, the results are the same as the "default locators" plugin defined above.
    """
    return extract_examples(page)
