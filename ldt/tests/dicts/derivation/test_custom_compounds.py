# -*- coding: utf-8 -*-
import unittest

import ldt

from ldt.helpers.ignore import ignore_warnings


class Tests(unittest.TestCase):
    """
    The tests in this block inspect the custom LDT functionality for
    analysis of the morphological structure of non-dictionary word:
    splitting of compounds (with English data).

    """

    # noise = ldt.dicts.base.wiktionary.BaseWiktionary(language="en",
    #                                                  cache=False)
    noise = ldt.dicts.base.wordnet.en.BaseWordNet(language="en")
    morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
    test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)

    @ignore_warnings
    def test_split_on_dash(self, test_dict=test_dict):
        """Test splitting dashed words"""
        res = test_dict.split_on_dash("merry-go-round")
        self.assertIn("merry", res["roots"])

    @ignore_warnings
    def test_in_vocab(self, test_dict=test_dict):
        """Insertion and replacement patterns: such patterns don't
        exist in English, so testing with fake ones."""
        #test lemmatization
        res1 = test_dict._in_vocab("cats")
        #test replacements
        test_dict.replacements_in_compounds = [["t", "z"]]
        res2 = test_dict._in_vocab("caz")
        test_dict.insertions_in_compounds = ["w"]
        res3 = test_dict._in_vocab("catw")
        worked = res1 == res2 == res3 == "cat"
        self.assertTrue(worked)

    @ignore_warnings
    def test_split_compounds_all(self, test_dict=test_dict):
        """Test splitting compounds"""
        res = test_dict.split_compound("tomcat", filtering=None)
        self.assertIn(['tom', 'c', 'a', 't'], res)

    @ignore_warnings
    def test_split_compounds_filter_min_length(self, test_dict=test_dict):
        """Test splitting compounds with min length limitations"""
        res = test_dict.split_compound("tomcat", filtering="min_split_3")
        self.assertEqual([['tom', 'cat']], res)

    @ignore_warnings
    def test_leave_known_word_alone(self, test_dict=test_dict):
        res = test_dict.decompose_compound("catwalk", split_known_words=False)
        self.assertEqual(res["roots"], [])

    @ignore_warnings
    def test_decompose_compounds(self, test_dict=test_dict):
        res1 = test_dict.decompose_compound("cat-walk", split_known_words=True)
        res2 = test_dict.decompose_compound("catwalk", split_known_words=True)
        worked = res1["roots"] == res2["roots"] == ['cat', 'walk']
        self.assertTrue(worked)


#anti-librarian
if __name__ == '__main__':
    ldt.config = ldt._test_config
    unittest.main()