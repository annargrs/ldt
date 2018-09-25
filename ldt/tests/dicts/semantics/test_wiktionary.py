import unittest

import ldt
import os
import time

from ldt.helpers.ignore import ignore_warnings

class Tests(unittest.TestCase):
    '''
    The tests in this block inspect the Wiktionary functionality:
    updating the vocab list cache and retrieving entry data.
    '''

    @ignore_warnings
    def test_wiktionary_initialization(self):
        test_dict = ldt.dicts.semantics.Wiktionary(cache=False,
                                                   language="English")
        self.assertEqual(test_dict.language, "en")

    @ignore_warnings
    def test_wiktionary_language_setting(self):
        test_dict = ldt.dicts.semantics.Wiktionary(cache=False)
        test_dict.language = "French"
        self.assertEqual(test_dict.language, "fr")

    @ignore_warnings
    def test_wiktionary_cache(self):
        test_dict = ldt.dicts.semantics.Wiktionary(cache=False)
        test_dict.language = "zulu"
        test_dict.load_cache()
        self.assertIn("indlu", test_dict.cache)

    @ignore_warnings
    def test_word_in_wiktionary(self):
        test_dict = ldt.dicts.semantics.Wiktionary(cache=False)
        test_dict.language = "zulu"
        time.sleep(0.5)
        self.assertTrue(test_dict.is_a_word("indlu"))

    @ignore_warnings
    def test_wikidata(self):
        test_dict = ldt.dicts.semantics.Wiktionary(cache=False)
        test_dict.language = "zulu"
        # test_dict.load_cache()
        time.sleep(0.5)
        res = test_dict.query("indlu")
        self.assertIn("definitions", res[0].keys())

    @ignore_warnings
    def test_get_wiktionary_relations(self):
        test_dict = ldt.dicts.semantics.Wiktionary(cache=False)
        test_dict.language = "english"
        time.sleep(0.5)
        res = test_dict.get_relations("white", relations="all")
        self.assertIn("black", res["antonyms"])

    @ignore_warnings
    def test_get_wiktionary_relation(self):
        test_dict = ldt.dicts.semantics.Wiktionary(cache=False)
        test_dict.language = "english"
        time.sleep(0.5)
        res = test_dict.get_relation("white", relation="antonyms")
        self.assertIn("black", res)

if __name__ == '__main__':
    unittest.main()