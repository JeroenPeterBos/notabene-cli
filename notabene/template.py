"""Template checking section of notabene cli."""

import click

from notabene.base import Project, base


@base.group()
@click.option(
    "--template-dir",
    "-t",
    type=click.Path(exists=True, file_okay=False),
)
@click.pass_obj
def template(project: Project, template_dir: click.Path):
    """Use, check and create templates."""
    if template_dir is not None:
        project.template_dir = template_dir


@template.command(name="list")
@click.pass_obj
def list_command(project: Project):
    """List all available templates."""
    click.echo(
        click.style(
            "The available templates in this project are:", fg="cyan", bold=True
        )
    )
    for i, path in enumerate(project.template_dir.glob("*.ipynb")):
        click.echo(f"[{i:>2}]\t{path.stem}")
