import unittest

import ldt
import os
import shutil

from ldt.load_config import config as config

path_to_resources = config["path_to_resources"]

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the Wiktionary cache:
    updating the vocab list cache for a given language.
    """

    def test_find_wiktionary_vocab(self):
        res = ldt.helpers.wiktionary_cache.find_vocab_file(language="zu",
        path_to_cache=path_to_resources)
        correctness = "zu" in res or res == "none"
        self.assertTrue(correctness)

    def test_get_timestamped_vocab_filenames(self):
        res = ldt.helpers.wiktionary_cache.get_timestamped_vocab_filenames(
            filename = "none", language = "zu")
        self.assertIn("new_filename", res.keys())

    def test_update_cache(self):
        res = ldt.helpers.wiktionary_cache.update_wiktionary_cache(
            language="zu")
        self.assertFalse(res)

    def test_load_cache(self):
        res = ldt.helpers.wiktionary_cache.load_wiktionary_cache(
            language="zu", lowercasing = True)
        worked = "-dlula" in res
        self.assertTrue(worked)

    def test_cleanup(self):
        path_to_cache = os.path.join(path_to_resources, "cache")
        for f in os.listdir(path_to_cache):
            os.remove(os.path.join(path_to_cache, f))

if __name__ == '__main__':
    unittest.main()
