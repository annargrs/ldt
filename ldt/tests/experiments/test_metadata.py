import unittest

import ldt
import os

from ldt.load_config import config

path_to_resources = config["path_to_resources"]

class Tests(unittest.TestCase):
    """
    The tests in this block inspect generating vector neighborhood data.
    """

    # def test_base(self):
    #     meta = ldt.experiments.metadata.Metadata()
    #     self.assertTrue(meta._metadata["class"], "experiment")
    #
    # def test_class(self):
    #     with self.assertRaises(ValueError):
    #         meta = ldt.experiments.metadata.Metadata(task="get_neighbor")
    #
    # def test_extra_fields(self):
    #     meta = ldt.experiments.metadata.Metadata(
    #         extra_metadata={"my_param" : "my_val"})
    #     self.assertEqual(meta._metadata["my_param"], "my_val")
    #
    # def test_naming(self):
    #     meta = ldt.experiments.metadata.Metadata(experiment_name="test",
    #                                              task="get_neighbors")
    #     correctness = "test" in meta._metadata["name"]
    #     self.assertTrue(correctness)


if __name__ == '__main__':
    unittest.main()
