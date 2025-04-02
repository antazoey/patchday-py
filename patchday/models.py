from datetime import datetime

from pydantic import BaseModel

from patchday.types import (
    SiteID,
    HormoneID,
    ScheduleID,
    ExpirationDuration,
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

    expiration_duration: ExpirationDuration
    """
    The expiration duration.
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

    def __lt__(self, other: "Hormone") -> bool:
        expiration_date = self.expiration_date
        other_expiration_date = other.expiration_date
        if not other_expiration_date:
            return False

        elif not expiration_date:
            return True

        return expiration_date.__lt__(other_expiration_date)

    @property
    def active(self) -> bool:
        """
        True if this hormone has been applied.
        """
        return self.date_applied is not None

    @property
    def expired(self) -> bool:
        """
        True if this hormone needs to be re-applied.
        """
        if expiration_date := self.expiration_date:
            return expiration_date <= datetime.now()

        return False

    @property
    def expiration_date(self) -> datetime | None:
        """
        The date the hormone expires.
        """

        if not (date_applied := self.date_applied):
            # If not applied, it doesn't have an exp. date.
            return None

        return self.expiration_duration.date_from(date_applied)

    def apply(self, application: HormoneApplication | None = None):
        """
        Take the hormone.
        """
        application = application or HormoneApplication.from_hormone(self)
        self.date_applied = application.date
