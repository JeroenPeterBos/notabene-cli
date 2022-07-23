#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests of the base cli commands.

.. currentmodule:: test_cli
.. moduleauthor:: Jeroen Peter Bos <jeroen@notabene.cloud>

This is the test module for the project's command-line interface (CLI)
module.
"""
import logging
import shutil
from pathlib import Path

import pytest
from click.testing import Result

from notabene import __version__
from notabene.base import Project
from notabene.cli import cli
from tests.testing_utils import CliRunner


@pytest.fixture
def pf_data_path(request):
    """Fixture that resolves the path to the test data directory."""
    test_file = Path(request.module.__file__)
    return test_file.parent / "data" / test_file.stem


@pytest.fixture
def pf_empty(pf_data_path: Path, tmp_path: Path):
    """Fixture project with only a 'pyproject.toml' file."""
    shutil.copy(
        pf_data_path / "pyproject.toml",
        tmp_path,
    )
    return tmp_path


class TestVersion:
    """Test the 'version' command."""

    def test_version_displays_library_version(self):
        """Test the `version` subcommand."""
        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli, ["version"])
        assert (
            __version__ in result.output.strip()
        ), "Version number should match library version."

    def test_verbose_output(self, caplog):
        """Test the `version` subcommand with the '--verbose' option."""
        caplog.set_level(logging.INFO)

        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli, ["--verbose", "version"])
        logging_output = "\n".join(caplog.messages)

        assert result.exit_code == 0
        assert (
            "Verbose" in logging_output and "INFO" in logging_output
        ), "Verbose logging should be indicated in output."

    def test_debug_output(self, caplog):
        """Test the `version` subcommand with the '--debug' option."""
        caplog.set_level(logging.DEBUG)

        runner: CliRunner = CliRunner()
        result: Result = runner.invoke(cli, ["--debug", "version"])
        logging_output = "\n".join(caplog.messages)

        assert result.exit_code == 0
        assert (
            "Verbose" in logging_output and "DEBUG" in logging_output
        ), "Verbose logging should be indicated in output."


class TestProject:
    """Test the project class functionality."""

    def test_project_root_without_pyproject(self, tmp_path: Path):
        """Test finding project root without a pyproject file."""
        with CliRunner().enter_fixture(tmp_path):
            cwd = Path().cwd()
            project = Project()

            assert project.root == cwd

    def test_project_root_with_pyproject(self, pf_empty: Path):
        """Test finding project root without a pyproject file."""
        (pf_empty / "notebooks").mkdir(parents=True, exist_ok=True)
        with CliRunner().enter_fixture(pf_empty / "notebooks"):
            project = Project()

            assert project.root == pf_empty


class TestInfo:
    """Test the 'info' command."""

    def test_info_basic(self, pf_empty: Path):
        """Test basic functionality of the info command."""
        with CliRunner().enter_fixture(pf_empty) as runner:
            result = runner.invoke(cli, ["info"])

            assert result.exit_code == 0
