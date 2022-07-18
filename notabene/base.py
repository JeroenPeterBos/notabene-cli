"""Base cli setup and click extentions."""
import logging
import os
from pathlib import Path
from typing import List

import click

from notabene.version import __version__

LOGGING_LEVELS = {
    -1: logging.NOTSET,
    0: logging.ERROR,
    1: logging.WARN,
    2: logging.INFO,
    3: logging.DEBUG,
}


class Project:
    """Project object that is used to pass information troughout the cli."""

    def __init__(self, verbose: int) -> None:
        """Create the `Project` object to be used troughout the cli.

        Args:
            verbose (int): The verbosity level for logging messages.
        """
        self.verbose = verbose
        self.root = self._find_project_root()
        self.template_dir = self.root / ".notabene" / "templates"

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
        return sorted(self.template_dir.glob("*.ipynb"))


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
    ctx.obj = Project(verbose=verbose)

    if verbose >= 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                "Verbose logging is enabled."
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )


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
