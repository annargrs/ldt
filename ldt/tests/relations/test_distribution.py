# -*- coding: utf-8 -*-
"""Testing retrieval of distributional information."""
import unittest

import ldt

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the retrieval of distributional
    information per word pair.

    """

    @classmethod
    def setUpClass(cls):
        """Setting up the test variables."""
        # cls.test_dict = \
        #     ldt.relations.distribution.DistributionDict(language="english",
        #                                                 gdeps=True,
        #                                                 cooccurrence=True,
        #                                                 cooccurrence_freq=False)
        # cls.test_dict_cooc = \
        #     ldt.relations.distribution.DistributionDict(language="english",
        #                                                 cooccurrence=True,
        #                                                 cooccurrence_freq=True)

        cls.test_dict_filtered = \
            ldt.relations.distribution.DistributionDict(language="english",
                                                        cooccurrence=True,
                                                        gdeps=True,
                                                        wordlist=["cat",
                                                                  "walk"])

    @classmethod
    def tearDownClass(cls):
        """Clearning up the test variables."""
        # cls.test_dict = None
        # cls.test_dict_cooc = None
        cls.test_dict_filtered = None

    def test_init(self):
        """Test initialization"""
        self.assertEqual(self.test_dict_filtered.language, "english")

    # def test_gdeps(self):
    #     """Test cooccurrence in google dependency ngrams"""
    #     self.assertTrue(self.test_dict.gdeps.are_related("strongly",
    #                                                      "abatised"))
    #
    # def test_cooccurrence(self):
    #     """Test cooccurrence in the corpus"""
    #     self.assertTrue(self.test_dict.cooccurrence.are_related("fatuorum",
    #                                                             "failed"))

    def test_freqdict(self):
        """Test getting frequency in corpus"""
        self.assertTrue(self.test_dict_filtered.freqdict.data["fatuorum"], 16)

    def test_freqdict_wrap(self):
        """Test getting frequency in corpus (wrapper method)"""
        self.assertTrue(self.test_dict_filtered.frequency_in_corpus("fatuorum"), 16)

    # def test_cooccurrence_wrap(self):
    #     """Test cooccurrence in the corpus (wrapper method)"""
    #     self.assertEqual(self.test_dict.cooccur_in_corpus("pinnock",
    #                                                       "national"), True)
    #
    # def test_cooccurrence_wrap_num(self):
    #     """Test cooccurrence in the corpus (wrapper method)"""
    #     self.assertEqual(self.test_dict_cooc.cooccur_in_corpus("pinnock",
    #                                                            "national"), 2)
    def test_gdeps_wrap(self):
        """Test cooccurrence in google dependency ngrams (wrapper method)"""
        filtered_out = self.test_dict_filtered.cooccur_in_gdeps("strongly",
                                                                "abatised")
        if not filtered_out:
            filtered_out = True
        remained = self.test_dict_filtered.cooccur_in_gdeps("walk", "along")
        self.assertTrue(remained and filtered_out)

    def test_filtering(self):
        filtered_out = "pinnock" in \
                 self.test_dict_filtered.cooccurrence.data
        if not filtered_out:
            filtered_out = True
        remained = "cat" in self.test_dict_filtered.cooccurrence.data
        self.assertTrue(remained and filtered_out)

if __name__ == '__main__':
    unittest.main()
