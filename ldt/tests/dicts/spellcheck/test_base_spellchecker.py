# -*- coding: utf-8 -*-

import unittest

import ldt

test_dict = ldt.dicts.spellcheck.Spellchecker(engine_order="aspell,myspell")

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the base spellchecker functionality:
    checking if the word is in a given language, or a pre-defined set of
    foreign languages.

    """

    def test_dict_initialization(self):
        self.assertIn("fr", test_dict.foreign_languages)

    def test_dict_error(self):
        with self.assertRaises(ldt.helpers.exceptions.LanguageError):
            test_dict2 = ldt.dicts.spellcheck.Spellchecker(language="cat")

    def test_dict_is_a_word(self):
        self.assertTrue(test_dict.is_a_word("cat"))

    def test_dict_is_foreign(self):
        self.assertTrue(test_dict.is_a_word("chateau"))

    def test_dict_with_charset(self):
        self.assertFalse(test_dict._filter_by_charset("ça", include=["latin",
                                                               "with"]))

    def test_dict_latin(self):
        self.assertFalse(test_dict._filter_by_charset("кот", include=["latin"]))

    def test_dict_suggest(self):
        self.assertIn("with", test_dict.suggest("iwth"))

    #only aspell is installed in travis, so the order does not actually change
    def test_dict_providers(self):
        test_dict2 = ldt.dicts.spellcheck.Spellchecker(engine_order="aspell,myspell")
        self.assertEqual(test_dict.provider, test_dict2.provider)

    def test_opcodes(self):
        test = test_dict.get_opcode_alignment("generaly", "generally")
        self.assertEqual(test["misspelling"], 'general_y')

if __name__ == '__main__':
    unittest.main()