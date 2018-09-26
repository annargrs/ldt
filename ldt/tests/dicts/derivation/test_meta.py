# -*- coding: utf-8 -*-

import unittest
import time
import ldt

from ldt.helpers.ignore import ignore_warnings

test_dict = ldt.dicts.derivation.meta.DerivationAnalyzer(language="en")

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the retrieval of all derivational
    information.
    """

    @classmethod
    @ignore_warnings
    def setUpClass(cls):
        """Setting up the test variables."""
        cls.test_dict = ldt.dicts.derivation.meta.DerivationAnalyzer(language="en")

    @classmethod
    def tearDownClass(cls):
        """Clearning up the test variables."""
        cls.test_dict = None

    @ignore_warnings
    def test_dict_initialization(self):
        self.assertEqual(self.test_dict.language, "en")

    @ignore_warnings
    def test_dict_affixes(self):
        res = self.test_dict._get_constituents("kindness")
        self.assertIn("-ness", res["suffixes"])

    @ignore_warnings
    def test_dict_compounds(self):
        res = self.test_dict._get_constituents("toothpaste")
        self.assertIn("tooth", res["roots"])

    @ignore_warnings
    def test_dict_related(self):
        res = self.test_dict._get_related_words("kind")
        self.assertIn("kindness", res)

    # @ignore_warnings
    # def test_dict_all(self):
    #     time.sleep(0.5)
    #     res = test_dict.analyze("kindness")
    #     worked = "-ness" in res["suffixes"] and "kindliness" in res[
    #         "related_words"]
    #     self.assertTrue(worked)

if __name__ == '__main__':
    unittest.main()