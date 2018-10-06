
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
from ldt.experiments.annotate import get_fname_for_embedding
from ldt.load_config import config

class LDScoring(Experiment):
    """This class provides a simple interface for computing ld scores,
    given a collection of annotated vector neighborhood files.
    Vecto-style metadata is also generated."""

    def __init__(self, experiment_name=None, extra_metadata=None,
                 overwrite=False, output_dir=os.path.join(
                     config["path_to_resources"], "experiments")):

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

        Returns:

            (None): a table with ld scores for all available variables,
                together with the experiment metadata.

        """

        super(LDScoring, self).__init__(
            experiment_name=experiment_name, extra_metadata=extra_metadata, \
            overwrite=overwrite, embeddings=None, output_dir=output_dir,
            dataset=None, experiment_subfolder="analysis")

        self._metadata["task"] = "ld_scoring"
        self._metadata["uuid"] = str(uuid.uuid4())
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
            self._metadata["embeddings"] = neighbors_metadata["embeddings"]
            self.embeddings = []
            for embedding in self._metadata["embeddings"]:
                self.embeddings.append(embedding["path"])

        self.supported_vars = ["SharedPOS", "SharedMorphForm",
                               "SharedDerivation", "NonCooccurring",
                               "GDeps", "TargetFrequency",
                               "NeighborFrequency", "Associations",
                               "ShortestPath", "Synonyms", "Antonyms",
                               "Meronyms", "Hyponyms", "Hypernyms",
                               "OtherRelations", "Numbers", "ProperNouns",
                               "Noise", "URLs", "Filenames",
                               "ForeignWords", "Hashtags"]

        self.continuous_vars = ['ShortestPath', 'TargetFrequency',
                                'NeighborFrequency', 'CloseNeighbors',
                                'FarNeighbors']

        self.binary_vars = [x for x in self.supported_vars if not \
            x in self.continuous_vars]

        self.message = None

    def _load_dataset(self, dataset):
        """Dataset for generating vector neighborhoods was already processed in
        the previous stage of the experiment, so nothing needs to be done
        here."""
        pass

    def _process(self, embeddings_path):
        filename = get_fname_for_embedding(embeddings_path)
        annotated_file_path = os.path.join(self.output_dir.replace(
            "analysis", "neighbors_annotated"), filename)
        input_df = pd.read_csv(annotated_file_path, header=0, sep="\t")

        len_df = len(input_df)

        def percentage(num, len_df=len_df):
            """Helper for formatting % numbers"""
            return round(100*num/len_df, 2)

        # print(input_df.head())
        res = {"Embedding":filename}
        # # dicts = input_df.to_dict(orient="records")
        for var in self.binary_vars:
            if var in input_df.columns:
                try:
                    res[var] = percentage(num=list(input_df[var]).count(True))
                except KeyError:
                    pass
        # if "ShortestPath" in self.binary_vars:
        if "NeighborFrequency" in input_df.columns:
            highfreq_neighbors = [x for x in list(
                input_df["NeighborFrequency"]) if x > 10000]
            res["HighFreqNeighbors"] = percentage(len(highfreq_neighbors))
            res["LowFreqNeighbors"] = 1-res["HighFreqNeighbors"]
        if "Similarity" in input_df.columns:
            far_neighbors = [x for x in list(
                input_df["Similarity"]) if x < 0.7]
            close_neighbors = [x for x in list(
                input_df["Similarity"]) if x > 0.8]
            res["FarNeighbors"] = percentage(len(far_neighbors))
            res["CloseNeighbors"] = percentage(len(close_neighbors))
        return res


    def get_results(self):
        """The basic routine for processing embeddings one-by-one, and saving
        the timestamps of when each file was started and finished."""
        input_data = self.find_unprocessed_files()
        self.embeddings = input_data
        res = []
        for i in self.embeddings:

            # uuid = self._check_uuid_in_metadata(field="embeddings", path=i)

            res.append(self._process(embeddings_path=i))
            cols = ["Embedding", "SharedPOS", "SharedMorphForm",
                    "SharedDerivation", "NonCooccurring", "GDeps",
                    "LowFreqNeighbors", "HighFreqNeighbors", "FarNeighbors",
                    "CloseNeighbors", "Associations", "ShortestPath",
                    "Synonyms", "Antonyms", "Meronyms", "Hyponyms",
                    "Hypernyms", "OtherRelations", "Numbers", "ProperNouns",
                    "Noise", "URLs", "Filenames", "ForeignWords", "Hashtags"]
            res_df = pd.DataFrame(res, columns=cols)
            res_df.to_csv(os.path.join(self.output_dir, "ld_scores.tsv"),
                          index=False, sep="\t")
            self._metadata["timestamp"] = datetime.datetime.now().isoformat()
            self.save_metadata()

# if __name__ == '__main__':
#     annotation = LDScoring(experiment_name="testing", overwrite=True)
#     annotation.get_results()
