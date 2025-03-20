import pytest

from patchday.date import DAY
from patchday.types import ExpirationDuration


class TestExpirationDuration:
    @pytest.mark.parametrize(
        "value,expected",
        [
            (f"{DAY}", DAY),
            ("1d", DAY),
            ("1d1s", DAY + 1),
            ("1d1h1s", DAY + (60 * 60) + 1),
        ],
    )
    def test_init(self, value, expected):
        actual = ExpirationDuration(value)
        assert actual == expected

    @pytest.mark.parametrize(
        "duration,expected",
        [(DAY, "1d"), (302400, "3d12h"), (0, "0s")],
    )
    def test_repr(self, duration, expected):
        duration = ExpirationDuration(duration)
        actual = repr(duration)
        assert actual == expected
