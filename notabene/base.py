import logging

import click

from notabene.version import __version__

LOGGING_LEVELS = {
    -1: logging.NOTSET,
    0: logging.ERROR,
    1: logging.WARN,
    2: logging.INFO,
    3: logging.DEBUG,
}


@click.group()
@click.option(
    "--verbose",
    "-v",
    default=-1,
    type=int,
    help="Enable verbose output, use 0, 1, 2, 3 for ERROR, WARN, INFO, DEBUG.",
)
@click.pass_context
def base(ctx: click.Context, verbose: int):
    """Run notabene."""
    if verbose >= 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. (LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    ctx.obj = dict()
    ctx.obj["verbose"] = verbose


@base.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))
