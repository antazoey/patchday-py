from pathlib import Path

from functools import cached_property

from patchday.schedule import ScheduleManager
from patchday.storage import PatchData


class PatchDay:
    """
    The entry point PatchDay application class.
    """

    def __init__(self, storage_path: Path | None = None):
        self._storage_path = storage_path

    @cached_property
    def _db(self) -> PatchData:
        return PatchData(path=self._storage_path)

    @cached_property
    def schedules(self) -> ScheduleManager:
        return ScheduleManager(self._db)


patchday = PatchDay()
