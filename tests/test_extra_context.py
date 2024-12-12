from aocd.examples import Page

from aocd_example_parser.extraction import extract_examples


fake_prose = """
<title>Day 10 - Advent of Code 2016</title>
<article>
<pre><code>test input data</code></pre>
<code>test answer_a</code>
</article>
<article>
<code>test answer_b</code>
</article>
"""


def test_locator_extra_context():
    page = Page.from_raw(html=fake_prose)
    examples = extract_examples(page)
    [example] = examples
    assert example.extra == {"chip1": 5, "chip2": 2}
