# -*- coding: utf-8 -*-

import unittest
import os

import ldt

web_dict = ldt.dicts.resources.WebDictionary()
name_dict = ldt.dicts.resources.NameDictionary(language="english",
                                               lowercasing=False)
number_dict = ldt.dicts.resources.NumberDictionary(language="english")
file_dict = ldt.dicts.resources.FileDictionary()

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the base spellchecker functionality:
    checking if the word is in a given language, or a pre-defined set of
    foreign languages.

    """

    def test_names(self):
        self.assertEqual("en", name_dict.language)

    def test_names(self):
        self.assertTrue(test_dict.is_a_word("Alice"))

    def test_names(self):
        test_dict = ldt.dicts.resources.NameDictionary(language="english",
                                                       lowercasing=True)
        self.assertTrue(test_dict.is_a_word("alice"))

    def test_numbers(self):
        self.assertTrue(number_dict.is_a_word("one"))

    def test_numbers(self):
        self.assertTrue(number_dict.is_a_word("2"))

    def test_numbers(self):
        self.assertTrue(number_dict.is_a_word("test2"))

    def test_associations(self):
        test_dict = ldt.dicts.resources.AssociationDictionary(
            language="english", lowercasing=False)
        self.assertTrue(test_dict.is_a_word("falcon"))

    def test_associations(self):
        test_dict = ldt.dicts.resources.AssociationDictionary(
            language="english", lowercasing=True)
        # print(list(test_dict.data.keys()))
        self.assertIn("eagle", test_dict.data["falcon"])

    def test_domain(self):
        self.assertTrue(web_dict.is_a_word("example.com"))

    def test_wwww(self):
        self.assertTrue(web_dict.is_a_word("www.bizarre.bzzzz"))

    def test_domain_long(self):
        self.assertTrue(web_dict.is_a_word("example.com/sub/something"))

    def test_file(self):
        self.assertTrue(file_dict.is_a_word("cat.jpg"))

    def test_file(self):
        self.assertTrue(file_dict.is_a_word("path/to/cat/cat.jpg"))

if __name__ == '__main__':
    unittest.main()