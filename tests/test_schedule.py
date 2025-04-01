from datetime import datetime, timedelta

from patchday.models import Hormone
from patchday.schedule import HormoneSchedule
import pytest

from patchday.types import DeliveryMethod


@pytest.fixture
def patches_db(mocker, mock_data):
    db = mocker.MagicMock()
    db.load_list.return_value = [
        create_patch(0),
        create_patch(1),
        create_patch(2),
    ]
    return db


def create_patch(idx) -> Hormone:
    return Hormone(
        delivery_method=DeliveryMethod.PATCH,
        expiration_duration="3d12h",
        hormone_id=idx,
    )


@pytest.fixture(autouse=True)
def patch_data(mocker, mock_data, patches_db):
    def open_fn(key):
        if key == "patch":
            return patches_db

        return mocker.MagicMock()

    mock_data.open.side_effect = open_fn
    return mock_data


@pytest.fixture
def schedule(mock_data):
    return HormoneSchedule(
        delivery_method=DeliveryMethod.PATCH,
        expiration_duration="3d12h",
        schedule_id="My Schedule",
        quantity=3,
        patchdata=mock_data,
    )


class TestHormoneSchedule:
    def test_hormones(self, schedule):
        assert len(schedule.hormones) == 3

    def test_active_hormones(self, schedule):
        assert len(schedule.active_hormones) == 0

        # Activate them all.
        for hormone in schedule.hormones:
            hormone.apply()

        assert len(schedule.active_hormones) == 3

    def test_expired_hormones(self, schedule):
        assert schedule.expired_hormones == []
        hormone = schedule.hormones[0]
        hormone.date_applied = datetime.now() - timedelta(days=4)
        assert schedule.expired_hormones == [hormone]

    def test_next_expired_hormone(self, schedule):
        assert schedule.next_expired_hormone is None

        # Make up dates.
        now = datetime.now()
        offset = 1
        hormone = None
        for hormone in schedule.hormones:
            hormone.date_applied = now - timedelta(days=offset)
            offset += 1

        # The last hormone in the loop is the expected next expired.
        assert schedule.next_expired_hormone is hormone
