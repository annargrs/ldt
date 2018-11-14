import unittest
import os

os.environ["TESTING_LDT"] = "TRUE"

import ldt
from ldt.dicts.semantics.lex_dictionary import LexicographicDictionary

class MockDictionary(LexicographicDictionary):

    def is_a_word(self, word):
        pass

    def get_relations(self, word, relations):
        pass

    def get_relation(self, word, relation):
        pass

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the WordNet functions: the pre-computed
    output is expected to be contained, but the module is not punished for
    new words not in the pre-computed lists - in case the dictionaries get
    updated.
    """

    def test_dictionary_initialization(self):
        test = MockDictionary()
        test.language = "French"
        self.assertEqual(test.language, "French")

    def test_relation_check(self):
        test = MockDictionary()
        res = test.check_relation("hyponyms")
        self.assertEqual(res, "hyponyms")

    def test_relations_check(self):
        test = MockDictionary()
        res = test.check_relations(("synonyms", "antonyms"))
        self.assertEqual(res, ("synonyms", "antonyms"))

    def test_relations_error(self):
        test = MockDictionary()
        with self.assertRaises(ldt.helpers.exceptions.DictError):
            test.check_relations(relations=("synonyms", "troponyms"))

    def test_relation_error(self):
        test = MockDictionary()
        with self.assertRaises(ldt.helpers.exceptions.DictError):
            test.check_relation(relation="troponyms")

    def test_post_processing(self):
        test = MockDictionary()
        test.lowercasing = True
        res = test.post_process(["Good"])
        self.assertIn("good", res)

if __name__ == '__main__':
    ldt.config = ldt._test_config
    unittest.main()