"""
Tests for `randsik` module.
"""
from randsik import Note, Pattern, QUARTER, EIGHTH, generate


def test_pattern_happy_path():
    """
    Test the happy path for creating objects
    """
    notes = (
        ('A4', 127, EIGHTH),
        ('B4', 127, EIGHTH),
        ('C4', 127, QUARTER),
    )

    pattern = Pattern([
        Note(*args) for args in notes
    ])

    assert pattern.track


def test_generate_happy_path():
    """
    Test the happy path for using the "generate" function to create a random pattern
    """
    pattern = generate()
    assert pattern.track
