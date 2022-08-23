"""Base cli setup and click extentions."""
import logging
import os
from pathlib import Path
from typing import List

import click

from notabene.version import __version__

log = logging.getLogger(__name__)


LOGGING_LEVELS = {
    -1: logging.NOTSET,
    0: logging.ERROR,
    1: logging.WARN,
    2: logging.INFO,
    3: logging.DEBUG,
}


class Project:
    """Project object that is used to pass information troughout the cli."""

    def __init__(self, log_level: int = logging.ERROR) -> None:
        """Create the `Project` object to be used troughout the cli."""
        self.log_level = log_level
        self.root = self._find_project_root()
        self.template_root = self.root / ".notabene" / "templates"
        self.notebook_root = self.root / "notebooks"

    def _find_project_root(self) -> Path:
        cwd = path = Path(os.getcwd())
        while not (path / "pyproject.toml").exists():
            if len(path.parents) == 0:
                return cwd
            path = path.parent
        return path

    def get_templates(self) -> List[Path]:
        """Get a list of all the available templates.

        Returns:
            List[Path]: A list of paths to all the templates.
        """
        templates = list(self.template_root.glob("*.ipynb"))

        if len(templates) > 0:
            log.info(
                "Retrieved %s templates from '%s'", len(templates), self.template_root
            )
        else:
            log.warning("No templates were found in '%s'", self.template_root)

        return sorted(templates)

    def get_notebooks(self) -> List[Path]:
        """Get a list of all the notebooks in the project.

        Returns:
            List[Path]: A list of paths to all the notebooks in this project.
        """
        notebooks = list(self.notebook_root.glob("*.ipynb"))

        if len(notebooks) > 0:
            log.info(
                "Retrieved %s notebooks from '%s'", len(notebooks), self.template_root
            )
        else:
            log.warning("No templates were found in '%s'", self.template_root)

        return sorted(notebooks)


@click.group()
@click.option(
    "--verbose", "-v", default=False, is_flag=True, help="Enable verbose output."
)
@click.option(
    "--debug", "-b", default=False, is_flag=True, help="Enable debugging output."
)
@click.pass_context
def base(ctx: click.Context, verbose: bool, debug: bool):
    """Run notabene."""
    log_level = None
    if verbose:
        log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG

    if log_level is not None:
        logging.basicConfig(level=log_level)
        log.info("Verbose logging. (Level %s)", logging.getLevelName(log_level))

    ctx.obj = Project(log_level=log_level)


@base.command()
@click.pass_obj
def info(project: Project):
    """Show information about the current project."""
    click.echo(click.style("Project contextual information:", fg="cyan", bold=True))
    properties = [
        a
        for a in dir(project)
        if not a.startswith("__")
        and not a.startswith("_")
        and not callable(getattr(project, a))
    ]
    for attr in sorted(properties):
        click.echo(f"{attr:<20}: {getattr(project, attr)}")


@base.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))
