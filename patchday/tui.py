from typing import TYPE_CHECKING

from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widget import Widget
from textual.widgets import Label, Button
import patchday
from patchday.date import format_date

if TYPE_CHECKING:
    from patchday.schedule import HormoneSchedule


class BaseWidget(Widget):
    def update_peer(self, selector_id: str, *args, **kwargs):
        self.query_one(f"#{selector_id}").update(*args, **kwargs)  # type: ignore


class ScheduleContainer(BaseWidget):
    schedule: "HormoneSchedule"

    @classmethod
    def from_schedule(cls, schedule: "HormoneSchedule") -> "ScheduleContainer":
        instance = cls()
        instance.schedule = schedule
        return instance

    def compose(self):
        yield Label(self.schedule.schedule_id)
        yield self.create_status_label()
        yield Button("Take", id="take_button")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "take_button":
            # Not the right button pressed.
            return

        self.handle_take_button_pressed()

    def get_next_expiration_status(self) -> str:
        next_hormone = self.schedule.next_expired_hormone
        if exp_date := next_hormone.expiration_date:
            if last_taken := self.schedule.last_taken_hormone:
                if last_taken_date := last_taken.date_applied:
                    return (
                        f"Last taken: {format_date(last_taken_date)}\n"
                        f"Next expiration: {format_date(exp_date)}"
                    )

        return "Not yet taken!"

    def create_status_label(self) -> Label:
        status_text = self.get_next_expiration_status()
        return Label(status_text, id="take_label")

    def handle_take_button_pressed(self):
        self.schedule.take_next_hormone()
        status_text = self.get_next_expiration_status()
        self.update_peer("take_label", status_text)


class PatchDay(App):
    CSS = """
        Screen { align: center middle; }
        Label { width: auto; }
    """

    def compose(self) -> ComposeResult:
        yield Label("best hrt ever\n~~~~~~~")

        schedules = [
            ScheduleContainer.from_schedule(schedule) for schedule in patchday.schedules
        ]

        yield VerticalScroll(*schedules)

    def on_ready(self) -> None:
        self.update_dates()

        # Update dates every minute so it works like a clock.
        self.set_interval(60, self.update_dates)

    def update_dates(self) -> None:
        # TODO
        pass


def launch_app():
    app = PatchDay()
    app.run()
