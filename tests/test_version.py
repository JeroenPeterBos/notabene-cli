#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the version.py module.

.. currentmodule:: test_example
.. moduleauthor:: Jeroen Peter Bos <jeroen@notabene.cloud>

This is a sample test module.
"""


def test_version_import():
    """Test that we can import the version number."""
    from notabene.version import __version__  # pylint: disable=import-outside-toplevel

    assert all(map(lambda x: x.isdigit(), __version__.split(".")))


def test_release_import():
    """Test that we can import the release number."""
    from notabene.version import __release__  # pylint: disable=import-outside-toplevel

    assert all(map(lambda x: x.isdigit(), __release__.split(".")))
