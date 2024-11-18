from datetime import datetime
from importlib.metadata import version

from aocd_example_parser.extraction import _locators


def test_version_str():
    metadata_version = version("aocd-example-parser")
    date = datetime.strptime(metadata_version, "%Y.12.%d")
    assert date.year >= 2023
    assert 1 <= date.day <= 25
    latest = next(reversed(_locators()))
    year, day = map(int, latest.split("/"))
    assert date.year >= year
    assert date.day >= day
