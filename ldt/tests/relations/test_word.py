# -*- coding: utf-8 -*-
"""Testing the assembly of information from ld.dicts"""

import unittest
import ldt

from ldt.helpers.ignore import ignore_warnings as ignore_warnings

# cat = ldt.relations.word.Word("cat")
kindness = ldt.relations.word.Word("kindness")

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the loading of all the information from
    ldt.dicts for a given word.
    """

    def test_init(self):
        """Test initialization."""
        self.assertEqual(kindness.original_spelling, "kindness")

    def test_lemma(self):
        """Test lemma detection."""
        self.assertTrue(kindness.info["IsLemma"])

    def test_name(self):
        """Test lemma detection."""
        self.assertFalse(kindness.info["ProperNouns"])

    def test_number(self):
        """Test number detection."""
        self.assertFalse(kindness.info["Numbers"])

    def test_pos(self):
        """Test pos detection."""
        self.assertIn("noun", kindness.info["POS"])

    def test_affixes(self):
        """Test pos detection."""
        self.assertIn("-ness", kindness.info["Suffixes"])

    # def test_sem(self):
    #     """Test pos detection."""
    #     self.assertIn("feline", cat.info["Hypernyms"])

if __name__ == '__main__':
    unittest.main()
