# -*- coding: utf-8 -*-
"""Testing the analysis of antonymy with productive derivational
patterns."""

import unittest
import ldt

from ldt.helpers.ignore import ignore_warnings as ignore_warnings

# cat = ldt.relations.word.Word("cat")
irregular = ldt.relations.word.Word("irregular")
regular = ldt.relations.word.Word("regular")
careful = ldt.relations.word.Word("careful")
careless = ldt.relations.word.Word("careless")
care = ldt.relations.word.Word("care")
cat = ldt.relations.word.Word("cat")
prewar = ldt.relations.word.Word("pre-war")
postwar = ldt.relations.word.Word("post-war")


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
        """Loading of resources."""
        self.assertIn("ir-", test_dict.resources["Prefixes"])

    def test_antonymy(self):
        """Detecting antonymy in prefixes."""
        self.assertTrue(test_dict.detect_antonymy(regular, irregular))

    def test_antonymy_reverse(self):
        """Detecting antonymy in prefixes."""
        self.assertTrue(test_dict.detect_antonymy(irregular, regular))

    def test_antonymy_sanity(self):
        """Sanity check for antonymy in prefixes."""
        self.assertFalse(test_dict.detect_antonymy(irregular, cat))

    def test_antonymy_suf(self):
        """Detecting antonymy in suffixes."""
        self.assertTrue(test_dict.detect_antonymy(care, careless))

    def test_antonymy_suf_reverse(self):
        """Detecting antonymy in suffixes in reverse."""
        self.assertTrue(test_dict.detect_antonymy(careless, care))

    def test_antonymy_suf_pair(self):
        """Detecting antonymy in suffix pairs."""
        self.assertTrue(test_dict.detect_antonymy(careful, careless))

    def test_antonymy_suf_pair_reverse(self):
        """Detecting antonymy in suffix pairs in reverse."""
        self.assertTrue(test_dict.detect_antonymy(careless, careful))

    def test_antonymy_pref_pair(self):
        """Detecting antonymy in prefix pairs."""
        self.assertTrue(test_dict.detect_antonymy(prewar, postwar))

    def test_antonymy_pref_pair_reverse(self):
        """Detecting antonymy in prefix pairs in reverse."""
        self.assertTrue(test_dict.detect_antonymy(postwar, prewar))

