import importlib.resources
import json
from functools import cache

from aocd.examples import Example
from aocd.examples import Page


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
