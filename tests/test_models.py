from datetime import timedelta

import pytest


from patchday.types import DeliveryMethod
from patchday.models import Hormone

HORMONE_ID = 1
SITE_ID = 1


@pytest.fixture
def patch():
    return Hormone(
        delivery_method=DeliveryMethod.PATCH,
        expiration_duration="3d12h",
        hormone_id=HORMONE_ID,
        location=SITE_ID,
    )


class TestHormone:
    def test_properties(self, patch):
        assert patch.hormone_id == HORMONE_ID
        assert patch.location == SITE_ID
        assert not patch.active

    def test_apply(self, patch):
        """
        Also tests ``.active`` property.
        """
        assert not patch.active
        assert patch.date_applied is None
        patch.apply()
        assert patch.active
        assert patch.date_applied is not None

    def test_expiration_date(self, patch):
        assert patch.expiration_date is None  # Inactive means no exp. date.
        patch.apply()  # Apply the patch.
        actual = patch.expiration_date
        expected = patch.date_applied + timedelta(days=3, hours=12)
        assert actual == expected

    def test_is_expired(self, patch):
        assert not patch.expired  # Inactive is also False
        patch.apply()  # Apply the patch.
        assert not patch.expired
        # Simulate having placed it 3 days and 12 hours ago.
        patch.date_applied -= timedelta(days=3, hours=12)
        assert patch.expired
