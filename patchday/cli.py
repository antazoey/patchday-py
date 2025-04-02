import sys

import click
from typing import TYPE_CHECKING


import patchday
from patchday._click_ext import (
    expiration_option,
    delivery_method_option,
    quantity_option,
    prompt_for_quantity,
    schedule_option,
)
from patchday.date import format_date
from patchday.exceptions import ScheduleNotExistsError
from patchday.tui import launch_app

if TYPE_CHECKING:
    from patchday.types import DeliveryMethod


@click.group(invoke_without_command=True)
@click.pass_context
def app(ctx):
    if sys.argv[1:]:
        return

    launch_app()


@app.group()
def hormones():
    """
    take hormones
    """


@app.group()
def sites():
    """
    rotate sites
    """


@app.group(invoke_without_command=True)
def schedule():
    """
    manage schedules
    """
    if sys.argv[-1] == "schedule":
        _list_schedules()


@schedule.command("list")
def _list():
    """
    list schedules
    """
    _list_schedules()


def _list_schedules():
    for sched in list(patchday.schedules):
        if exp_date := sched.next_expired_hormone.expiration_date:
            suffix = format_date(exp_date)
        else:
            suffix = "not taken yet"

        click.echo(f"{sched.delivery_method.value} - {suffix}")


@schedule.command()
@schedule_option(help="name of the new schedule")
@delivery_method_option(prompt=True)
@expiration_option(prompt=True, default="3d12h")
@quantity_option()
def create(
    schedule_id: str,
    delivery_method: "DeliveryMethod",
    expiration: int,
    quantity: int | None,
):
    """
    make a schedule
    """
    from patchday.main import patchday
    from patchday.types import DeliveryMethod

    if delivery_method is DeliveryMethod.PATCH and quantity is None:
        # Only prompt for the quantity if the delivery method is 'patches'
        # and `--quantity` was not provided.
        quantity = prompt_for_quantity()

    patchday.schedules += {
        "delivery_method": delivery_method,
        "expiration": expiration,
        "schedule_id": schedule_id,
        "quantity": quantity,
    }

    click.echo("Creating a schedule with:")
    click.echo(f"\tdelivery_method: {delivery_method}")
    click.echo(f"\texpiration duration: {expiration}")

    if delivery_method is DeliveryMethod.PATCH:
        click.echo(f"\tnumber of patches: {quantity}")


@schedule.command()
@click.argument("schedule_id", required=False)
def remove(schedule_id):
    """
    delete a schedule
    """
    try:
        patchday.schedules.remove_schedule(schedule_id)
    except ScheduleNotExistsError as err:
        raise click.UsageError(f"{err}")

    click.echo(f"Successfully remove schedule '{schedule_id}'")
