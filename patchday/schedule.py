from functools import cached_property
from typing import TYPE_CHECKING

from pydantic import BaseModel

from patchday.storage import ManagedData
from patchday.types import DeliveryMethod, ExpirationDuration, ScheduleID

if TYPE_CHECKING:
    from patchday.storage import PatchData


class Manager:
    def __init__(self, patchdata: "PatchData"):
        self.patchdata = patchdata


class ScheduleManager(Manager):
    DB_KEY = "schedules"

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
        return self.patchdata.open(self.DB_KEY)

    def get_schedules(self) -> list["HormoneSchedule"]:
        """
        Get the schedules stored on the system.
        """
        return self.db.load_list(HormoneSchedule)

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
        )
        self.db.persist_list_object(self.DB_KEY, new_schedule)


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
