import unittest

import ldt
import os
import shutil

from ldt.load_config import config

path_to_resources = config["path_to_resources"]

class Tests(unittest.TestCase):
    """
    The tests in this block inspect generating vector neighborhood data.
    """

    @classmethod
    def tearDownClass(cls):
        """Clearning up the test variables."""
        dir = os.path.join(config["path_to_resources"], "experiments/neighbors/testing")
        shutil.rmtree(dir)

    def test_metadata(self):
        res = ldt.experiments.generate_experiment_metadata(
            experiment_name="test", task="testing")
        correctness = "testing" in res["task"]
        self.assertTrue(correctness)

    def test_dir(self):
        res = ldt.experiments.get_neighbors(top_n=5, experiment_name="testing")
        dir = os.path.join(config["path_to_resources"], "experiments/neighbors/testing")
        self.assertTrue(os.path.isdir(dir))

    def test_neighbors(self):
        dir = os.path.join(config["path_to_resources"], "experiments/neighbors/testing")
        files = os.listdir(dir)
        fname = ""
        for f in files:
            if "sample_embeddings" in f:
                f = os.path.join(dir, f)
                with open(f, "r") as sample_neighbor_file:
                    data = sample_neighbor_file.readlines()
                    print(data)
                    res = 'hurricane\t1\tstorm\t0.9598022699356079\n' in data
                    self.assertTrue(res)

if __name__ == '__main__':
    unittest.main()
