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

if TYPE_CHECKING:
    from patchday.types import DeliveryMethod


@click.group(invoke_without_command=True)
def app():
    schedules = list(patchday.schedules)
    if len(schedules) > 0:
        click.echo("best hrt ever")
        click.echo("~~~~~~~~~~~~~")
        click.echo("Your report:")

    else:
        click.echo("Hi! Want to manage your HRT using PatchDay?")

    # schedules = patchday.get_schedules()
    # if schedules:
    #     click.echo("Your schedules:")


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


@app.command(name="list")
def _list():
    """
    list schedules
    """
    click.echo(patchday.schedules.list())


@app.command()
@schedule_option(help="name of the new schedule")
@delivery_method_option(prompt=True)
@expiration_option(prompt="Expiration (e.g. 3d12h)")
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
