from datetime import datetime

from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widget import Widget
from textual.widgets import Digits
import patchday


class ScheduleContainer(Widget):
    def compose(self):
        yield Digits("")


class PatchDay(App):
    CSS = """
        Screen { align: center middle; }
        Digits { width: auto; }
    """

    def compose(self) -> ComposeResult:
        schedules = [ScheduleContainer() for _ in patchday.schedules]
        yield VerticalScroll(*schedules)

    def on_ready(self) -> None:
        self.update_clock()

        # Update dates every minute so it works like a clock.
        self.set_interval(60, self.update_clock)

    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.query_one(Digits).update(f"{clock:%T}")


def launch_app():
    app = PatchDay()
    app.run()
