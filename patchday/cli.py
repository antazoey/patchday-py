import json
import sys

import click
from typing import TYPE_CHECKING

import rich

import patchday
from patchday._click_ext import (
    expiration_option,
    delivery_method_option,
    quantity_option,
    prompt_for_quantity,
    schedule_option,
)
from patchday.schedule import HormoneSchedule

if TYPE_CHECKING:
    from patchday.types import DeliveryMethod


@click.group(invoke_without_command=True)
@click.pass_context
def app(ctx):
    if sys.argv[1:]:
        return

    schedules_list = list(patchday.schedules)
    if len(schedules_list) > 0:
        _output_schedules(schedules_list)

    else:
        click.echo("Hi! Want to manage your HRT using PatchDay?")


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


@app.command()
def schedules():
    """
    list schedules
    """
    if schedules_list := list(patchday.schedules):
        _output_schedules(schedules_list)
    else:
        click.echo("No schedules yet! Add one using the `create` method.")


def _output_schedules(schedules_list: list["HormoneSchedule"]):
    schedules_dict = {}
    for schedule in schedules_list:
        schedules_dict[schedule.schedule_id] = schedule.model_dump()

    json_str = json.dumps(schedules_dict, indent=2)
    rich.print(json_str)


@app.command()
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
