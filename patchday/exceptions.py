class PatchDayException(Exception):
    """
    Base exception class for PatchDay.
    """


class StorageCorruption(PatchDayException):
    """
    A storage item may be corrupted.
    """

    def __init__(self, storage_key: str, reason: str) -> None:
        super().__init__(f"Storage '{storage_key}' is corrupted: {reason}'")


class ScheduleNotExistsError(PatchDayException):
    def __init__(self, schedule_id: str) -> None:
        super().__init__(f"Schedule '{schedule_id}' does not exist.")
