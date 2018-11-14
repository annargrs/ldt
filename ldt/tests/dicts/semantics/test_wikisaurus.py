import unittest
import os
import time
import os

os.environ["TESTING_LDT"] = "TRUE"

import ldt
from ldt.helpers.ignore import ignore_warnings

class Tests(unittest.TestCase):
    '''
    The tests in this block inspect the Wikisaurus functionality:
    updating the vocab list cache and retrieving entry data.
    '''

    @classmethod
    @ignore_warnings
    def setUpClass(cls):
        """Setting up the test variables."""
        cls.test_dict = ldt.dicts.semantics.wikisaurus.Wikisaurus(cache=False)


    @classmethod
    def tearDownClass(cls):
        """Clearning up the test variables."""
        cls.test_dict = None

    @ignore_warnings
    def test_wikisaurus_initialization(self):
        self.assertEqual(self.test_dict.language, "en")

    @ignore_warnings
    def test_wikisaurus_language_setting(self):
        test_dict_fr = ldt.dicts.semantics.wikisaurus.Wikisaurus(cache=False)
        test_dict_fr.language = "French"
        self.assertEqual(test_dict_fr.language, "fr")

    # @ignore_warnings
    # def test_wikisaurus_cache(self):
    #     test_dict.load_cache()
    #     self.assertIn("benzodiazepine", test_dict.cache)

    @ignore_warnings
    def test_word_in_wikisaurus(self):
        # test_dict = ldt.dicts.semantics.wikisaurus.Wikisaurus(cache=False)
        # test_dict.language = "english"
        # test_dict.load_cache()
        time.sleep(0.5)
        self.assertTrue(self.test_dict.is_a_word("benzodiazepine"))

    @ignore_warnings
    def test_retrieve_wikisaurus(self):
        # test_dict = ldt.dicts.semantics.wikisaurus.Wikisaurus(cache=False)
        # test_dict.language = "english"
        time.sleep(0.5)
        res = self.test_dict.query("cat")
        self.assertIn("feline", res[0])

    @ignore_warnings
    def test_parse_wikisaurus(self):
        # test_dict = ldt.dicts.semantics.wikisaurus.Wikisaurus(cache=False)
        # test_dict.language = "english"
        time.sleep(0.5)
        res_data = self.test_dict.query("cat")
        res = self.test_dict._parse_wikisaurus_relations(res_data)
        self.assertIn("synonyms", res)

    @ignore_warnings
    def test_cleanup_wikisaurus(self):
        # test_dict = ldt.dicts.semantics.wikisaurus.Wikisaurus(cache=False)
        # test_dict.language = "english"
        time.sleep(0.5)
        res_data = self.test_dict.query("cat")
        res = self.test_dict._parse_wikisaurus_relations(res_data)
        cleaned_res = self.test_dict._cleanup_wikisaurus(res)
        worked = "\n{{ws" in cleaned_res["synonyms"]
        self.assertFalse(worked)

    @ignore_warnings
    def test_wikisaurus_relations(self):
        # test_dict = ldt.dicts.semantics.wikisaurus.Wikisaurus(cache=False)
        # test_dict.language = "english"
        time.sleep(0.5)
        res = self.test_dict.get_relations("cat", relations=("synonyms",
                                                         "antonyms"))
        worked = "hyponyms" not in res and "tabby" in res["synonyms"]
        self.assertTrue(worked)

if __name__ == '__main__':
    ldt.config = ldt._test_config
    unittest.main()