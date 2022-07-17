#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests of the base cli commands.

.. currentmodule:: test_cli
.. moduleauthor:: Jeroen Peter Bos <jeroen@notabene.cloud>

This is the test module for the project's command-line interface (CLI)
module.
"""
from click.testing import CliRunner, Result

from notabene import __version__
from notabene.cli import cli


def test_version_displays_library_version():
    """Test the `version` subcommand."""
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli, ["version"])
    assert (
        __version__ in result.output.strip()
    ), "Version number should match library version."


def test_verbose_output():
    """Test the `version` subcommand with the '--verbose' option."""
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli, ["--verbose", "0", "version"])
    assert (
        "Verbose" in result.output.strip()
    ), "Verbose logging should be indicated in output."
