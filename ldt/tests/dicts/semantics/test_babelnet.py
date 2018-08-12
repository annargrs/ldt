import unittest

import ldt


class Tests(unittest.TestCase):
    '''
    The tests in this block inspect the BabelNet functionality: the pre-computed
    output is expected to be contained, but the module is not punished for
    new words not in the pre-computed lists - in case the dictionaries get
    updated.
    '''

    # def test_babelnet_initialization(self):
    #     test = ldt.dicts.semantics.BabelNet()
    #     test.language = "Italian"
    #     self.assertEqual(test.language, "IT")
    #
    # def test_babelnet_ids(self):
    #     test = ldt.dicts.semantics.BabelNet()
    #     test.language = "English"
    #     res = test.get_ids("cat")
    #     self.assertIn('bn:00516031n', res)
    #
    # def test_babelnet_is_word(self):
    #     test = ldt.dicts.semantics.BabelNet()
    #     test.language = "English"
    #     self.assertFalse(test.is_a_word("catttttt"))
    #
    # def test_babelnet_lemmas(self):
    #     test = ldt.dicts.semantics.BabelNet()
    #     test.language = "English"
    #     test.lowercasing = True
    #     res = test.get_lemmas('bn:00516031n')
    #     self.assertIn('alternative_versions_of_kitty_pryde', res)
    #
    # def test_babelnet_edges(self):
    #     test = ldt.dicts.semantics.BabelNet()
    #     test.language = "English"
    #     res = test.get_edges('bn:00516031n')
    #     self.assertIn('bn:00004927n', res["other"])

    # def test_babelnet_relation(self):
    #     test = ldt.dicts.semantics.BabelNet()
    #     test.language = "English"
    #     res = test.get_relation("senator", relation="hypernyms")
    #     self.assertIn('legislator', res)
    #
    # def test_babelnet_relations(self):
    #     test = ldt.dicts.semantics.BabelNet()
    #     test.language = "English"
    #     res = test.get_relations("senator", relations=("hypernyms"))
    #     self.assertIn('legislator', res["hypernyms"])