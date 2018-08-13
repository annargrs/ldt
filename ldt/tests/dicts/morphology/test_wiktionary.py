import unittest

import ldt
import time
from ldt.helpers.ignore import ignore_warnings as ignore_warnings

test_dict = ldt.dicts.morphology.wiktionary.MorphWiktionary(cache=False,
                                                            language="english")

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the Wiktionary morphological functions:
    lemmatization and retrieval of possible POS tags for a query word.

    """
    @ignore_warnings
    def test_dict_initialization(self):
        self.assertEqual(test_dict.language, "en")

    @ignore_warnings
    def test_pos_dict(self):
        time.sleep(0.5)
        res = test_dict.get_pos("cat")
        self.assertGreaterEqual(res["noun"], 8)

    @ignore_warnings
    def test_pos_list(self):
        time.sleep(0.5)
        res = test_dict.get_pos("cat", formatting="list")
        worked = len(res) >= 2 and "noun" in res
        self.assertTrue(worked)

    # def test_lemmatize(self):
    #     test_dict = ldt.dicts.morphology.wiktionary.MorphWiktionary()
    #     res = test_dict.lemmatize("cats")
    #     worked = len(res) == 1 and "cat" in res
    #     self.assertTrue(worked)

if __name__ == '__main__':
    unittest.main()
