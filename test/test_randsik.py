"""
Tests for `randsik` module.
"""
import tempfile
import os

from randsik import Note, Pattern, QUARTER, WHOLE, SIXTEENTH, EIGHTH, generate


class TestRandsik:

    @classmethod
    def setup_class(cls):
        pass

    def test_pattern_happy_path(self):
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

        tf_str = tempfile.mktemp()
        pattern.save(tf_str)
        os.unlink(tf_str)

    def test_generate_happy_path(self):
        """
        Test the happy path for using the "generate" function to create a random pattern
        """
        pattern = generate()

        tf_str = tempfile.mktemp()
        pattern.save(tf_str)
        os.unlink(tf_str)

    @classmethod
    def teardown_class(cls):
        pass
