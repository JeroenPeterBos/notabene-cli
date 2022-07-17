"""Template checking section of notabene cli."""

import logging
import shutil
from pathlib import Path
from typing import List

import click

from notabene.base import Project, base

log = logging.getLogger(__name__)


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


def _list_templates(template_dir: Path):
    return sorted(template_dir.glob("*.ipynb"))


def _echo_templates(templates: List[Path]):
    click.secho("The available templates in this project are:", fg="cyan", bold=True)
    for i, path in enumerate(templates):
        click.echo(f"[{i:>2}]\t{path.stem}")


@template.command(name="list")
@click.pass_obj
def list_command(project: Project):
    """List all of your templates."""
    _echo_templates(_list_templates(project.template_dir))


@template.command()
@click.option(
    "--template",
    "-t",
    type=str,
    default="",
    help="The name or index of a template. An option prompt is shown by default.",
)
@click.argument("notebook", type=str)
@click.pass_obj
def use(project: Project, template: str, notebook: str):
    """Create a new notebook using one of your templates.

    NOTEBOOK is the name of the new notebook. Adding `.ipynb` is optional.
    """
    notebook = Path(notebook).with_suffix(".ipynb")
    if notebook.exists():
        raise click.BadArgumentUsage(f"The file '{notebook}' already exists.")

    templates = _list_templates(project.template_dir)
    if template == "":
        _echo_templates(templates)
        while True:
            template = click.prompt("Select one of your templates", default=0, type=int)
            if 0 <= template < len(templates):
                break
            click.echo(f"Error: Template index '{template}' does not exist.")
        template_path = templates[template]
    elif template.isdigit():
        if 0 <= int(template) < len(templates):
            template_path = templates[int(template)]
        else:
            raise click.BadOptionUsage(
                option_name="template",
                message=f"Template index '{template}' does not exist. "
                "Leave empty or call the list command to get a list of options.",
            )
    else:
        for path in templates:
            if path.stem == template:
                template_path = path
                break
        else:
            raise click.BadOptionUsage(
                option_name="template",
                message=f"Template name '{template}' does not exist. "
                "Leave empty or call the list command to get a list of options.",
            )
    log.info("Using template located at %s", template_path)

    notebook.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(template_path, notebook)
    click.secho(
        f"Created new notebook '{notebook}' using template '{template_path.stem}'.",
        fg="cyan",
        bold=True,
    )
