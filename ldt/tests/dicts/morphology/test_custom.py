# -*- coding: utf-8 -*-
import unittest
import time

import ldt

from ldt.helpers.ignore import ignore_warnings as ignore_warnings

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the custom LDT functionality for
    lemmatization of non-dictionary words.

    """

    @ignore_warnings
    def test_dict_initialization(self):
        test_dict = ldt.dicts.morphology.custom.en.MorphCustomDict()
        self.assertEqual(test_dict.language, "en")

    @ignore_warnings
    def test_comparative(self):
        test_dict = ldt.dicts.morphology.custom.en.MorphCustomDict()
        test_base_dict = ldt.dicts.base.wordnet.en.BaseWordNet()
        res = test_dict.lemmatize("posher", test_base_dict)
        self.assertEqual(res, ["posh"])

    @ignore_warnings
    def test_superlative(self):
        test_dict = ldt.dicts.morphology.custom.en.MorphCustomDict()
        test_base_dict = ldt.dicts.base.wordnet.en.BaseWordNet()
        res = test_dict.lemmatize("poshest", test_base_dict)
        self.assertEqual(res, ["posh"])

    @ignore_warnings
    def test_plural(self):
        test_dict = ldt.dicts.morphology.custom.en.MorphCustomDict()
        test_base_dict = ldt.dicts.base.wordnet.en.BaseWordNet()
        res = test_dict.lemmatize("kindnesses", test_base_dict)
        self.assertEqual(res, ["kindness"])

    @ignore_warnings
    def test_3rdPdSg(self):
        test_dict = ldt.dicts.morphology.custom.en.MorphCustomDict()
        test_base_dict = ldt.dicts.base.wordnet.en.BaseWordNet()
        res = test_dict.lemmatize("sickens", test_base_dict)
        self.assertEqual(res, ["sicken"])

    @ignore_warnings
    def test_gerund(self):
        test_dict = ldt.dicts.morphology.custom.en.MorphCustomDict()
        test_base_dict = ldt.dicts.base.wordnet.en.BaseWordNet()
        res1 = test_dict.lemmatize("whopping", test_base_dict)
        res2 = test_dict.lemmatize("floundering", test_base_dict)
        worked = res1 == ["whop"] and res2 == ["flounder"]
        self.assertTrue(worked)

    @ignore_warnings
    def test_past(self):
        test_dict = ldt.dicts.morphology.custom.en.MorphCustomDict()
        test_base_dict = ldt.dicts.base.wiktionary.BaseWiktionary(language="en",
                                                      cache=False)
        res1 = test_dict.lemmatize("whopped", test_base_dict)
        time.sleep(0.5)
        res2 = test_dict.lemmatize("floundered", test_base_dict)
        time.sleep(0.5)
        res3 = test_dict.lemmatize("microwaved", test_base_dict)
        time.sleep(0.5)
        res4 = test_dict.lemmatize("stir-fried", test_base_dict)
        worked = res1 == ["whop"] and res2 == ["flounder"] and res3 == [
            "microwave"] and res4 == ["stir-fry"]
        self.assertTrue(worked)

if __name__ == '__main__':
    unittest.main()
