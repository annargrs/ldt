# -*- coding: utf-8 -*-

import unittest
import os

import ldt
from ldt.helpers.ignore import ignore_warnings as ignore_warnings

test_dict_fr = ldt.dicts.metadictionary.MetaDictionary(language="French",
    cache=False)

test_dict_en = ldt.dicts.metadictionary.MetaDictionary(language="English",
    cache=False)

class Tests(unittest.TestCase):
    '''
    The tests in this block inspect the MetaDictionary functionality:
    combining WordNet and Wiktionary data.
    '''

    @ignore_warnings
    def test_metadictionary_initialization(self):
        self.assertEqual(test_dict_fr.wikisaurus.language, "fr")

    @ignore_warnings
    def test_metadictionary_initialization_wn(self):
        with self.assertRaises(AttributeError):
            test_dict_fr.wn.language

    @ignore_warnings
    def test_metadictionary_wn(self):
        self.assertEqual(test_dict_en.wn._language, "en")

    @ignore_warnings
    def test_metadictionary_is_a_word(self):
        self.assertTrue(test_dict_fr.is_a_word("chatte"))

    @ignore_warnings
    def test_metadictionary_relations(self):
        res = test_dict_en.get_relations("white", relations="main")
        worked = "unclean" in res["antonyms"] and "nonwhite" in res["antonyms"]
        self.assertTrue(worked)

    @ignore_warnings
    def test_metadictionary_relation(self):
        res = test_dict_en.get_relation("white", relation="antonyms")
        worked = "unclean" in res and "nonwhite" in res
        self.assertTrue(worked)

if __name__ == '__main__':
    unittest.main()