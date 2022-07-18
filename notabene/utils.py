"""A collection file for utility functions."""
import re


def is_snake_case(s: str) -> bool:
    """Check if a string is written in snake case.

    Args:
        s (str): The string to check.

    Returns:
        bool: Whether the string is in snake case.
    """
    return re.match("^_?[a-z]+(_[a-z]+)*$", s)
