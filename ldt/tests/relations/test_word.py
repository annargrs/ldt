# -*- coding: utf-8 -*-
"""Testing the assembly of information from ld.dicts"""

import unittest
import ldt

from ldt.helpers.ignore import ignore_warnings as ignore_warnings

cat = ldt.relations.word.Word("cat")
kindness = ldt.relations.word.Word("kindness")

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the loading of all the information from
    ldt.dicts for a given word.
    """

    def test_init(self):
        """Test initialization."""
        self.assertEqual(cat.original_spelling, "cat")

    def test_lemma(self):
        """Test lemma detection."""
        self.assertTrue(cat.is_a_lemma)

    def test_name(self):
        """Test lemma detection."""
        self.assertFalse(cat.is_a_proper_noun)

    def test_number(self):
        """Test number detection."""
        self.assertFalse(cat.is_a_number)

    def test_pos(self):
        """Test pos detection."""
        self.assertIn("noun", cat.pos)

    def test_affixes(self):
        """Test pos detection."""
        self.assertIn("-ness", kindness.suffixes)

    def test_sem(self):
        """Test pos detection."""
        self.assertIn("feline", cat.semantics["hypernyms"])

if __name__ == '__main__':
    unittest.main()
