# -*- coding: utf-8 -*-
"""Annotating vector neighborhoods.

This module provides functionality for annotating vector neighborhoods
obtained from a number of word embeddings.

This is the second (and most important) step in LDT analysis workflow. The
input is pre-computed vector neighborhood files that are prepared with
:class:`~ldt.experiments.neighbors.VectorNeighborhoods` class. See the
documentation of that class for more details.

The output is saved in the experiments/neighbors_annotated/your_experiment_name
subfolder of the ldt resource folder specified in the configuration file.
These are tab-separated data files with columns indicating the presence of a
binary relation in target_neighbor word pairs (e.g. whether they are
synonyns), or a numerical indicator of a relationship (e.g. the distance
between them in an ontology). See the full list of available scores `here
<http://ldtoolkit.space/ldscores/>`_.

"""

import os
import warnings
import uuid

import pandas as pd

from vecto.utils.data import load_json

from ldt.experiments.metadata import Experiment
from ldt.load_config import config
from ldt.dicts.normalize import Normalization
from ldt.dicts.derivation.meta import DerivationAnalyzer
from ldt.dicts.semantics.metadictionary import MetaDictionary
from ldt.relations.pair import RelationsInPair

class AnnotateVectorNeighborhoods(Experiment):
    """This class provides a simple interface for generating top_n vector
    neighborhoods for a given vocabulary sample, using vecto library.
    Vecto-style metadata is also generated."""

    #pylint: disable=too-many-arguments
    def __init__(self, experiment_name=None, extra_metadata=None,
                 overwrite=False, ld_scores="all",
                 output_dir=os.path.join(config["path_to_resources"],
                                         "experiments")):

        super(AnnotateVectorNeighborhoods, self).__init__(
            experiment_name=experiment_name, extra_metadata=extra_metadata, \
            overwrite=overwrite, embeddings=None, output_dir=output_dir,
            dataset=None, experiment_subfolder="neighbors_annotated")


        print(
            "\n\nIf your embeddings are not normalized, retrieving neighbors "
            "will take more time. By default LDT normalizes them on loading. "
            "If you need them not normalized, use normalize=False option.\n")

        self._metadata["task"] = "annotate_neighbors"
        self._metadata["uuid"] = str(uuid.uuid4())
        self._load_dataset(dataset=None)
        neighbors_metadata_path = self.output_dir.replace(
            "neighbors_annotated", "neighbors")
        neighbors_metadata_path = os.path.join(neighbors_metadata_path,
                                               "metadata.json")
        if not os.path.isfile(neighbors_metadata_path):
            raise IOError("The metadata for the neighborhood generation task "
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
                                'NeighborFrequency']

        self.binary_vars = [x for x in self.supported_vars if not \
            x in self.continuous_vars]

        ld_scores_error = "The ld_scores argument is invalid. It should be " \
                          "'all' for all supported relations, or a list with " \
                          "one or more of the following values:\n" + \
                          " ".join(self.supported_vars)

        if ld_scores == "all":
            self._ld_scores = self.supported_vars
        else:
            if isinstance(ld_scores, list):
                unsupported = [x for x in ld_scores if not x in
                                                           self.supported_vars]
                if unsupported:
                    raise ValueError(ld_scores_error)
                else:
                    self._ld_scores = [x for x in self.supported_vars if x
                                       in ld_scores]
            else:
                raise ValueError(ld_scores_error)

        # setting up ldt resources to be used
        normalizer = Normalization(language="English",
                                   order=("wordnet", "custom"),
                                   lowercasing=True)
        derivation = DerivationAnalyzer()
        LexDict = MetaDictionary()

        self.analyzer = RelationsInPair(normalizer=normalizer,
                                        derivation_dict=derivation,
                                        lex_dict=LexDict)

    def _load_dataset(self, dataset):
        """Dataset for generating vector neighborhoods was already processed in
        the previous stage of the experiment, so nothing needs to be done
        here."""
        pass

    def _process(self, embeddings_path):
        filename = get_fname_for_embedding(embeddings_path)
        neighbor_file_path = os.path.join(self.output_dir.replace(
                "neighbors_annotated", "neighbors"), filename)
        df = pd.read_csv(neighbor_file_path, header=0, sep="\t")
        dicts = df.to_dict(orient="records")
        for d in dicts:
            neighbor = d["Neighbor"]
            target = d["Target"]
            # print(target, neighbor)
            relations = self.analyzer.analyze(target, neighbor)
            for i in self.continuous_vars:
                if i in relations:
                    d[i] = relations[i]
            for i in self.binary_vars:
                d[i] = i in relations

        df = pd.DataFrame(dicts, columns=["Target", "Rank", "Neighbor",
                                          "Similarity"]+self._ld_scores)
        print(df.head())
        df.to_csv(os.path.join(self.output_dir, filename), index=False,
                  sep="\t")

        # explicit cache on disk for word function results that would be
        # explicitly reloaded in each subprocess on each step?
        #  each process


def get_fname_for_embedding(embeddings_path):

    """At the moment, filenames are simply directory names for folders that
    contained the initial embeddings. They are assumed to be unique."""

    filename = os.path.split(embeddings_path)[-1]+".tsv"
    return filename


if __name__ == '__main__':
    annotation = AnnotateVectorNeighborhoods(experiment_name="testing",
                                             overwrite=True)
    annotation.get_results()