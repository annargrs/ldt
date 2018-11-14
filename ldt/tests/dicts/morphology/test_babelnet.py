import unittest
import os

os.environ["TESTING_LDT"] = "TRUE"

import ldt


class Tests(unittest.TestCase):
    """
    The tests in this block inspect the Wiktionary morphological functions:
    lemmatization and retrieval of possible POS tags for a query word.

    """

    def test_dict_initialization(self):
        with self.assertRaises(ldt.helpers.exceptions.AuthorizationError):
            test_dict = ldt.dicts.morphology.babelnet.MorphBabelNet(
                language="english", babelnet_key=None)

    # def test_dict_initialization(self):
    #     test_dict = ldt.dicts.morphology.babelnet.MorphBabelNet(
    #         language="english")
    #     self.assertEqual(test_dict.language, "EN")
    #
    # def test_pos_dict(self):
    #     test_dict = ldt.dicts.morphology.babelnet.MorphBabelNet(
    #         language="english")
    #     res = test_dict.get_pos("cat")
    #     self.assertGreaterEqual(res["noun"], 40)
    #
    # def test_pos_list(self):
    #     test_dict = ldt.dicts.morphology.babelnet.MorphBabelNet(
    #         language="english")
    #     res = test_dict.get_pos("cat", formatting="list")
    #     worked = len(res) >= 2 and "noun" in res
    #     self.assertTrue(worked)

if __name__ == '__main__':
    unittest.main()
