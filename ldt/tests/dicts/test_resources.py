# -*- coding: utf-8 -*-

import unittest
import os

import ldt

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the base spellchecker functionality:
    checking if the word is in a given language, or a pre-defined set of
    foreign languages.

    """

    @classmethod
    def setUpClass(cls):
        """Setting up the test variables."""
        cls.web_dict = ldt.dicts.resources.WebDictionary()
        cls.name_dict = ldt.dicts.resources.NameDictionary(
            language="english", lowercasing=False)
        cls.number_dict = ldt.dicts.resources.NumberDictionary(
            language="english")
        cls.file_dict = ldt.dicts.resources.FileDictionary()


    @classmethod
    def tearDownClass(cls):
        """Clearning up the test variables."""
        cls.web_dict = None
        cls.name_dict = None
        cls.number_dict = None
        cls.file_dict = None

    def test_names(self):
        self.assertEqual("en", self.name_dict.language)

    def test_names(self):
        self.assertTrue(self.name_dict.is_a_word("Alice"))

    def test_names(self):
        test_dict = ldt.dicts.resources.NameDictionary(language="english",
                                                       lowercasing=True)
        self.assertTrue(test_dict.is_a_word("alice"))

    def test_numbers(self):
        self.assertTrue(self.number_dict.is_a_word("one"))

    def test_numbers(self):
        self.assertTrue(self.number_dict.is_a_word("2"))

    #todo: split such cases?
    def test_numbers(self):
        self.assertFalse(self.number_dict.is_a_word("test2"))

    def test_associations(self):
        test_dict = ldt.dicts.resources.AssociationDictionary(
            language="english", lowercasing=False)
        self.assertTrue(self.test_dict.is_a_word("falcon"))

    def test_associations(self):
        test_dict = ldt.dicts.resources.AssociationDictionary(
            language="english", lowercasing=True)
        # print(list(test_dict.data.keys()))
        self.assertIn("eagle", test_dict.data["falcon"])

    def test_domain(self):
        self.assertTrue(self.web_dict.is_a_word("example.com"))

    def test_wwww(self):
        self.assertTrue(self.web_dict.is_a_word("www.bizarre.bzzzz"))

    def test_domain_long(self):
        self.assertTrue(self.web_dict.is_a_word("example.com/sub/something"))

    def test_file(self):
        self.assertTrue(self.file_dict.is_a_word("cat.jpg"))

    def test_file(self):
        self.assertTrue(self.file_dict.is_a_word("path/to/cat/cat.jpg"))

if __name__ == '__main__':
    unittest.main()