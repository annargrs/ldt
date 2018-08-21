import unittest
import os

import ldt

from ldt.helpers.ignore import ignore_warnings as ignore_warnings

test_dict = ldt.dicts.normalize.Normalization(language="English",
                                              lowercasing=False,
                                              order=("wordnet", "custom"))

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the normalizer class.
    """

    def test_init(self):
        self.assertEqual("English", test_dict.language)

    def test_contains_a_letter(self):
        res = ldt.dicts.normalize.contains_a_letter("^*&%*2")
        self.assertFalse(res)

    def test_noise(self):
        res = test_dict._noise("^*&%*2")
        self.assertEqual(res["word_categories"], ["Noise"])

    def test_noise_norm(self):
        res = test_dict.normalize("^*&%*2")
        self.assertEqual(res["word_categories"], ["Noise"])

    def test_contains_non_letter(self):
        res = ldt.dicts.normalize.contains_non_letters("apt50")
        self.assertTrue(res)

    def test_num(self):
        res = test_dict.numberdict.is_a_word("apt50")
        self.assertTrue(res)

    def test_num_norm(self):
        res = test_dict.normalize("apt50")
        self.assertTrue(res)

    def test_web(self):
        res = test_dict.normalize("google.com")
        self.assertEqual(res["word_categories"], ["URLs"])

    def test_files(self):
        res = test_dict.normalize("cat.jpg")
        self.assertEqual(res["word_categories"], ["Filenames"])

    @ignore_warnings
    def test_hashtags(self):
        res = test_dict.normalize("#cat")
        self.assertEqual(res["word_categories"], ["Hashtags"])

    def test_numbers(self):
        res = test_dict.normalize("twenty")
        self.assertEqual(res["word_categories"], ["Numbers"])

    @ignore_warnings
    def test_basic(self):
        res = test_dict.normalize("cat")
        self.assertIn("wordnet", res["found_in"])

    @ignore_warnings
    def test_lemmas(self):
        res = test_dict.normalize("cats")
        self.assertIn("cat", res["lemmas"])

    @ignore_warnings
    def test_names(self):
        res = test_dict.normalize("alice")
        self.assertIn("Names", res["word_categories"])

    # @ignore_warnings
    # def test_foreign(self):
    #     res = test_dict.normalize("niño")
    #     self.assertIn("Foreign", res["word_categories"])
    #
    # @ignore_warnings
    # def test_denoise(self):
    #     res = test_dict.normalize("#$%cats(*")
    #     print(res)  #{'found_in': ['wordnet'], 'lemmas': ['cat']}
    #     self.assertIn("cat", res["lemmas"])




if __name__ == '__main__':
    unittest.main()