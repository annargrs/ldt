import unittest
import os

import ldt

from ldt.helpers.ignore import ignore_warnings as ignore_warnings

test_dict = ldt.dicts.normalize.Normalization(language="English",
                                              order=("wordnet", "custom"),
                                              lowercasing=True)

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the _normalizer class.
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
        self.assertIn("Numbers", res["word_categories"])

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

    @ignore_warnings
    def test_foreign(self):
        res = test_dict.normalize("gouvernement")
        self.assertIn("Foreign", res["word_categories"])

    def test_denoise(self):
        res = ldt.dicts.normalize.denoise("#$%cats(*")
        self.assertEqual(res, "cats")

    def test_denoise_norm(self):
        res = test_dict.normalize("#$%cats(*")
        self.assertIn("cat", res["lemmas"])

    def test_misspell(self):
        res = test_dict.spelldict.spelling_nazi("mispelling")
        self.assertEqual(res, "misspelling")

    def test_misspell_norm(self):
        res = test_dict.normalize("gramar")
        self.assertIn("grammar", res["lemmas"])
    # fix spelling
    #
    # # fix hyphenation
    @ignore_warnings
    def test_hyphenation(self):
        res = test_dict.normalize("hy-phen")
        self.assertIn("hyphen", res["lemmas"])

    @ignore_warnings
    def test_dash_join(self):
        res = test_dict._dash("hy-phen")
        self.assertIn("hyphen", res["lemmas"])
    #
    @ignore_warnings
    def test_split(self):
        res = test_dict.normalize("cat.purrs")
        worked = "purr" in res["lemmas"] and "cat" in res["lemmas"]
        self.assertTrue(worked)

    @ignore_warnings
    def test_split_unspaced(self):
        res = test_dict.normalize("knownissue")
        worked = "known" in res["lemmas"] and "issue" in res["lemmas"]
        self.assertTrue(worked)

if __name__ == '__main__':
    unittest.main()