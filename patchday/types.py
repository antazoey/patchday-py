from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator

SiteID = int
HormoneID = int


class HormoneApplication(BaseModel):
    """
    A model describing the application of a hormone.
    """

    hormone_id: HormoneID
    """
    The hormone being applied.
    """

    date: datetime
    """
    The date applied.
    """

    @classmethod
    def from_hormone(cls, hormone: "Hormone", **kwargs) -> "HormoneApplication":
        if "date" not in kwargs:
            kwargs["date"] = datetime.now()

        return HormoneApplication(hormone_id=hormone.hormone_id, **kwargs)

    @field_validator("date", mode="before")
    @classmethod
    def _validate_date(cls, value):
        return value or datetime.now()


class DeliveryMethod(str, Enum):
    PATCH = "PATCH"
    INJECTION = "INJECTION"
    PILL = "PILL"
    GEL = "GEL"


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

    delivery_method: DeliveryMethod = DeliveryMethod.PATCH
    """
    The method to deliver the hormone.
    """

    location: SiteID | None = None
    """
    The ID of the location of the site.
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
