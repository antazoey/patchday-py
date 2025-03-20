import click
from click import Choice, option


def schedule_option(**kwargs):
    if "help" not in kwargs:
        kwargs["help"] = "id of a schedule"

    return click.option("--schedule-id", **kwargs)


class DeliveryMethodChoice(Choice):
    def __init__(self):
        from patchday.types import DeliveryMethod

        super().__init__([x.value for x in DeliveryMethod], case_sensitive=False)


def delivery_method_option(**kwargs):
    if "help" not in kwargs:
        kwargs["help"] = "pill, patch, injection, gel"

    return option(
        "--delivery-method",
        "-dm",
        type=DeliveryMethodChoice(),
        **kwargs,
    )


def expiration_option(**kwargs):
    if "help" not in kwargs:
        kwargs["help"] = "time between dose"

    return option(
        "--expiration",
        "-x",
        **kwargs,
    )


def quantity_option(**kwargs):
    def callback(ctx, param, value):
        if value is None:
            return None

        from patchday.types import DeliveryMethod, validate_quantity

        int_value = validate_quantity(value)
        delivery_method = ctx.params.get("delivery_method")
        if int_value != 1 and delivery_method != DeliveryMethod.PATCH:
            raise click.BadOptionUsage(
                "--quantity",
                f"'--quantity' only applicable for patches; not {delivery_method}.",
            )

        return int_value

    return option(
        "--quantity",
        "-q",
        type=int,
        help="amount of patches",
        callback=callback,
        default=1,
        **kwargs,
    )


def prompt_for_quantity() -> int:
    from patchday.types import validate_quantity

    value = click.prompt("Enter the number of patches you use")
    while True:
        try:
            return validate_quantity(value)
        except Exception as err:
            click.echo(f"Invalid quantity '{value}'. Problem: {err}")
            value = click.prompt("Enter the number of patches you use")
