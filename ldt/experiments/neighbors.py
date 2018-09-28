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

Todo:

    * folder-per-neighbors with metadata
    * folder name creation with detecting the model parameters that
        differ in the input models
    * experiment metadata
    * timestamps in the experiments
    * pylinting
    * tests

"""

import os

import vecto.embeddings

import pandas as pd

from ldt import load_resource
from ldt.load_config import config


def detect_varying_parameters:
    """Detecting what parameters vary in the input vecto embedding
    metadata"""
    pass

def get_neighbors(top_n=100,
                  embeddings_paths=config["experiments"]["embeddings"],
                  vocab_sample=config["experiments"]["vocab_sample"],
                  normalize=True):
    """ Retrieving top *n* neighbors for a given vocab sample

    Args:
        top_n (int): how many top neighbors should be retrieved for each word.
        embeddings_paths (list of str): the locations of embeddings folders
            (one embedding per folder)
        vocab_sample (str or list of str): the location of vocabulary sample
            file, or list of words to get the neighbors for

    Returns:
        (None): the neighbors file will be written to disk together with the
        experiment metadata

    """

    out_path = os.path.join(config["path_to_resources"],
                            "experiments/neighbors")
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    if isinstance(vocab_sample, str):
        vocab_sample = os.path.join(config["path_to_resources"],
                                    "experiments/vocab_samples/"+vocab_sample)
        print(vocab_sample)
        vocab_sample = load_resource(vocab_sample, format="vocab")
        print(vocab_sample)

    for embeddings_path in embeddings_paths:

        embeddings = vecto.embeddings.load_from_dir(embeddings_path)
        out_fname = os.path.join(out_path, embeddings.metadata["model"])
        if normalize:
            embeddings.normalize()

    # get dictionary with list of lists
        neighbors = []
        for word in vocab_sample:
            neighbor_list = embeddings.get_most_similar_words(word,
                                                              cnt=top_n+1)[1:]
            for i in range(len(neighbor_list)):
                pair = []
                pair.append(word)
                pair.append(i+1)
                pair.append(neighbor_list[i][0])
                pair.append(neighbor_list[i][1])
                neighbors.append(pair)

        df = pd.DataFrame(neighbors, columns=["Target", "Rank", "Neighbor",
                                              "Similarity"])
        df.to_csv(path_or_buf=out_fname, header=True, index=False, sep="\t")




