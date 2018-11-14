# -*- coding: utf-8 -*-
"""Testing the analysis of relations in word pairs"""

import unittest
import os

os.environ["TESTING_LDT"] = "TRUE"

import ldt

from ldt.helpers.ignore import ignore_warnings

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
        LexDict = ldt.dicts.semantics.metadictionary.MetaDictionary()
        cls.test_dict = ldt.relations.pair.RelationsInPair(
            normalizer=normalizer, derivation_dict=DerivationAnalyzer,
            lex_dict=LexDict)
        # cls.test_dict2 = ldt.relations.pair.RelationsInPair(
        #     normalizer=normalizer, derivation_dict=DerivationAnalyzer,
        #     lex_dict=LexDict, distr_dict="None")

    @classmethod
    def tearDownClass(cls):
        """Clearning up the test variables."""
        cls.test_dict = None
        # cls.test_dict2 = None

    @ignore_warnings
    def test_paths(self):
        """Test hashtag detection."""
        res = self.test_dict.analyze("working", "class")
        self.assertEqual(res["ShortestPath"], 0.0625)

    @ignore_warnings
    def test_associations(self):
        """Test hashtag detection."""
        res = self.test_dict.analyze("falcons", "eagle")
        self.assertEqual(res["Associations"], True)

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

    @ignore_warnings
    def test_associations(self):
        """Test hashtag detection."""
        res = self.test_dict.analyze("falcon", "eagle")
        worked = "SharedPOS" in res and "Associations" in res
        self.assertTrue(worked)

    # @ignore_warnings
    # def test_gdeps(self):
    #     """Test gdeps cooccurrence."""
    #     res = self.test_dict.analyze("walk", "quickly")
    #     self.assertIn("GDeps", res)

    # @ignore_warnings
    # def test_cooccurrence(self):
    #     """Test corpus cooccurrence."""
    #     res = self.test_dict.analyze("walk", "quickly")
    #     self.assertIn("NonCooccurring", res)

    # @ignore_warnings
    # def test_cooccurrence(self):
    #     """Test frequency retrieval."""
    #     res = self.test_dict.analyze("walk", "quickly")
    #     self.assertEqual(res["TargetFrequency"], 20)
    #
    # @ignore_warnings
    # def test_cooccurrence(self):
    #     """Test frequency retrieval."""
    #     res = self.test_dict2.analyze("walk", "quickly")
    #     self.assertNotIn("TargetFrequency", res)

if __name__ == '__main__':
    unittest.main()
