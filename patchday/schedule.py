from patchday.types import Hormone, Site


class HormoneSchedule:
    """
    Manage hormones.
    """

    def __init__(self, hormones: list[Hormone] | None = None):
        self.hormones: list[Hormone] = hormones or []

    def __iter__(self) -> list[Hormone]:
        return iter(self.hormones)


class SiteSchedule:
    """
    Manage sites in the hormone rotation.
    """

    def __init__(self, sites: list[Site] | None = None):
        self.sites: list[Site] = sites or []

    def __iter__(self) -> list[Site]:
        return iter(self.sites)
