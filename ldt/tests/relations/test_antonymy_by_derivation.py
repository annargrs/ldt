# -*- coding: utf-8 -*-
"""Testing the analysis of antonymy with productive derivational
patterns."""

import unittest
import ldt

from ldt.helpers.ignore import ignore_warnings as ignore_warnings

class Tests(unittest.TestCase):
    """
    The tests in this block inspect detection of antonymy via producuctive
    derivational patterns.
    """

    @classmethod
    @ignore_warnings
    def setUpClass(cls):
        """Setting up the test variables."""
        cls.cat = ldt.relations.word.Word("cat")
        cls.irregular = ldt.relations.word.Word("irregular")
        cls.regular = ldt.relations.word.Word("regular")
        cls.careful = ldt.relations.word.Word("careful")
        cls.careless = ldt.relations.word.Word("careless")
        cls.care = ldt.relations.word.Word("care")
        cls.prewar = ldt.relations.word.Word("pre-war")
        cls.postwar = ldt.relations.word.Word("post-war")
        cls.test_dict = ldt.relations.antonymy_by_derivation.DerivationalAntonymy(
            language="English")

    @classmethod
    def tearDownClass(cls):
        """Clearning up the test variables."""
        cls.cat = None
        cls.irregular = None
        cls.regular = None
        cls.careful = None
        cls.careless = None
        cls.care = None
        cls.prewar = None
        cls.postwar = None
        cls.test_dict = None

    def test_init(self):
        """Test initialization."""
        self.assertEqual(self.test_dict.language, "en")

    def test_resources(self):
        """Loading of resources."""
        self.assertIn("ir-", self.test_dict.resources["Prefixes"])

    def test_antonymy(self):
        """Detecting antonymy in prefixes."""
        self.assertTrue(self.test_dict.detect_antonymy(self.regular,
                                                       self.irregular))

    def test_antonymy_reverse(self):
        """Detecting antonymy in prefixes."""
        self.assertTrue(self.test_dict.detect_antonymy(self.irregular,
                                                       self.regular))

    def test_antonymy_sanity(self):
        """Sanity check for antonymy in prefixes."""
        self.assertFalse(self.test_dict.detect_antonymy(self.irregular,
                                                       self.cat))

    def test_antonymy_suf(self):
        """Detecting antonymy in suffixes."""
        self.assertTrue(self.test_dict.detect_antonymy(self.care,
                                                       self.careless))

    def test_antonymy_suf_reverse(self):
        """Detecting antonymy in suffixes in reverse."""
        self.assertTrue(self.test_dict.detect_antonymy(self.careless,
                                                       self.care))

    def test_antonymy_suf_pair(self):
        """Detecting antonymy in suffix pairs."""
        self.assertTrue(self.test_dict.detect_antonymy(self.careful,
                                                    self.careless))

    def test_antonymy_suf_pair_reverse(self):
        """Detecting antonymy in suffix pairs in reverse."""
        self.assertTrue(self.test_dict.detect_antonymy(self.careless,
                                                    self.careful))

    def test_antonymy_pref_pair(self):
        """Detecting antonymy in prefix pairs."""
        self.assertTrue(self.test_dict.detect_antonymy(self.prewar,
                                                      self.postwar))

    def test_antonymy_pref_pair_reverse(self):
        """Detecting antonymy in prefix pairs in reverse."""
        self.assertTrue(self.test_dict.detect_antonymy(self.postwar,
                                                      self.prewar))

