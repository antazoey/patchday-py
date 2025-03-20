from enum import Enum

from pydantic import RootModel, model_validator

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

    @property
    def plural_name(self) -> str:
        if self is DeliveryMethod.PATCH:
            return "patches"

        return f"{self.lower()}s"


class ExpirationDuration(RootModel[int]):
    """
    An expiration duration for hormones. It works like
    an integer except you can initialize it with shorthand
    strings such as ``"3d12h"``. Also, it's representation
    is the human-readable duration.
    """

    @model_validator(mode="before")
    @classmethod
    def validate_expiration_duration(cls, value: int | str) -> "ExpirationDuration":
        if isinstance(value, str):
            return parse_duration(value)
        elif isinstance(value, int):
            return value

        return int(value)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return format_duration(int(self))

    def __int__(self) -> int:
        return self.root


def validate_quantity(value: int) -> int:
    try:
        int_value = int(value)
    except Exception as err:
        raise TypeError(err)

    if int_value > MAX_QUANTITY or int_value < 0:
        raise ValueError(f"'{int_value}' out of bounds (max={MAX_QUANTITY}).")

    return int_value
