# -*- coding: utf-8 -*-
"""Testing the analysis of antonymy in by productive derivational
patterns."""

import unittest
import ldt

from ldt.helpers.ignore import ignore_warnings as ignore_warnings

# cat = ldt.relations.word.Word("cat")
irregular = ldt.relations.word.Word("irregular")
regular = ldt.relations.word.Word("regular")

test_dict = ldt.relations.antonymy_by_derivation.DerivationalAntonymy(
    language="English")

class Tests(unittest.TestCase):
    """
    The tests in this block inspect detection of antonymy via producuctive
    derivational patterns.
    """

    def test_init(self):
        """Test initialization."""
        self.assertEqual(test_dict.language, "en")

    def test_resources(self):
        """Test initialization."""
        self.assertIn("ir-", test_dict.prefixes)

