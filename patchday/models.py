from datetime import datetime

from pydantic import BaseModel
from patchday.types import (
    SiteID,
    HormoneID,
    ScheduleID,
)


class HormoneApplication(BaseModel):
    """
    A model describing the application of a hormone.
    """

    hormone_id: HormoneID
    """
    The hormone being applied.
    """

    date: datetime | None
    """
    The date applied. If `None`, the hormone has never been applied
    (new schedule or changing a schedule's quantity setting).
    """

    @classmethod
    def from_hormone(cls, hormone: "Hormone", **kwargs) -> "HormoneApplication":
        if "date" not in kwargs:
            kwargs["date"] = datetime.now()

        return HormoneApplication(hormone_id=hormone.hormone_id, **kwargs)


class Site(BaseModel):
    """
    Represents a location on the body to apply hormones.
    """

    site_id: SiteID
    """
    The identifier of the site.
    """


class Hormone(BaseModel):
    """
    Represents like a patch, injection, or gel.
    """

    hormone_id: HormoneID
    """
    The ID for lookup.
    """

    date_applied: datetime | None = None
    """
    The date the hormone was applied or taken.
    """

    location: SiteID | None = None
    """
    The ID of the location of the site.
    """

    schedule_id: ScheduleID | None = None
    """
    The ID of the schedule this hormone belongs to.
    """

    @property
    def applied(self) -> bool:
        """
        True if this hormone has been applied.
        """
        return self.date_applied is not None

    def apply(self, application: HormoneApplication | None = None):
        """
        Take the hormone.
        """
        application = application or HormoneApplication.from_hormone(self)
        self.date_applied = application.date
