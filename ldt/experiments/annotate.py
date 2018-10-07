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

Todo:

    * parsing arguments from command line
    * cache saved between sessions
    * ldt resource settings saved to metadata

"""

import os
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
    """This class provides a simple interface for annotating pre-computed top_n
    vector neighborhoods for a given vocabulary sample.
    Vecto-style metadata is also generated."""

    #pylint: disable=too-many-arguments
    def __init__(self, experiment_name=None, extra_metadata=None,
                 overwrite=False, ld_scores="all",
                 output_dir=os.path.join(config["path_to_resources"],
                                         "experiments"),
                 ldt_analyzer=None):

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
            ldt_analyzer: :class:`~ldt.relations.pair.RelationsInPair`
                instance, with lexicographic, morphological and normalization
                resources set up as desired (see tutorial and
                class documentation). If None, default settings for English
                will be used.
            ld_scores (str or list of str): "all" for all supported scores,
                or a list of ld_scores. Supported values are:

                    - "SharedPOS",
                    - "SharedMorphForm",
                    - "SharedDerivation",
                    - "NonCooccurring",
                    - "GDeps",
                    - "TargetFrequency",
                    - "NeighborFrequency",
                    - "Associations",
                    - "ShortestPath",
                    - "Synonyms",
                    - "Antonyms",
                    - "Meronyms",
                    - "Hyponyms",
                    - "Hypernyms",
                    - "OtherRelations",
                    - "Numbers",
                    - "ProperNouns",
                    - "Noise",
                    - "URLs",
                    - "Filenames",
                    - "ForeignWords",
                    - "Hashtags"
                    - 'TargetFrequency',
                    - 'NeighborFrequency'.

        See more details for these scores `here
        <http://ldtoolkit.space/ldscores/>`_.

        Returns:
            (None): the annotated neighbors file will be written to disk
                together with the experiment metadata.

        """

        super(AnnotateVectorNeighborhoods, self).__init__(
            experiment_name=experiment_name, extra_metadata=extra_metadata, \
            overwrite=overwrite, embeddings=None, output_dir=output_dir,
            dataset=None, experiment_subfolder="neighbors_annotated")

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

        self.message = "Starting LD annotation."

        self._metadata["failed_pairs"] = []
        self._metadata["missed_pairs"] = []
        self._metadata["total_pairs"] = 0

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
                          ", ".join(self.supported_vars)

        if ld_scores == "all":
            self._ld_scores = self.supported_vars
        else:
            if isinstance(ld_scores, list):
                unsupported = [x for x in ld_scores if not
                               x in self.supported_vars]
                if unsupported:
                    raise ValueError(ld_scores_error)
                else:
                    self._ld_scores = [x for x in self.supported_vars if x
                                       in ld_scores]
            else:
                raise ValueError(ld_scores_error)

        if ldt_analyzer:
            self.analyzer = ldt_analyzer
        else:
            # setting up default ldt resources to be used
            normalizer = Normalization(language="English",
                                       order=("wordnet", "custom"),
                                       lowercasing=True)
            derivation = DerivationAnalyzer()
            lex_dict = MetaDictionary()

            self.analyzer = RelationsInPair(normalizer=normalizer,
                                            derivation_dict=derivation,
                                            lex_dict=lex_dict)

    def _load_dataset(self, dataset):
        """Dataset for generating vector neighborhoods was already processed in
        the previous stage of the experiment, so nothing needs to be done
        here."""
        pass

    def _process(self, embeddings_path):

        prior_data = collect_prior_data(self.output_dir)

        filename = get_fname_for_embedding(embeddings_path)
        neighbor_file_path = os.path.join(self.output_dir.replace(
            "neighbors_annotated", "neighbors"), filename)
        print("Annotating "+neighbor_file_path)

        input_df = pd.read_csv(neighbor_file_path, header=0, sep="\t")
        self._metadata["total_pairs"] += len(input_df)
        dicts = input_df.to_dict(orient="records")
        for col_dict in dicts:
            neighbor = col_dict["Neighbor"]
            target = col_dict["Target"]
            if target+":"+neighbor in prior_data:
                col_dict.update(prior_data[target+":"+neighbor])
            else:
                relations = self.analyzer.analyze(target, neighbor)
                if not relations:
                    self._metadata["failed_pairs"].append(tuple([target, neighbor]))
                else:
                    if not "Missing" in relations:
                        to_check_continuous = self.continuous_vars
                        to_check_binary = self.binary_vars
                    else:
                        to_check_binary = ["NonCooccurring", "GDeps"]
                        to_check_continuous = ["TargetFrequency",
                                               "NeighborFrequency"]
                        self._metadata["missed_pairs"].append(
                            tuple([target, neighbor]))
                    for i in to_check_continuous:
                        if i in relations:
                            col_dict[i] = relations[i]
                    for i in to_check_binary:
                        col_dict[i] = i in relations

        output_df = pd.DataFrame(dicts,
                                 columns=["Target", "Rank", "Neighbor",
                                          "Similarity"]+self._ld_scores)
        output_df.to_csv(os.path.join(self.output_dir, filename),
                         index=False, sep="\t")

    def _postprocess_metadata(self):
        """Helper method for logging unique failed target:neighbor pairs and
        calculating the overall coverage (considered as number of non-unique
        pairs for which dictionary data was successfully found)."""

        total_fails = self._metadata["failed_pairs"]+self._metadata[
            "missed_pairs"]
        total_fails = list(set(total_fails))
        self._metadata["coverage"] = \
            1 - round(len(total_fails)/self._metadata["total_pairs"], 2)


def collect_prior_data(output_dir):
    """Helper for collecting all the previously processed data (useful in
    case a large experiment is interrupted in the middle, as many word pairs
    repeat across different embeddings).

    Args:
        output_dir (str): the path where the previous results have been saved.

    Returns:
         (dict): a dictionary with previously computed word relations,
         with similarity and rank data removed. The keys are target:neighbor
         pairs.

    """
    processed_files = os.listdir(output_dir)
    if "metadata.json" in processed_files:
        processed_files.remove("metadata.json")
    prior_res = {}
    for f in processed_files:
        input_df = pd.read_csv(os.path.join(output_dir, f), header=0, sep="\t")
        del input_df["Rank"]
        del input_df["Similarity"]
        dicts = input_df.to_dict(orient="records")
        for pair in dicts:
            prior_res[pair["Target"]+":"+pair["Neighbor"]] = pair
    return prior_res



def get_fname_for_embedding(embeddings_path):

    """At the moment, filenames are simply directory names for folders that
    contained the initial embeddings. They are assumed to be unique."""

    filename = os.path.split(embeddings_path)[-1]+".tsv"
    return filename

if __name__ == '__main__':
    annotation = AnnotateVectorNeighborhoods(experiment_name="testing",
                                             overwrite=True)
    annotation.get_results()
