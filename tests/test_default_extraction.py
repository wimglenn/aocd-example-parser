from aocd.examples import Page

from aocd_example_parser.extraction import extract_examples



fake_prose = """
<title>Day 1 - Advent of Code 1234</title>
<article>
<pre><code>test input data</code></pre>
<code>test answer_a</code>
</article>
<article>
<code>test answer_b</code>
</article>
"""


def test_default_extraction_both_parts():
    page = Page.from_raw(html=fake_prose)
    examples = extract_examples(page)
    assert len(examples) == 1
    [example] = examples
    assert example.input_data == "test input data"
    assert example.answer_a == "answer_a"
    assert example.answer_b == "answer_b"
    assert example.extra is None


def test_default_extraction_part_a_only():
    i = fake_prose.rindex("<article>")
    prose_locked = fake_prose[:i]
    page = Page.from_raw(html=prose_locked)
    assert page.article_b is None
    examples = extract_examples(page)
    assert len(examples) == 1
    [example] = examples
    assert example.input_data == "test input data"
    assert example.answer_a == "answer_a"
    assert example.answer_b is None
    assert example.extra is None


def test_sequence_line_join(mocker):
    page = Page.from_raw(html=fake_prose)
    lines = "line1", "line2"
    mocker.patch("aocd_example_parser.extraction.eval", return_value=lines)
    [example] = extract_examples(page, use_default_locators=True)
    assert example.input_data == "line1\nline2"


def test_locator_crash(mocker):
    page = Page.from_raw(html=fake_prose)
    mock = mocker.patch("aocd_example_parser.extraction.eval", side_effect=Exception)
    examples = extract_examples(page, use_default_locators=True)
    assert examples == []
    assert mock.call_count == 3  # input_data, answer_a, answer_b
