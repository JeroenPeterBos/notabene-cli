"""Utilities to make writing tests easier."""
import contextlib
import os
from pathlib import Path
from typing import Iterator

import click.testing
import pytest


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


@pytest.fixture
def pf_data_path(request):
    """Fixture that resolves the path to the test data directory."""
    test_file = Path(request.module.__file__)
    return test_file.parent / "data" / test_file.stem
