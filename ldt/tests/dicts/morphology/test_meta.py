# -*- coding: utf-8 -*-

import unittest
import os
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
        cls.test_dict_fr = ldt.dicts.morphology.meta.MorphMetaDict(
            language="French", cache=False)
        cls.test_dict_en = ldt.dicts.morphology.meta.MorphMetaDict(
            language="English", cache=False, custom_base="wiktionary")


    @classmethod
    def tearDownClass(cls):
        """Clearning up the test variables."""
        cls.test_dict_fr = None
        cls.test_base_en = None

    @ignore_warnings
    def test_metadictionary_initialization(self):
        self.assertEqual(self.test_dict_fr.wiktionary.language, "fr")

    @ignore_warnings
    def test_metadictionary_initialization_wn(self):
        with self.assertRaises(AttributeError):
            self.test_dict_fr.wn.language

    @ignore_warnings
    def test_metadictionary_wn(self):
        self.assertEqual(self.test_dict_en.wordnet._language, "en")

    @ignore_warnings
    def test_metadictionary_order(self):
        self.assertEqual(self.test_dict_en._order[0], "wordnet")

    @ignore_warnings
    def test_metadictionary_minimal(self):
        self.assertEqual(self.test_dict_en.is_a_word("cat", minimal=True),
                         ["wordnet"])

    @ignore_warnings
    def test_metadictionary_minimal(self):
        self.assertEqual(self.test_dict_en.is_a_word("cat", minimal=True),
                         ["wordnet"])

    @ignore_warnings
    def test_metadictionary_get_pos(self):
        test_dict = ldt.dicts.morphology.meta.MorphMetaDict(order=[
            "wordnet"], custom_base="wordnet")
        res = test_dict.get_pos("nouned")
        self.assertEqual(res, ["verb"])

    @ignore_warnings
    def test_metadictionary_lemmatize(self):
        test_dict = ldt.dicts.morphology.meta.MorphMetaDict(order=[
            "wordnet"], custom_base="wordnet")
        res = test_dict.lemmatize("nouned")
        self.assertEqual(res, ["noun"])

    @ignore_warnings
    def test_metadictionary_lemmatize(self):
        test_dict = ldt.dicts.morphology.meta.MorphMetaDict(order=["wordnet",
                                                                   "wiktionary"], custom_base="wiktionary")
        res = test_dict.lemmatize("GPUs")
        self.assertEqual(res, ["GPU"])

    #
    # @ignore_warnings
    # def test_metadictionary_lemmatize(self):
    #     self.assertEqual(test_dict_en.is_a_word("cat", minimal=True), ["wordnet"])

    # @ignore_warnings
    # def test_metadictionary_max(self):
    #     res = test_dict_en.is_a_word("cat", minimal=False)
    #     self.assertTrue(len(res) > 1)
    #
    # @ignore_warnings
    # def test_metadictionary_is_a_word(self):
    #     time.sleep(0.5)
    #     self.assertTrue(test_dict_fr.is_a_word("chatte"))
    #
    # @ignore_warnings
    # def test_metadictionary_relations(self):
    #     time.sleep(0.5)
    #     res = test_dict_en.get_relations("white", relations="main")
    #     worked = "unclean" in res["antonyms"] and "nonwhite" in res["antonyms"]
    #     self.assertTrue(worked)
    #
    # @ignore_warnings
    # def test_metadictionary_relation(self):
    #     time.sleep(0.5)
    #     res = test_dict_en.get_relation("white", relation="antonyms")
    #     worked = "unclean" in res and "nonwhite" in res
    #     self.assertTrue(worked)

if __name__ == '__main__':
    ldt.config = ldt._test_config
    unittest.main()