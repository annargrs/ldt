import unittest

import ldt
import os
import shutil

import json

import pandas as pd

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
            experiment_name="testing", overwrite=True, top_n=2)
        cls.experiment.get_results()

        normalizer = ldt.dicts.normalize.Normalization(language="English",
                                                       order=("wordnet", "custom"),
                                                       lowercasing=True)
        derivation = ldt.dicts.derivation.meta.DerivationAnalyzer()
        lex_dict = ldt.dicts.semantics.metadictionary.MetaDictionary(
                language="English", order=("wordnet", "wiktionary"))

        # global analyzer
        analyzer = ldt.relations.pair.RelationsInPair(
            normalizer=normalizer, derivation_dict=derivation,
                lex_dict=lex_dict)
        cls.annotation = ldt.experiments.AnnotateVectorNeighborhoods(
            experiment_name="testing", overwrite=True,
            ldt_analyzer=analyzer, ld_scores="main", multiprocessing=1,
                debugging=True)
        cls.annotation.get_results()

        output_scores=["SharedPOS", "SharedMorphForm", "SharedDerivation",
                        "ShortestPathMedian", "CloseInOntology", "Synonyms",
                        "Antonyms",  "Meronyms", "Hyponyms", "Hypernyms",
                        "OtherRelations", "Numbers", "ProperNouns", "Noise",
                        "URLs", "Filenames", "ForeignWords", "Hashtags"]
        cls.scoring = ldt.experiments.LDScoring(experiment_name="testing",
                                                overwrite=True,
                                                ld_scores=output_scores)
        cls.scoring.get_results()

    # @classmethod
    # def tearDownClass(cls):
    #     """Clearning up the test dir."""
    #     cls.experiment = None
    #     subfolders = ["neighbors", "neighbors_annotated", "analysis"]
    #     for sub in subfolders:
    #         dir = os.path.join(config["path_to_resources"], "experiments",
    #                            "testing", sub)
    #         shutil.rmtree(dir)

######## tests for metadata and neighborhoods #############


    def test_dir(self):
        """Creation of subfolder per specific experiment"""
        dir = os.path.join(config["path_to_resources"], "experiments",
                           "testing", "neighbors")
        self.assertTrue(os.path.isdir(dir))

    def test_dataset(self):
        """Testing that the vocabulary sample is loaded"""
        self.assertTrue("activism" in self.experiment.dataset)


    def test_metadata(self):
        """Testing that the experiment metadata is saved"""
        metadata_path = os.path.join(config["path_to_resources"],
                                     "experiments", "testing", "neighbors",
                                     "metadata.json")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        self.assertTrue("timestamp" in metadata)

    def test_metadata_embeddings(self):
        """Testing that the embeddings metadata is incorporated"""
        metadata_path = os.path.join(config["path_to_resources"],
                                     "experiments", "testing", "neighbors",
                                     "metadata.json")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        self.assertTrue("model" in metadata["embeddings"][0])

    def test_metadata_dataset(self):
        """Testing that the dataset metadata is incorporated"""
        metadata_path = os.path.join(config["path_to_resources"],
                                     "experiments", "testing", "neighbors",
                                     "metadata.json")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        self.assertTrue("language" in metadata["dataset"])

    def test_metadata_uuid(self):
        """Testing that the dataset metadata is incorporated"""
        metadata_path = os.path.join(config["path_to_resources"],
                                     "experiments", "testing", "neighbors",
                                     "metadata.json")
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        self.assertTrue("uuid" in metadata and len(metadata["uuid"]) == 36)

    def test_neighbor_extraction(self):
        dir = os.path.join(config["path_to_resources"], "experiments",
                           "testing", "neighbors")
        files = os.listdir(dir)
        fname = ""
        for f in files:
            if "sample_embeddings" in f:
                f = os.path.join(dir, f)
                with open(f, "r") as sample_neighbor_file:
                    data = sample_neighbor_file.readlines()
                    res = 'hurricane\t1\tstorm\t0.9598022699356079\n' in data
                    self.assertTrue(res)

    # def test_overwriting(self):
    #     timestamp = os.path.getmtime(os.path.join(self.experiment.output_dir,
    #                                               "sample_embeddings.tsv"))
    #     exp2 = ldt.experiments.VectorNeighborhoods(experiment_name="testing",
    #                                                overwrite=False, top_n=5)
    #     exp2.get_results()
    #     timestamp2 = os.path.getmtime(os.path.join(exp2.output_dir,
    #                                               "sample_embeddings.tsv"))
    #     self.assertEqual(timestamp, timestamp2)

########## annotation tests #############

    def test_dir_annotation(self):
        """Creation of subfolder per specific experiment"""
        dir = os.path.join(config["path_to_resources"], "experiments",
                           "testing", "neighbors_annotated")
        self.assertTrue(os.path.isdir(dir))

    def test_annotation(self):
        f = os.path.join(config["path_to_resources"], "experiments",
                           "testing", "neighbors_annotated",
                           "sample_embeddings.tsv")
        res_df = pd.read_csv(f, header=0, sep="\t")
        operations_is_lemma = res_df.at[res_df['Neighbor'].eq(
            'operations').idxmax(), 'SharedMorphForm']
        self.assertFalse(operations_is_lemma)

########## analysis tests #############

    def test_dir_analysis(self):
        """Creation of subfolder per specific experiment"""
        dir = os.path.join(config["path_to_resources"], "experiments",
                           "testing", "analysis")
        self.assertTrue(os.path.isdir(dir))

    def test_analysis(self):
        """Creation of subfolder per specific experiment"""
        file = os.path.join(config["path_to_resources"], "experiments",
                            "testing", "analysis", "ld_scores.tsv")
        res_df = pd.read_csv(file, header=0, sep="\t")
        hashtags = res_df.at[res_df['LDScores'].eq(
            'Synonyms').idxmax(), 'sample_embeddings']
        self.assertEqual(hashtags, 0.0)

if __name__ == '__main__':
    unittest.main()
