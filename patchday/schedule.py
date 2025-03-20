from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING

from pydantic import BaseModel

from patchday.models import Hormone
from patchday.storage import ManagedData
from patchday.types import DeliveryMethod, ExpirationDuration, ScheduleID

if TYPE_CHECKING:
    from patchday.storage import PatchData


class Manager:
    def __init__(self, patchdata: "PatchData"):
        self.patchdata = patchdata


class ScheduleManager(Manager):
    _DB_KEY = "schedules"

    def __init__(self, patchdata: "PatchData", max_schedules: int = 10):
        self._max_schedules = max_schedules
        super().__init__(patchdata)

    def __iter__(self) -> "HormoneSchedule":
        yield from self.get_schedules()

    def __add__(self, other: dict) -> "HormoneSchedule":
        if not isinstance(other, dict):
            raise TypeError(
                f"Cannot add {type(self).__name__} to {type(other).__name__}"
            )

        self.create_schedule(**other)

    @cached_property
    def db(self) -> ManagedData:
        return self.patchdata.open(self._DB_KEY)

    def get_schedules(self) -> list["HormoneSchedule"]:
        """
        Get the schedules stored on the system.
        """
        return self.db.load_list(HormoneSchedule, patchdata=self.patchdata)

    def create_schedule(
        self,
        delivery_method: DeliveryMethod,
        expiration: ExpirationDuration,
        schedule_id: str | None = None,
        quantity: int = 1,
    ):
        """
        Create a new schedule.

        Args:
            delivery_method (DeliveryMethod): The delivery method to use.
            expiration (ExpirationDuration): The expiration duration to use.
            schedule_id (str): The ID of the schedule to create.
            quantity (int): The quantity of the schedule to create.
        """
        existing_schedules = self.get_schedules()
        if len(existing_schedules) == self._max_schedules:
            # The performance of this application assumes a small number of schedules.
            # However, smart enough users can change the max if they so desire.
            raise ValueError("Maximum schedules reached")

        if schedule_id is None:
            # Create a default one using the delivery method and existing schedules.
            matching_schedules = [
                s for s in existing_schedules if s.delivery_method == delivery_method
            ]
            index = len(matching_schedules)
            schedule_id = f"{delivery_method.lower().capitalize()} Schedule {index}"

        else:
            # Ensure it does not exist.
            for schedule in existing_schedules:
                if schedule.schedule_id == schedule_id:
                    raise ValueError(
                        f"Schedule already exists with ID '{schedule_id}'."
                    )

        new_schedule = HormoneSchedule(
            expiration_duration=expiration,
            delivery_method=delivery_method,
            schedule_id=schedule_id,
            quantity=quantity,
            patchdata=self.patchdata,
        )
        self.db.persist_list_object(new_schedule)


class HormoneSchedule(BaseModel):
    """
    The settings the build up a hormone schedule.
    """

    delivery_method: DeliveryMethod
    """
    The way to administer the hormones, such as transdermal
    patches or injections.
    """

    expiration_duration: ExpirationDuration
    """
    The length of time the hormones in this schedule take
    to expire.
    """

    schedule_id: ScheduleID
    """
    The ID of this schedule.
    """

    quantity: int = 1
    """
    The quantity of hormones in the schedule. The only
    delivery method where this value is not ``1`` is
    patches.
    """

    def __init__(self, **kwargs):
        patchdata: "PatchData" = kwargs.pop("patchdata")
        super().__init__(**kwargs)
        self._patchdata = patchdata

    @cached_property
    def _db_key(self) -> str:
        return self.delivery_method.value.lower()

    @cached_property
    def db(self) -> ManagedData:
        return self._patchdata.open(self._db_key)

    @property
    def hormones(self) -> list[Hormone]:
        existing_list = self.db.load_list(Hormone)
        self._validate_hormones(existing_list)
        return existing_list

    def _validate_hormones(self, existing_list: list[Hormone]):
        existing_size = len(existing_list)
        if existing_size == self.quantity:
            # It is good.
            return

        elif existing_size < self.quantity:
            self._init_default_hormones(existing_list)

        elif existing_size > self.quantity:
            # This should be an impossible state... but just in case, delete some.
            # TODO: Improve handling (e.g. delete less active objects, like new or
            #   super old.
            existing_list = existing_list[:self.quantity]
            self.db.persist_list_object(existing_list)

    def _init_default_hormones(self, existing_list: list[Hormone]):
        # NOTE: Assumes hormones size is less than the quantity defined in the schedule.

        # If we do 1 greater than the max, it should for sure be a unique ID.
        # Don't fear this number getting too big or worrying about gaps in IDs, it
        # doesn't really matter.
        max_id = max(existing_list, lambda h: h.hormone_id).hormone_id if existing_list else 0

        # Set defaults for any missing.
        did_add = False
        for idx in range(len(existing_list), self.quantity):
            hormone_id = max_id + idx
            default_hormone = Hormone(hormone_id=hormone_id)
            existing_list.append(default_hormone)
            did_add = True

        if did_add:
            # Persist the defaults so we don't have to generate them again.
            self.db.persist_list(existing_list)

