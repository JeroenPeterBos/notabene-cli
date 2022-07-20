#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests of the base cli commands.

.. currentmodule:: test_cli
.. moduleauthor:: Jeroen Peter Bos <jeroen@notabene.cloud>

This is the test module for the project's command-line interface (CLI)
module.
"""
import logging
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


def test_verbose_output(caplog):
    """Test the `version` subcommand with the '--verbose' option."""
    caplog.set_level(logging.INFO)

    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli, ["--verbose", "version"])
    logging_output = "\n".join(caplog.messages)

    assert result.exit_code == 0
    assert (
        "Verbose" in logging_output and "INFO" in logging_output
    ), "Verbose logging should be indicated in output."


def test_debug_output(caplog):
    """Test the `version` subcommand with the '--debug' option."""
    caplog.set_level(logging.DEBUG)

    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(cli, ["--debug", "version"])
    logging_output = "\n".join(caplog.messages)

    assert result.exit_code == 0
    assert (
        "Verbose" in logging_output and "DEBUG" in logging_output
    ), "Verbose logging should be indicated in output."
