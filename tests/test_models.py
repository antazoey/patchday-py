import pytest


from patchday.types import DeliveryMethod
from patchday.models import Hormone

HORMONE_ID = 1
SITE_ID = 1


@pytest.fixture
def patch():
    return Hormone(
        delivery_method=DeliveryMethod.PATCH,
        hormone_id=HORMONE_ID,
        location=SITE_ID,
    )


class TestHormone:
    def test_properties(self, patch):
        assert patch.hormone_id == HORMONE_ID
        assert patch.location == SITE_ID
        assert not patch.applied

    def test_apply(self, patch):
        assert not patch.applied
        patch.apply()
        assert patch.applied
        assert patch.date_applied is not None
