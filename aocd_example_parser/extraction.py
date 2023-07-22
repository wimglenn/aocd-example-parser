import importlib.resources
import json
from functools import cache

from aocd.examples import Example
from aocd.examples import Page

from .util import real_datas_unused


@real_datas_unused
def default(page: Page, datas: list[str]) -> list[Example]:
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
def canned(page: Page, datas: list[str]) -> list[Example]:
    """
    Example parser implementation which always uses the pre-calculated locators.
    This implementation will always return correct results for puzzles which are
    published in the past. It can be used as a reference to compare the results of
    other example parser implementations against. For puzzles that hadn't been released
    yet, the results are the same as the "default locators" plugin defined above.
    """
    return extract_examples(page)


@cache
def _locators() -> dict:
    # predetermined locations of code-blocks etc for example data
    resource = importlib.resources.files(__package__) / "examples.json"
    txt = resource.read_text()
    data = json.loads(txt)
    return data


def extract_examples(page: Page, use_default_locators: bool = False) -> list[Example]:
    """
    Takes the puzzle page's html and returns a list of `Example` instances.
    """
    scope = {"page": page}
    part_b_locked = page.article_b is None
    parts = "a" if part_b_locked else "ab"
    for part in parts:
        for tag in "code", "pre", "em", "li":
            name = f"{part}_{tag}"
            scope[name] = getattr(page, name)
    result = []
    locators = _locators()
    key = f"{page.year}/{page.day:02d}"
    default = locators["default_locators"]
    if use_default_locators:
        locs = [default]
    else:
        locs = locators.get(key, [default])
    for loc in locs:
        vals = []
        for k in "input_data", "answer_a", "answer_b", "extra":
            pos = loc.get(k, default[k])
            if k == "extra" and pos is None:
                break
            if k == "answer_b" and (part_b_locked or page.day == 25):
                vals.append(None)
                continue
            try:
                val = eval(pos, scope)
            except Exception:
                val = None
            if isinstance(val, (tuple, list)):
                val = "\n".join(val)
            if val is not None:
                val = val.rstrip("\r\n")
            vals.append(val)
        if vals[0] is not None:
            result.append(Example(*vals))
    return result
