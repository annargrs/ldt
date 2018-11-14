import unittest
import os

os.environ["TESTING_LDT"] = "TRUE"

import ldt

from ldt.helpers.ignore import ignore_warnings

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the _normalizer class.
    """

    @classmethod
    @ignore_warnings
    def setUpClass(cls):
        """Setting up the test variables."""
        cls.test_dict = ldt.dicts.normalize.Normalization(language="English",
                                                          order=("wordnet",
                                                                 "custom"),
                                                          lowercasing=True)

    @classmethod
    def tearDownClass(cls):
        """Clearning up the test variables."""
        cls.test_dict = None

    def test_init(self):
        self.assertEqual("English", self.test_dict.language)

    def test_contains_a_letter(self):
        res = ldt.dicts.normalize.contains_a_letter("^*&%*2")
        self.assertFalse(res)

    def test_noise(self):
        res = self.test_dict._noise("^*&%*2")
        self.assertEqual(res["word_categories"], ["Noise"])

    def test_noise_norm(self):
        res = self.test_dict.normalize("^*&%*2")
        self.assertEqual(res["word_categories"], ["Noise"])

    def test_contains_non_letter(self):
        res = ldt.dicts.normalize.contains_non_letters("apt50")
        self.assertTrue(res)

    def test_num(self):
        res = self.test_dict.numberdict.is_a_word("apt50")
        self.assertTrue(res)

    def test_num_norm(self):
        res = self.test_dict.normalize("apt50")
        self.assertTrue(res)

    def test_web(self):
        res = self.test_dict.normalize("google.com")
        self.assertEqual(res["word_categories"], ["URLs"])

    def test_files(self):
        res = self.test_dict.normalize("cat.jpg")
        self.assertEqual(res["word_categories"], ["Filenames"])

    @ignore_warnings
    def test_hashtags(self):
        res = self.test_dict.normalize("#cat")
        self.assertEqual(res["word_categories"], ["Hashtags"])

    def test_numbers(self):
        res = self.test_dict.normalize("twenty")
        self.assertIn("Numbers", res["word_categories"])

    @ignore_warnings
    def test_basic(self):
        res = self.test_dict.normalize("cat")
        self.assertIn("wordnet", res["found_in"])

    @ignore_warnings
    def test_lemmas(self):
        res = self.test_dict.normalize("cats")
        self.assertIn("cat", res["lemmas"])

    @ignore_warnings
    def test_names(self):
        res = self.test_dict.normalize("alice")
        self.assertIn("ProperNouns", res["word_categories"])

    @ignore_warnings
    def test_foreign(self):
        res = self.test_dict.normalize("gouvernement")
        self.assertIn("ForeignWords", res["word_categories"])

    def test_denoise(self):
        res = ldt.dicts.normalize.denoise("#$%cats(*")
        self.assertEqual(res, "cats")

    def test_denoise_norm(self):
        res = self.test_dict.normalize("#$%cats(*")
        self.assertIn("cat", res["lemmas"])

    def test_misspell(self):
        res = self.test_dict.spelldict.spelling_nazi("mispelling")
        self.assertEqual(res, "misspelling")

    def test_misspell_norm(self):
        res = self.test_dict.normalize("gramar")
        self.assertIn("grammar", res["lemmas"])
    # fix spelling
    #
    # # fix hyphenation
    @ignore_warnings
    def test_hyphenation(self):
        res = self.test_dict.normalize("hy-phen")
        self.assertIn("hyphen", res["lemmas"])

    @ignore_warnings
    def test_dash_join(self):
        res = self.test_dict._dash("hy-phen")
        self.assertIn("hyphen", res["lemmas"])
    #
    @ignore_warnings
    def test_split(self):
        res = self.test_dict.normalize("cat.purrs")
        worked = "purr" in res["lemmas"] and "cat" in res["lemmas"]
        self.assertTrue(worked)

    @ignore_warnings
    def test_split_unspaced(self):
        res =self.test_dict.normalize("knownissue")
        worked = "known" in res["lemmas"] and "issue" in res["lemmas"]
        self.assertTrue(worked)

if __name__ == '__main__':
    unittest.main()