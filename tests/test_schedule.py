from patchday.schedule import HormoneSchedule
from patchday.types import Hormone, Site


class TestHormoneSchedule:
    def test_list(self):
        hormone = Hormone(hormone_id=0)
        schedule = HormoneSchedule([hormone])
        actual = list(schedule)
        assert actual == [hormone]


class TestSiteSchedule:
    def test_list(self):
        hormone = Site(site_id=0)
        schedule = HormoneSchedule([hormone])
        actual = list(schedule)
        assert actual == [hormone]
