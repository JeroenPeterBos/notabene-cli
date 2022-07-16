from pathlib import Path

import click

from notabene.base import base


@base.group()
@click.option(
    "--template-dir",
    "-t",
    type=click.Path(exists=True, file_okay=False),
    default="templates",
)
@click.pass_context
def template(ctx: click.Context, template_dir: click.Path):
    """Templates"""
    ctx.obj["template_dir"] = Path(template_dir)


@template.command()
@click.pass_context
def list(ctx: click.Context):
    """List all templates"""
    click.echo("The available templates in this project are:")
    for i, path in enumerate(ctx.obj["template_dir"].glob("*.ipynb")):
        click.echo(f"[{i:>2}]\t{path.stem}")


@template.command()
@click.pass_context
def context(ctx):
    """Get the context dictionary."""
    click.echo(ctx.obj)
