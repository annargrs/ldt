# -*- coding: utf-8 -*-

import unittest

import ldt

test_dict = ldt.dicts.spellcheck.en.SpellcheckerEn(engine_order="aspell,"
                                                                "myspell")


class Tests(unittest.TestCase):
    """
    The tests in this block inspect the base spellchecker functionality:
    checking if the word is in a given language, or a pre-defined set of
    foreign languages.

    """

    def test_dict_initialization(self):
        self.assertIn("fr", test_dict.foreign_languages)

    def test_dict_with_charset(self):
        self.assertTrue(test_dict.filter_by_charset("the-cat-and-the-fiddle"))

    def test_dict_foreign(self):
        self.assertTrue(test_dict.is_foreign("猫"))

    def test_dict_foreign(self):
        self.assertTrue(test_dict.is_foreign("niño"))

    def test_dict_foreign(self):
        self.assertTrue(test_dict.is_foreign("chocolat"))

    def test_double_letters(self):
        res = test_dict.common_misspellings("gramar", "grammar")
        self.assertEqual(res, ['double_letter_missed'])

    def test_double_letters(self):
        res = test_dict.common_misspellings("travell", "travel")
        self.assertEqual(res, ['letter_misdoubled'])

    def test_misplaced_letters(self):
        res = test_dict.common_misspellings("abritrary", "arbitrary")
        self.assertEqual(res, ['letter_misplaced'])

    def test_replacements(self):
        res = test_dict.common_misspellings("magik", "magic")
        self.assertEqual(res, ['common_pattern'])

    def test_extra_letters(self):
        res = test_dict.common_misspellings("befor", "before")
        self.assertIn('missing_common_letter', res)

    # def test_extra_letters(self):
    #     res = test_dict.common_misspellings("beeen", "been")
    #     self.assertIn('extra_common_letter', res)

    def test_min_length(self):
        res = test_dict.spelling_nazi("pot", min_length=4)
        self.assertFalse(res)

    def test_existing(self):
        res = test_dict.spelling_nazi("abandon", strict=True)
        self.assertFalse(res)

    def test_patterns(self):
        res = test_dict.spelling_nazi("abillity", confidence=True,
                                        strict=True)
        self.assertEqual(res, "ability")

    def test_strict(self):
        res = test_dict.spelling_nazi("abondon", strict=True)
        self.assertFalse(res)

    def test_non_strict(self):
        res = test_dict.spelling_nazi("abondon", strict=False,
                                       confidence=False)
        if "abandon" in res:
            worked = True
        else:
            worked = False
        self.assertTrue(worked)

if __name__ == '__main__':
    unittest.main()