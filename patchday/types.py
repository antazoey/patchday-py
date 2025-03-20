from enum import Enum

from pydantic_core import core_schema

from patchday.constants import MAX_QUANTITY
from patchday.date import parse_duration, format_duration

# Can be custom.
ScheduleID = str

# Only system set.
HormoneID = int
SiteID = int


class DeliveryMethod(str, Enum):
    PATCH = "PATCH"
    INJECTION = "INJECTION"
    PILL = "PILL"
    GEL = "GEL"


class ExpirationDuration:
    """
    An expiration duration for hormones. It works like
    an integer except you can initialize it with shorthand
    strings such as ``"3d12h"``. Also, it's representation
    is the human-readable duration.
    """

    def __init__(self, value: int | str):
        if isinstance(value, str):
            self.value = parse_duration(value)
        elif isinstance(value, int):
            self.value = value
        elif hasattr(value, "value"):
            self.value = value.value
        else:
            raise TypeError(value)

    def __repr__(self) -> str:
        return format_duration(self.value)

    def __int__(self) -> int:
        return self.value

    def __eq__(self, other) -> bool:
        if isinstance(other, ExpirationDuration):
            return self.value == other.value

        elif isinstance(other, int):
            return self.value == other

        elif isinstance(other, str):
            return self.value == parse_duration(other)

        raise TypeError(other)

    def __get_pydantic_core_schema__(self, _source):
        return core_schema.int_schema()


def validate_quantity(value: int) -> int:
    try:
        int_value = int(value)
    except Exception as err:
        raise TypeError(err)

    if int_value > MAX_QUANTITY or int_value < 0:
        raise ValueError(f"'{int_value}' out of bounds (max={MAX_QUANTITY}).")

    return int_value
