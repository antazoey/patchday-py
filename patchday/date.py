import re


DURATION_PATTERN = re.compile(r"(\d+)([dhmsw])")
MINUTE = 60
HOUR = 3600
DAY = 86400
WEEK = DAY * 7


def parse_duration(duration_str: str | int) -> int:
    """
    Given the given duration string to an amount in seconds.
    Example inputs are like ``1w`` or ``3d12h``.

    Args:
        duration_str: The duration string to parse.

    Returns:
        int: The amount in seconds.
    """
    if isinstance(duration_str, int):
        return duration_str

    elif not isinstance(duration_str, str):
        if hasattr(duration_str, "value"):
            # Hack to ExpirationDuration objects works here.
            return int(duration_str)

        raise TypeError(duration_str)

    elif duration_str.isnumeric() or isinstance(duration_str, int):
        # Given seconds only.
        return int(duration_str)

    elif any(not x.isnumeric() and x not in ("d", "h", "m", "s") for x in duration_str):
        raise ValueError(
            f"Invalid duration format {duration_str}. Expecting strings like '3d12h'."
        )

    # Amass up the seconds from the shorthands.
    total_seconds = 0
    pattern = r"(\d+)([d|h|m|s|w])"

    for match in re.finditer(pattern, duration_str.strip().lower()):
        amount = int(match.group(1))
        unit = match.group(2)

        if unit == "s":
            total_seconds += amount
        elif unit == "m":
            total_seconds += amount * 60
        elif unit == "h":
            total_seconds += amount * 3600
        elif unit == "d":
            total_seconds += amount * DAY
        elif unit == "w":
            total_seconds += amount * DAY * 7

    return total_seconds


def format_duration(seconds: int) -> str:
    """
    Convert the given duration integer to a human-readable string.

    Args:
        seconds: The amount in seconds to format.

    Returns:
        str: The formatted duration e.g. `"3d12h"`.
    """
    weeks = seconds // WEEK
    seconds %= WEEK
    days = seconds // DAY
    seconds %= DAY
    hours = seconds // HOUR
    seconds %= HOUR
    minutes = seconds // MINUTE
    seconds %= MINUTE

    result = []
    if weeks > 0:
        result.append(f"{weeks}w")
    if days > 0:
        result.append(f"{days}d")
    if hours > 0:
        result.append(f"{hours}h")
    if minutes > 0:
        result.append(f"{minutes}m")
    if seconds > 0:
        result.append(f"{seconds}s")

    return "".join(result) if result else "0s"
