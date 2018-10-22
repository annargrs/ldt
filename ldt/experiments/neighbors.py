# -*- coding: utf-8 -*-
"""Sampling vector neighborhoods.

This module provides functionality for sampling top_n most similar words for
a given vocab sample from a list of word embeddings resources.

The embeddings are accessed through vecto library, which assumes that each
embedding is contained in a separate directory and accompanied with a
``metadata.json`` file, which describes its parameters and allows to
bundle this information with LDT results for better reproducibility and
tracking of experiments. See `Vecto documentation
<https://vecto.readthedocs.io/en/docs/tutorial/metadata.html#the-embeddings
-metadata>`_for more details.
By default, embeddings are normalized before cosine similarity is computed.


"""

import os
import warnings
import uuid

import pandas as pd
import vecto.embeddings
from vecto.utils.data import load_json

from ldt import load_resource
from ldt import __version__
from ldt.load_config import config
from ldt.experiments.metadata import Experiment



class VectorNeighborhoods(Experiment):
    """This class provides a simple interface for generating top_n vector
    neighborhoods for a given vocabulary sample, using vecto library.
    Vecto-style metadata is also generated."""

    #pylint: disable=too-many-arguments

    def __init__(self, experiment_name=config["experiments"]["experiment_name"],
                 extra_metadata=None,
                 overwrite=config["experiments"]["overwrite"],
                 top_n=config["experiments"]["top_n"], normalize=True,
                 embeddings=config["experiments"]["embeddings"],
                 output_dir=os.path.join(config["path_to_resources"],
                                         "experiments"),
                 dataset=config["experiments"]["vocab_sample"]):

        """ Retrieving top *n* neighbors for a given vocab sample

        Args:
            experiment_name (str): the human-readable name for the
                current experiment, which will be used to make a subfolder
                storing the generated data. If None, the folder will be simply
                timestamped.
            extra_metadata (dict): any extra fields to be added to the
                experiment metadata (overwriting any previously existing fields)
            embeddings (list of str): a list of paths to input
                data (each containing a metadata.json file).
            output_dir (str): the *existing* path for saving the *subfolder*
                named with the specified experiment_name, where the output data
                and metadata.json file will be saved.
            dataset (str): the location of the dataset to be used in the
                experiment.
            overwrite (bool): if True, any previous data for the same
                experiment will be overwritten, and the experiment will be
                re-started.
            top_n (int): how many top neighbors should be retrieved
                for each word.
            normalize (bool): whether the input embeddings should be
                normalized.

        Returns:
            (None): the neighbors file will be written to disk
                together with the experiment metadata

        """

        super(VectorNeighborhoods, self).__init__(
            experiment_name=experiment_name, extra_metadata=extra_metadata, \
            overwrite=overwrite, embeddings=embeddings, output_dir=output_dir,
            dataset=dataset, experiment_subfolder="neighbors")

        self.message = "\n\nIf your embeddings are not normalized, retrieving " \
                       "neighbors will take more time. By default LDT " \
                       "normalizes them on loading. If you need them not " \
                       "normalized, use normalize=False option.\n"

        self._metadata["task"] = "get_neighbors"
        self._metadata["uuid"] = str(uuid.uuid4())
        self._metadata["top_n"] = top_n
        self._load_dataset(dataset=dataset)

        self._normalize = normalize
        self._top_n = top_n

    def _load_dataset(self, dataset):
        """Loading the vocabulary file from the location specified in the
        ldt config file. If vecto-style metadata is found, it will also be
        bundled with the experiment metadata automatically.

        Args:
            dataset (str): either a full path to the dataset or a subfolder
            of "experiments/vocab_samples" folder in the general ldt
            resources location.

        Returns:
            None
        """
        dataset_metadata_path = \
            os.path.join(config["path_to_resources"], "experiments",
                         "vocab_samples", dataset, "metadata.json")
        if os.path.isfile(dataset_metadata_path):
            self._metadata["dataset"] = load_json(dataset_metadata_path)
        else:
            self._metadata["dataset"] = dataset
        dataset_path = dataset_metadata_path.strip("metadata.json")
        # assume there is a single ".vocab" file in the dataset folder

        file = [x for x in os.listdir(dataset_path) if x.endswith(".vocab")][0]
        dataset = load_resource(os.path.join(dataset_path, file),
                                format="vocab")
        self.dataset = dataset

    def _process(self, embeddings_path):
        """Extracting top_n neighbors from each of the embeddings,
        saving the results as tab-separated file in the output directory.

        Args:
            embeddings_path (str): the full path to a folder containing one
                word embedding file (any format supported by vecto library).
                If a metadata.json file is present, it will be automatically
                bundled with the experiment metadata.

        Returns:
            None
        """
        print("Extracting neighbors:", embeddings_path)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            embeddings = vecto.embeddings.load_from_dir(embeddings_path)
            if self._normalize:
                embeddings.normalize()

            # get dictionary with list of lists
            neighbors = []
            for word in self.dataset:
                neighbor_list = embeddings.get_most_similar_words(
                    word, cnt=self._top_n + 1)[1:]
                for i in enumerate(neighbor_list):
                    pair = []
                    pair.append(word)
                    pair.append(i[0] + 1)
                    pair.append(neighbor_list[i[0]][0])
                    pair.append(neighbor_list[i[0]][1])
                    neighbors.append(pair)

            # formatting the output
            res = pd.DataFrame(neighbors, columns=["Target", "Rank",
                                                   "Neighbor",
                                                   "Similarity"])
            res.to_csv(path_or_buf=os.path.join(self.output_dir,
                                                embeddings.metadata[
                                                    "model"]+".tsv"),
                       header=True, index=False, sep="\t")
            embeddings = None

if __name__ == '__main__':
    annotation = VectorNeighborhoods(experiment_name="testing", overwrite=True)
    annotation.get_results()