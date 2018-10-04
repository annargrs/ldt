import unittest

import ldt
import os

from ldt.load_config import config

path_to_resources = config["path_to_resources"]

class Tests(unittest.TestCase):
    """
    The tests in this block inspect annotating vector neighborhood data.
    """
    pass
    # @classmethod
    # def setUpClass(cls):
    #     """Setting up the test variables."""
    #     cls.experiment = ldt.experiments.AnnotateVectorNeighborhoods(
    #         experiment_name="testing", overwrite=True)
    #     cls.experiment.get_results()
    #
    # @classmethod
    # def tearDownClass(cls):
    #     """Clearning up the test dir."""
    #     cls.experiment = None
    #     dir = os.path.join(config["path_to_resources"], "experiments",
    #                        "neighbors_annotated", "testing")
    #     shutil.rmtree(dir)
    #
    # def test_dir(self):
    #     """Creation of subfolder per specific experiment"""
    #     dir = os.path.join(config["path_to_resources"], "experiments",
    #                        "neighbors_annotated", "testing")
    #     self.assertTrue(os.path.isdir(dir))

if __name__ == '__main__':
    unittest.main()
