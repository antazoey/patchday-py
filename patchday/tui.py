from typing import TYPE_CHECKING

from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widget import Widget
from textual.widgets import Label, Button
import patchday

if TYPE_CHECKING:
    from patchday.schedule import HormoneSchedule


class ScheduleContainer(Widget):
    schedule: "HormoneSchedule"

    @classmethod
    def from_schedule(cls, schedule: "HormoneSchedule") -> "HormoneSchedule":
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

        self.schedule.take_next_hormone()
        status_text = self.get_next_expiration_status()
        self.query_one("#take_label").update(status_text)

    def get_next_expiration_status(self) -> str:
        if next_exp := self.schedule.next_expired_hormone:
            if exp_date := next_exp.expiration_date:
                return f"Next expired: {exp_date}"

        return "Not yet taken!"

    def create_status_label(self) -> Label:
        status_text = self.get_next_expiration_status()
        return Label(status_text, id="take_label")

    def handle_take_button_pressed(self):
        self.schedule.take_next_hormone()


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
