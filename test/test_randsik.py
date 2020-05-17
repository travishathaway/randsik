"""
Tests for `randsik` module.
"""
import pytest
from randsik.randsik import Note, Pattern, Song, Chord


class TestRandsik:

    @classmethod
    def setup_class(cls):
        pass

    def test_happy_path(self):
        """
        Test the happy path for creating objects
        """
        notes = (
            ('A4', 127, 1/8),
            ('B4', 127, 1/8),
            ('C4', 127, 1/4),
        )

        pattern = Pattern([
            Note(*args) for args in notes
        ], tempo=120)

    @classmethod
    def teardown_class(cls):
        pass
