import unittest

import ldt
import os
import shutil

import json

from ldt.load_config import config
from ldt.helpers.ignore import ignore_warnings

path_to_resources = config["path_to_resources"]

class Tests(unittest.TestCase):
    """
    The tests in this block inspect generating vector neighborhood data.
    """

    @classmethod
    @ignore_warnings
    def setUpClass(cls):
        """Setting up the test variables."""
        cls.experiment = ldt.experiments.VectorNeighborhoods(
            experiment_name="testing", overwrite=True, top_n=5)
        cls.experiment.get_results()

        normalizer = ldt.dicts.normalize.Normalization(language="English",
                                                       order=("wordnet", "custom"),
                                                       lowercasing=True)
        derivation = ldt.dicts.derivation.meta.DerivationAnalyzer()
        lex_dict = ldt.dicts.semantics.metadictionary.MetaDictionary(order=(
            "wordnet","wiktionary"))

        analyzer = ldt.relations.pair.RelationsInPair(
            normalizer=normalizer, derivation_dict=derivation, lex_dict=lex_dict)
        cls.annotation = ldt.experiments.AnnotateVectorNeighborhoods(
            experiment_name="testing", overwrite=False,
            ldt_analyzer=analyzer)
        cls.annotation.get_results()

    # @classmethod
    # def tearDownClass(cls):
    #     """Clearning up the test dir."""
    #     cls.experiment = None
    #     dir = os.path.join(config["path_to_resources"], "experiments",
    #                        "neighbors", "testing")
    #     shutil.rmtree(dir)

######## tests for metadata and neighborhoods #############


    def test_dir(self):
        """Creation of subfolder per specific experiment"""
        dir = os.path.join(config["path_to_resources"], "experiments",
                           "neighbors", "testing")
        self.assertTrue(os.path.isdir(dir))

    def test_dataset(self):
        """Testing that the vocabulary sample is loaded"""
        self.assertTrue("activism" in self.experiment.dataset)


    def test_metadata(self):
        """Testing that the experiment metadata is saved"""
        metadata_path = os.path.join(config["path_to_resources"],
                                     "experiments", "neighbors", "testing",
                                     "metadata.json")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        self.assertTrue("timestamp" in metadata)

    def test_metadata_embeddings(self):
        """Testing that the embeddings metadata is incorporated"""
        metadata_path = os.path.join(config["path_to_resources"],
                                     "experiments", "neighbors", "testing",
                                     "metadata.json")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        self.assertTrue("model" in metadata["embeddings"][0])

    def test_metadata_dataset(self):
        """Testing that the dataset metadata is incorporated"""
        metadata_path = os.path.join(config["path_to_resources"],
                                     "experiments", "neighbors", "testing",
                                     "metadata.json")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        self.assertTrue("language" in metadata["dataset"])

    def test_metadata_uuid(self):
        """Testing that the dataset metadata is incorporated"""
        metadata_path = os.path.join(config["path_to_resources"],
                                     "experiments", "neighbors", "testing",
                                     "metadata.json")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        self.assertTrue("uuid" in metadata and len(metadata["uuid"]) == 36)

    def test_neighbor_extraction(self):
        dir = os.path.join(config["path_to_resources"], "experiments",
                           "neighbors", "testing")
        files = os.listdir(dir)
        fname = ""
        for f in files:
            if "sample_embeddings" in f:
                f = os.path.join(dir, f)
                with open(f, "r") as sample_neighbor_file:
                    data = sample_neighbor_file.readlines()
                    res = 'hurricane\t1\tstorm\t0.9598022699356079\n' in data
                    self.assertTrue(res)

    def test_overwriting(self):
        timestamp = os.path.getmtime(os.path.join(self.experiment.output_dir,
                                                  "sample_embeddings.tsv"))
        exp2 = ldt.experiments.VectorNeighborhoods(experiment_name="testing",
                                                   overwrite=False, top_n=5)
        exp2.get_results()
        timestamp2 = os.path.getmtime(os.path.join(exp2.output_dir,
                                                  "sample_embeddings.tsv"))
        self.assertEqual(timestamp, timestamp2)

########## annotation tests #############

    def test_dir_annotation(self):
        """Creation of subfolder per specific experiment"""
        dir = os.path.join(config["path_to_resources"], "experiments",
                           "neighbors_annotated", "testing")
        self.assertTrue(os.path.isdir(dir))

    def test_annotation(self):
        f = os.path.join(config["path_to_resources"], "experiments",
                           "neighbors_annotated", "testing",
                           "sample_embeddings.tsv")
        with open(f, "r") as sample_annotated_file:
            data = sample_annotated_file.readlines()
            res = 'premiership\t1\tsemi-final\t0.962702751159668\tTrue\tFalse' \
                  '\tFalse' in data[1]
            self.assertTrue(res)

if __name__ == '__main__':
    unittest.main()
