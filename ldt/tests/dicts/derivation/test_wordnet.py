# -*- coding: utf-8 -*-

import unittest

import ldt

from ldt.helpers.ignore import ignore_warnings

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the retrieval of WordNet derivationally
    related words.

    """

    @ignore_warnings
    def test_dict_initialization(self):
        test_dict = ldt.dicts.derivation.wordnet.en.DerivationWordNet(
            language="english")
        self.assertEqual(test_dict.language, "en")

    @ignore_warnings
    def test_get_related_words(self):
        test_dict = ldt.dicts.derivation.wordnet.en.DerivationWordNet(
            language="english")
        res = test_dict.get_related_words("happy")
        self.assertIn("happiness", res)

if __name__ == '__main__':
    unittest.main()
