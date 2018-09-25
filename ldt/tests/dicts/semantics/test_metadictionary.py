# -*- coding: utf-8 -*-

import unittest
import time

import ldt
from ldt.helpers.ignore import ignore_warnings

class Tests(unittest.TestCase):
    '''
    The tests in this block inspect the MetaDictionary functionality:
    combining WordNet and Wiktionary data.
    '''

    @classmethod
    @ignore_warnings
    def setUpClass(cls):
        """Setting up the test variables."""
        cls.test_dict_fr = ldt.dicts.semantics.metadictionary.MetaDictionary(
            language="French", cache=False)
        cls.test_dict_en = ldt.dicts.semantics.metadictionary.MetaDictionary(
            language="English", cache=False)

    @classmethod
    def tearDownClass(cls):
        """Clearning up the test variables."""
        cls.test_dict_fr = None
        cls.test_dict_en = None

    @ignore_warnings
    def test_metadictionary_initialization(self):
        self.assertEqual(self.test_dict_fr.wikisaurus.language, "fr")

    @ignore_warnings
    def test_metadictionary_initialization_wn(self):
        with self.assertRaises(AttributeError):
            self.test_dict_fr.wn.language

    @ignore_warnings
    def test_metadictionary_wn(self):
        self.assertEqual(self.test_dict_en.wordnet._language, "en")

    @ignore_warnings
    def test_metadictionary_order(self):
        self.assertEqual(self.test_dict_en._order, ["wordnet", "wiktionary",
                                                    "wikisaurus"])

    @ignore_warnings
    def test_metadictionary_minimal(self):
        self.assertEqual(self.test_dict_en.is_a_word("cat", minimal=True),
                         ["wordnet"])

    @ignore_warnings
    def test_metadictionary_max(self):
        res = self.test_dict_en.is_a_word("cat", minimal=False)
        self.assertTrue(len(res) > 1)

    @ignore_warnings
    def test_metadictionary_is_a_word(self):
        time.sleep(0.5)
        self.assertTrue(self.test_dict_fr.is_a_word("chatte"))

    @ignore_warnings
    def test_metadictionary_relations(self):
        time.sleep(0.5)
        res = self.test_dict_en.get_relations("white", relations="main")
        worked = "unclean" in res["antonyms"] and "nonwhite" in res["antonyms"]
        self.assertTrue(worked)

    @ignore_warnings
    def test_metadictionary_relation(self):
        time.sleep(0.5)
        res = self.test_dict_en.get_relation("white", relation="antonyms")
        worked = "unclean" in res and "nonwhite" in res
        self.assertTrue(worked)

if __name__ == '__main__':
    unittest.main()