# -*- coding: utf-8 -*-

import unittest
import time
import ldt

from ldt.helpers.ignore import ignore_warnings

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the retrieval of Wiktionary etymologies
    (rule-based).

    """
    @ignore_warnings
    def test_dict_initialization(self):
        test_dict = ldt.dicts.derivation.wiktionary.DerivationWiktionary(
            cache=False, language="english")
        self.assertEqual(test_dict.language, "en")

    @ignore_warnings
    def test_etymologies(self):
        test_dict = ldt.dicts.derivation.wiktionary.DerivationWiktionary(
            cache=False, language="english")
        time.sleep(0.5)
        res = test_dict.get_etymologies("planetarium")
        self.assertIn("planet", res[0])

    @ignore_warnings
    def test_etymologies_check(self):
        test_base_dict = ldt.dicts.base.wordnet.en.BaseWordNet()
        test_dict = ldt.dicts.derivation.wiktionary.DerivationWiktionary(
            cache=False, language="english")
        time.sleep(0.5)
        res = test_dict.get_etymologies("brotherhood",
                                        exclude_old_sources=test_base_dict)
        worked = "brotherrede" not in res[0] and "brother" in res[0]
        self.assertTrue(worked)

    @ignore_warnings
    def test_related_words(self):
        test_dict = ldt.dicts.derivation.wiktionary.DerivationWiktionary(
            cache=False, language="english")
        time.sleep(0.5)
        res = test_dict.get_related_words("kind")
        self.assertIn("kindliness", res)
        # res = test_dict.get_related_words("wizard")
        # self.assertIn("wizardess", res)

if __name__ == '__main__':
    unittest.main()
