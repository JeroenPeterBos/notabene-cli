"""Utilities to make writing tests easier."""
import contextlib
import os
from pathlib import Path
from typing import Iterator

import click.testing


class CliRunner(click.testing.CliRunner):
    """CliRunner to test click applications."""

    @contextlib.contextmanager
    def enter_fixture(self, path: Path) -> Iterator["CliRunner"]:
        """Enter a path / fixture to invoke the commands from.

        Args:
            path (Path): The pytest fixture path

        Yields:
            Iterator[Path]: The path that is entered
        """
        cwd = Path().cwd()
        os.chdir(path)

        try:
            yield self
        finally:
            os.chdir(cwd)
