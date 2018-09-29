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

Todo:

    * distinct filenames from varying parameters and model names

"""

import os
import datetime
import warnings

import pandas as pd
import vecto.embeddings
from vecto.utils.data import save_json

from ldt import load_resource
from ldt import __version__
from ldt.load_config import config

def generate_identifiable_filenames():
    pass


def generate_experiment_metadata(experiment_name, task):
    """Generating experiment metadata consistent with Vecto library format.
    See `Vecto docs <https://vecto.readthedocs.io/en/docs/tutorial/metadata
    .html>`_ for more detail.

    Args:
        experiment_name: the human-readable name of the experiment (e.g.
            "Profiling CBOW dims 25-500")
        task: the type of experiment being performed (in LDT - generating or
            annotating vector neighborhoods)

    Returns:
        (dict): dictionary with metadata fields

    """
    metadata = {}
    metadata["timestamp"] = datetime.datetime.now().isoformat()
    metadata["class"] = "experiment"
    metadata["name"] = experiment_name
    metadata["task"] = task
    metadata["version"] = __version__
    metadata["cite"] = \
        [{"contribution": "LDT library",
          "bibtex": {
              "type": "inproceedings",
              "id": "RogersAnanthakrishnaEtAl_2018",
              "author": [{"name": "Anna Rogers"},
                         {"name": "Shashwath Hosur Ananthakrishna"},
                         {"name": "Anna Rumshisky"}],
              "title": "What's in Your Embedding, And How It Predicts Task "
                       "Performance",
              "url": "http://aclweb.org/anthology/C18-1228",
              "address": "Santa Fe, New Mexico, USA, August 20-26, 2018",
              "publisher": "ACL",
              "booktitle": "Proceedings of the 27th International "
                           "Conference on Computational Linguistics",
              "year": 2018,
              "pages": "2690–2703"
              }
         }
        ]
    return metadata

def get_neighbors(top_n=100,
                  embeddings_paths=config["experiments"]["embeddings"],
                  vocab_sample=config["experiments"]["vocab_sample"],
                  experiment_name=None,
                  normalize=True):
    """ Retrieving top *n* neighbors for a given vocab sample

    Args:
        top_n (int): how many top neighbors should be retrieved for each word.
        embeddings_paths (list of str): the locations of embeddings folders
            (one embedding per folder).
        vocab_sample (str or list of str): the location of vocabulary sample
            file, or list of words to get the neighbors for.
        experiment_name (str): the human-readable name for the current
            experiment, which will be used to make a subfolder storing the
            generated data. If None, the folder will be simply timestamped.
        normalize (bool): whether the input embeddings should be normalized.

    Returns:
        (None): the neighbors file will be written to disk together with the
        experiment metadata

    """
    print("\n\nIf your embeddings are not normalized, retrieving neighbors "
          "will take more time. By default LDT normalizes them on loading. "
          "If you need them not normalized, use normalize=False option.\n")

    # timestamping
    if not experiment_name:
        experiment_name = datetime.datetime.now().isoformat()

    # experiment metadata
    metadata = generate_experiment_metadata(
        experiment_name="LDT (neighbor extraction): " +experiment_name,
        task="Retrieving vector neighborhoods")

    out_path = os.path.join(config["path_to_resources"],
                            "experiments/neighbors")
    out_path = os.path.join(out_path, experiment_name)
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    # loading the vocabulary sample
    if isinstance(vocab_sample, str):
        vocab_sample = os.path.join(config["path_to_resources"],
                                    "experiments/vocab_samples/"+vocab_sample)
        vocab_sample = load_resource(vocab_sample, format="vocab")

    # processing embeddings
    for embeddings_path in embeddings_paths:
        print(embeddings_path)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            embeddings = vecto.embeddings.load_from_dir(embeddings_path)
            if normalize:
                embeddings.normalize()

        # get dictionary with list of lists
            neighbors = []
            for word in vocab_sample:
                neighbor_list = embeddings.get_most_similar_words(word,
                                                                  cnt=top_n+1)[1:]
                for i in enumerate(neighbor_list):
                    pair = []
                    pair.append(word)
                    pair.append(i[0]+1)
                    pair.append(neighbor_list[i[0]][0])
                    pair.append(neighbor_list[i[0]][1])
                    neighbors.append(pair)

            # formatting the output
            res = pd.DataFrame(neighbors, columns=["Target", "Rank", "Neighbor",
                                                   "Similarity"])
            res.to_csv(path_or_buf=os.path.join(out_path,
                                                embeddings.metadata["model"]),
                       header=True,
                       index=False,
                       sep="\t")
            embeddings = None
    save_json(metadata, os.path.join(out_path, "metadata.json"))

