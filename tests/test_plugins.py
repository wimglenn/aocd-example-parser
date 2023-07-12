from importlib.metadata import entry_points


def test_plugin(mocker):
    [ep] = entry_points().select(
        group="adventofcode.examples",
        name="aocd_examples_default",
    )
    plugin = ep.load()
    mock = mocker.patch("aocd_example_parser.extract_examples")
    plugin(page="fake page", datas=[])
    mock.assert_called_once_with("fake page", use_default_locators=True)


def test_canned(mocker):
    [ep] = entry_points().select(
        group="adventofcode.examples",
        name="aocd_examples_canned",
    )
    plugin = ep.load()
    mock = mocker.patch("aocd_example_parser.extract_examples")
    plugin(page="fake page", datas=[])
    mock.assert_called_once_with("fake page")
