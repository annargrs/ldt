# -*- coding: utf-8 -*-
"""Testing the analysis of relations in word pairs"""

import unittest
import ldt

from ldt.helpers.ignore import ignore_warnings as ignore_warnings

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the loading of all the information from
    ldt.dicts for a given word.
    """

    @classmethod
    @ignore_warnings
    def setUpClass(cls):
        """Setting up the test variables."""
        normalizer = ldt.dicts.normalize.Normalization(language="English",
                                                       order=("wordnet",
                                                              "custom"),
                                                       lowercasing=True)
        DerivationAnalyzer = ldt.dicts.derivation.meta.DerivationAnalyzer()
        LexDict = ldt.dicts.metadictionary.MetaDictionary()
        cls.test_dict = ldt.relations.pair.RelationsInPair(
            normalizer=normalizer, derivation_dict=DerivationAnalyzer,
            lex_dict=LexDict)


    @classmethod
    def tearDownClass(cls):
        """Clearning up the test variables."""
        cls.test_dict = None


    @ignore_warnings
    def test_numbers(self):
        """Test hashtag detection."""
        res = self.test_dict.analyze("one", "two")
        self.assertIn("Numbers", res)

    @ignore_warnings
    def test_urls(self):
        """Test hashtag detection."""
        res = self.test_dict.analyze("google.com", "yahoo.com")
        self.assertIn("URLs", res)

    # @ignore_warnings
    # def test_hashtags(self):
    #     """Test hashtag detection."""
    #     res = test_dict.analyze("#dog", "#cat")
    #     worked = "Hashtags" in res and "SharedPOS" in res
    #     self.assertTrue(worked)

    @ignore_warnings
    def test_deriv(self):
        """Test hashtag detection."""
        res = self.test_dict.analyze("kindness", "happiness")
        worked = "SharedPOS" in res and "SharedDerivation" in res and \
                 "SharedMorphForm" in res
        self.assertTrue(worked)

    @ignore_warnings
    def test_antonyms(self):
        """Test hashtag detection."""
        res = self.test_dict.analyze("beautiful", "ugly")
        worked = "SharedPOS" in res and "Antonyms" in res
        self.assertTrue(worked)

if __name__ == '__main__':
    unittest.main()
