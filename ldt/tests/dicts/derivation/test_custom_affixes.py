# -*- coding: utf-8 -*-

import unittest

import ldt

from ldt.helpers.ignore import ignore_warnings as ignore_warnings

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the custom LDT functionality for
    analysis of the morphological structure of non-dictionary word: suffixes
    and prefixes (with English data).

    """

    @ignore_warnings
    def test_dict_initialization(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        worked = test_dict.language == "en" and \
                 test_dict.dictionary.is_a_word("cat") == True
        self.assertTrue(worked)

    @ignore_warnings
    def test_dict_vowels(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        self.assertTrue(test_dict.is_a_vowel("a"))

    @ignore_warnings
    def test_dict_exceptions(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        res = test_dict.check_exceptions("blood")
        self.assertIn("bleed", res["roots"])

    @ignore_warnings
    def test_dict_exceptions_equidistant(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        res = test_dict.check_exceptions("bleed")
        self.assertIn("blood", res["roots"])

    @ignore_warnings
    def test_dict_sion(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        res = test_dict._suffix_sion("corrosion")
        self.assertIn("corrode", res["roots"])

    @ignore_warnings
    def test_dict_lang_specific(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        res = test_dict._decompose_language_specific_suffixes("corrosion")
        self.assertIn("corrode", res["roots"])

    @ignore_warnings
    def test_dict_prefixes(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        res = test_dict.decompose_prefixes("antithesis")
        self.assertIn("thesis", res["roots"])

    @ignore_warnings
    def test_suffix_family_decomposition(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        res = test_dict._decompose_by_suffix_family("credibility")
        self.assertIn("credible", res["roots"])

    @ignore_warnings
    def test_suffix_basic(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        res = test_dict._decompose_suffix_simple("kingdom")
        self.assertIn("king", res["roots"])

    @ignore_warnings
    def test_suffix_doubling(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        res = test_dict._decompose_suffix_doubling("stopper")
        self.assertIn("stop", res["roots"])

    @ignore_warnings
    def test_suffix_replacements(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        res1 = test_dict._decompose_suffix_replacements("happily")
        res2 = test_dict._decompose_suffix_replacements("panicking")
        worked = "panic" in res2["roots"] and "happy" in res1["roots"]
        self.assertTrue(worked)

    @ignore_warnings
    def test_suffix_insertions(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        res = test_dict._decompose_suffix_insertions("imaginable")
        self.assertIn("imagine", res["roots"])

    @ignore_warnings
    def test_suffix_blend(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        res = test_dict._decompose_suffix_blend("historic")
        self.assertIn("history", res["roots"])

    @ignore_warnings
    def test_suffix_all(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        res = test_dict.decompose_suffixes("historic")
        # print(res)
        self.assertIn("history", res["roots"])

    @ignore_warnings
    def test_all_affixes(self):
        noise = ldt.dicts.base.wordnet.en.BaseWordNet()
        morph = ldt.dicts.morphology.wordnet.en.MorphWordNet()
        test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation(
            language="en", dictionary=noise, morph_dictionary=morph)
        res = test_dict.analyze_affixes("anti-intellectual")
        self.assertIn("intellect", res["roots"])

if __name__ == '__main__':
    unittest.main()
