from datetime import datetime
from enum import Enum

from pydantic import BaseModel

SiteID = int
HormoneID = int


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


class Hormone(BaseModel):
    """
    Represents like a patch, injection, or gel.
    """

    date_applied: datetime | None = None
    """
    The date the hormone was applied or taken.
    """

    delivery_method: DeliveryMethod
    """
    The method to deliver the hormone.
    """

    hormone_id: HormoneID
    """
    The ID for lookup.
    """

    location: SiteID
    """
    The ID of the location of the site.
    """

    @property
    def applied(self) -> bool:
        """
        True if this hormone has been applied.
        """
        return self.date_applied is not None

    def apply(self):
        """
        Take the hormone.
        """
        self.date_applied = datetime.now()
