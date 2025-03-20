import pytest

from patchday.date import parse_duration, format_duration, DAY


@pytest.mark.parametrize(
    "duration_str,expected",
    [(f"{DAY}", DAY), ("1d", DAY), ("1d1s", DAY + 1), ("1d1h1s", DAY + (60 * 60) + 1)],
)
def test_parse_duration(duration_str, expected):
    actual = parse_duration(duration_str)
    assert actual == expected


@pytest.mark.parametrize("bad_input", ("asdfasdf", "BAD INPUT"))
def test_parse_duration_error(bad_input):
    with pytest.raises(ValueError):
        parse_duration(bad_input)


@pytest.mark.parametrize(
    "duration,expected",
    [(DAY, "1d"), (302400, "3d12h"), (0, "0s")],
)
def test_format_duration(duration, expected):
    actual = format_duration(duration)
    assert actual == expected
