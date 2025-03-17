from patchday.schedule import HormoneSchedule, SiteSchedule
from cached_property import cached_property


class PatchDay:
    """
    The entry point PatchDay application class.
    """

    @cached_property
    def hormones(self) -> HormoneSchedule:
        """
        The schedule for managing hormones.
        """
        return HormoneSchedule()

    @cached_property
    def sites(self) -> SiteSchedule:
        """
        The schedule for managing sites.
        """
        return SiteSchedule()


patchday = PatchDay()
