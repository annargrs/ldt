
"""Analyzing ldt annotation.

This module provides functionality for analyzing ldt annotations of
vector neighborhoods. The input is a directory with annotated files and
metadata.json file, prepared by
:class:`~ldt.experiments.annotate.AnnotateVectorNeighborhoods` class. See the
documentation of that class for more details.

The output is saved in the experiments/analysis/your_experiment_name
subfolder of the ldt resource folder specified in the configuration file.
These are tab-separated data files with columns that contain ld
scores, as described `here <http://ldtoolkit.space/ldscores/>`_.

These scores are the basic profile of the information captured by a given
word embedding. They can be used for evaluation, error analysis, parameter
tuning and hypothesis-driven model development, as described `here
<http://ldtoolkit.space/analysis/examples/>`_.

"""

import os
import uuid
import datetime

import pandas as pd

from vecto.utils.data import load_json

from ldt.experiments.metadata import Experiment
from ldt.load_config import config

class LDScoring(Experiment):
    """This class provides a simple interface for computing ld scores,
    given a collection of annotated vector neighborhood files.
    Vecto-style metadata is also generated."""

    def __init__(self, experiment_name=config["experiments"]["experiment_name"],
                 extra_metadata=None,
                 overwrite=config["experiments"]["overwrite"],
                 ld_scores="main", output_dir=
                 os.path.join(config["path_to_resources"], "experiments")):

        """ Annotating pre-computed top *n* neighbors for a given vocab sample

        Args:
            experiment_name (str): the human-readable name for the
                current experiment, which will be used to make a subfolder
                storing the generated data. If None, the folder will be simply
                timestamped.
            extra_metadata (dict): any extra fields to be added to the
                experiment metadata (overwriting any previously existing fields)
            output_dir (str): the *existing* path for saving the *subfolder*
                named with the specified experiment_name, where the output data
                and metadata.json file will be saved.
            overwrite (bool): if True, any previous data for the same
                experiment will be overwritten, and the experiment will be
                re-started.
            ld_scores (str or list of str): "all" for all supported scores,
                or a list of ld_scores. Supported values are:

                    - "SharedPOS",
                    - "SharedMorphForm",
                    - "SharedDerivation",
                    - "NonCooccurring",
                    - "CloseNeighbors",
                    - "FarNeighbors",
                    - "LowFreqNeighbors",
                    - 'HighFreqNeighbors',
                    - "GDeps",
                    - "TargetFrequency",
                    - "NeighborFrequency",
                    - "Associations",
                    - "ShortestPathMedian",
                    - "CloseInOntology",
                    - "Synonyms",
                    - "Antonyms",
                    - "Meronyms",
                    - "Hyponyms",
                    - "Hypernyms",
                    - "OtherRelations",
                    - "Numbers",
                    - "ProperNouns",
                    - "Misspellings",
                    - "URLs",
                    - "Filenames",
                    - "ForeignWords",
                    - "Hashtags",
                    - "Noise".

        Returns:

            (None): a table with ld scores for all available variables,
                together with the experiment metadata.

        """

        super(LDScoring, self).__init__(
            experiment_name=experiment_name, extra_metadata=extra_metadata, \
            overwrite=overwrite, embeddings=None, output_dir=output_dir,
            dataset=None, experiment_subfolder="analysis")

        self.metadata["task"] = "ld_scores_analysis"
        self.metadata["uuid"] = str(uuid.uuid4())
        self._load_dataset(dataset=None)
        neighbors_metadata_path = self.output_dir.replace(
            "analysis", "neighbors_annotated")
        neighbors_metadata_path = os.path.join(neighbors_metadata_path,
                                               "metadata.json")
        if not os.path.isfile(neighbors_metadata_path):
            raise IOError("The metadata for the annotated neighborhood files "
                          "was not found at "+neighbors_metadata_path)
        else:
            neighbors_metadata = load_json(neighbors_metadata_path)
            self.metadata["embeddings"] = neighbors_metadata["embeddings"]
            self.metadata["annotation"] = neighbors_metadata
            del self.metadata["annotation"]["embeddings"]
            self.embeddings = []
            for embedding in self.metadata["embeddings"]:
                self.embeddings.append(embedding["path"])


        self.supported_vars = ["SharedPOS", "SharedMorphForm",
                               "SharedDerivation", "NonCooccurring",
                               "GDeps", "TargetFrequency",
                               "NeighborFrequency", "Associations",
                               "ShortestPath", "Synonyms", "Antonyms",
                               "Meronyms", "Hyponyms", "Hypernyms",
                               "OtherRelations", "Numbers", "ProperNouns",
                               "Misspellings", "URLs", "Filenames",
                               "ForeignWords", "Hashtags", "Noise"]

        self.continuous_vars = ['ShortestPath', 'TargetFrequency',
                                'NeighborFrequency', 'CloseNeighbors',
                                'FarNeighbors']

        self.binary_vars = [x for x in self.supported_vars if not \
            x in self.continuous_vars]

        output_vars = ["Model", "SharedPOS", "SharedMorphForm",
                       "SharedDerivation", "NonCooccurring",
                       "CloseNeighbors", "FarNeighbors",
                       "LowFreqNeighbors", 'HighFreqNeighbors', "GDeps",
                       "Associations", "ShortestPathMedian", "CloseInOntology",
                       "Synonyms", "Antonyms",  "Meronyms", "Hyponyms",
                       "Hypernyms", "OtherRelations", "Numbers", "ProperNouns",
                       "Misspellings", "URLs", "Filenames", "ForeignWords",
                       "Hashtags", "Noise"]

        # corpus_specific = ["NonCooccurring", "LowFreqNeighbors",
        #                    "HighFreqNeighbors"]
        #
        # if not config["corpus"]:
        #     output_vars = [x for x in output_vars if not x in corpus_specific]

        output_scores_error = "The ld_scores argument is invalid. It should " \
                              "be 'all' for all supported relations, " \
                              "or a list with one or more of the following " \
                              "values:\n" + ", ".join(output_vars)

        if ld_scores == "all":
            self.output_vars = output_vars
        elif ld_scores == "main":
            exclude = ["ShortestPathMedian", "URLs", "Filenames", "Hashtags",
                       "Noise"]
            if not config["corpus"]:
                exclude += ["NonCooccurring", "LowFreqNeighbors",
                            'HighFreqNeighbors', "GDeps"]

            self.output_vars = [x for x in output_vars if not x in exclude]

        else:
            if isinstance(ld_scores, list):
                unsupported = [x for x in ld_scores if not x in output_vars]
                if unsupported:
                    raise ValueError(output_scores_error)
                else:
                    self.output_vars = [x for x in output_vars if x in
                                        ld_scores]
                    self.output_vars = ["Model"] + self.output_vars
            else:
                raise ValueError(output_scores_error)
        self.metadata["ld_scores"] = self.output_vars
        self.message = None

    def _load_dataset(self, dataset):
        """Dataset for generating vector neighborhoods was already processed in
        the previous stage of the experiment, so nothing needs to be done
        here."""
        pass

    def _process(self, embeddings_path, lowfreq_threshold=10000,
                      far_neighbors_threshold=0.7,
                      close_neighbors_threshold=0.8, ontology_threshold=0.5):
        """

        Args:
            embeddings_path (str): the name of embedding model to process (
                currently taken to be the name of the corresponding file with
                annotated neighbors).
            lowfreq_threshold (int): neighbors below this number will be
                considered low-frequency, and those above this number -
                high-frequency.
            far_neighbors_threshold (float): neighbors further than this number
                will be considered as "far neighbors".
            close_neighbors_threshold (float): neighbors closer than this
                number will be considered as "close neighbors".
            ontology_threshold (float): neighbors closer in ontology than this
                number will be considered "CloseInOntology".

        Returns:

        """
        filename = self.get_fname_for_embedding(embeddings_path)

        annotated_file_path = os.path.join(self.output_dir.replace(
            "analysis", "neighbors_annotated"), filename+".tsv")
        input_df = pd.read_csv(annotated_file_path, header=0, sep="\t")

        len_df = len(input_df)

        def percentage(num, len_df=len_df):
            """Helper for formatting % numbers"""
            return round(100*num/len_df, 2)
        res = {"Model": filename}
        for var in self.binary_vars:
            if var in input_df.columns:
                try:
                    res[var] = percentage(num=list(input_df[var]).count(True))
                except KeyError:
                    pass

        if "ShortestPath" in input_df.columns:
            # median of all found shortest paths - that's what was done in
            # the paper
            res["ShortestPathMedian"] = \
                round(input_df["ShortestPath"].median(), 3)
            # number of words with paths shorter than threshold
            close = [x for x in list(
                input_df["ShortestPath"]) if x <= ontology_threshold]
            res["CloseInOntology"] = len(close)
        if "NeighborFrequency" in input_df.columns:
            highfreq_neighbors = [x for x in list(
                input_df["NeighborFrequency"]) if isinstance(x, float)]
            highfreq_neighbors = [x for x in highfreq_neighbors if x >
                                  lowfreq_threshold]
            res["HighFreqNeighbors"] = percentage(len(highfreq_neighbors))
            res["LowFreqNeighbors"] = 100-res["HighFreqNeighbors"]
        if "Similarity" in input_df.columns:
            far_neighbors = [x for x in list(
                input_df["Similarity"]) if x <= far_neighbors_threshold]
            close_neighbors = [x for x in list(
                input_df["Similarity"]) if x >= close_neighbors_threshold]
            res["FarNeighbors"] = percentage(len(far_neighbors))
            res["CloseNeighbors"] = percentage(len(close_neighbors))
        filtered_res = {}
        for i in res:
            if i in self.output_vars:
                filtered_res[i] = res[i]
        return filtered_res


    def get_results(self):
        """The basic routine for processing embeddings one-by-one, and saving
        the timestamps of when each file was started and finished."""

        if not self._overwrite:
            if os.path.isfile(os.path.join(self.output_dir, "ld_scores.tsv")):
                return None

        # self.embeddings = input_data
        res = []
        for i in self.embeddings:

            res.append(self._process(embeddings_path=i))

            for i in ["GDeps", "NonCooccurring"]:
                if not i in res[0]:
                    if i in self.output_vars:
                        self.output_vars.remove(i)

            res_df = pd.DataFrame(res, columns=self.output_vars)
            # res_df = res_df.set_index("Model")
            res_df = res_df.transpose()
            res_df.columns = res_df.iloc[0]
            res_df = res_df[1:]
            res_df.to_csv(os.path.join(self.output_dir, "ld_scores.tsv"),
                          index=True, sep="\t", header=1,
                          index_label="LDScores")
            self.metadata["timestamp"] = datetime.datetime.now().isoformat()
            self.save_metadata()

if __name__ == '__main__':
    annotation = LDScoring(experiment_name="testing", overwrite=True)
    annotation.get_results()
