# -*- coding: utf-8 -*-
"""Testing the analysis of relations in word pairs"""

import unittest
import os

os.environ["TESTING_LDT"] = "TRUE"

import ldt
from ldt.helpers.ignore import ignore_warnings

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the detection of the smallest distance
    between word senses of the two words.
    """

    @classmethod
    @ignore_warnings
    def setUpClass(cls):
        """Setting up the test variables."""
        cls.test_dict = ldt.relations.ontology_path.ontodict.OntoDict(
            language="English")

    @classmethod
    def tearDownClass(cls):
        """Clearning up the test variables."""
        cls.test_dict = None

    def test_init(self):
        self.assertEqual(self.test_dict.language,"en")

    @ignore_warnings
    def test_sim(self):
        self.assertEqual(self.test_dict.get_shortest_path("cat", "dog"), 0.05)

if __name__ == '__main__':
    ldt.config = ldt._test_config
    unittest.main()