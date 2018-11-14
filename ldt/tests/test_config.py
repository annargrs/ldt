# -*- coding: utf-8 -*-
"""Testing the loading of the configuration file."""

import unittest
import os

os.environ["TESTING_LDT"] = "TRUE"

import ldt
from ldt.load_config import config

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the loading of config file.
    """

    def test_config(self):
        """Test default language loading."""
        res = config
        self.assertEqual("English", res["default_language"])

if __name__ == '__main__':
    unittest.main()
