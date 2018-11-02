# -*- coding: utf-8 -*-
"""Annotating vector neighborhoods.

This module provides functionality for annotating vector neighborhoods
obtained from a number of word embeddings.

This is the second (and most important) step in LDT analysis default_workflow. The
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
    * ldt resource settings saved to metadata
    * add progressbars
    * multicore processing

"""
import ldt

import os
import uuid
import pandas as pd
import numpy as np
#import multiprocessing
#import multiprocessing.pool
# from billiard import
from p_tqdm import p_map
#from progressbar.bar import ProgressBar
from pathos.multiprocessing import ProcessingPool
from multiprocessing import Pool
#import multiprocessing.managers as m
from vecto.utils.data import load_json

from ldt.experiments.metadata import Experiment
from ldt.load_config import config
from ldt.dicts.normalize import Normalization
from ldt.dicts.derivation.meta import DerivationAnalyzer
from ldt.dicts.semantics.metadictionary import MetaDictionary
from ldt.relations.pair import RelationsInPair
from ldt.relations.distribution import DistributionDict
from ldt.load_config import config


# class NoDaemonProcess(multiprocessing.Process):
#   def __init__(self, group=None, target=None, name=None, args=(), kwargs={},
#                *, daemon=None):
#     super(NoDaemonProcess, self).__init__(group, target, name, args, kwargs, daemon=daemon)
#     if 'daemon' in multiprocessing.process._current_process._config:
#       del multiprocessing.process._current_process._config['daemon']
#     self._config = multiprocessing.process._current_process._config.copy()
#   # make 'daemon' attribute always return False
#   def _get_daemon(self):
#     return False
#   def _set_daemon(self, value):
#     pass
#   daemon = property(_get_daemon, _set_daemon)
#
# # We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# # because the latter is only a wrapper function, not a proper class.
# class MyPool(multiprocessing.pool.Pool):
#     Process = NoDaemonProcess


class AnnotateVectorNeighborhoods(Experiment):
    """This class provides a simple interface for annotating pre-computed top_n
    vector neighborhoods for a given vocabulary sample.
    Vecto-style metadata is also generated."""

    #pylint: disable=too-many-arguments
    def __init__(self, experiment_name=config["experiments"]["experiment_name"],
                 extra_metadata=None,
                 overwrite=config["experiments"]["overwrite"], ld_scores="main",
                 output_dir=os.path.join(config["path_to_resources"],
                                         "experiments"),
                 ldt_analyzer=None,
                 multiprocessing=config["experiments"]["multiprocessing"],
                 debugging=False):

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

        self.metadata["task"] = "annotate_neighbors"
        self.metadata["uuid"] = str(uuid.uuid4())
        self.metadata["ldt_config"] = config
        self.metadata["output_dir"] = self.output_dir
        self.metadata["debugging"] = debugging
        self.metadata["multiprocessing"] = multiprocessing

        self._load_dataset(dataset=None)
        neighbors_metadata_path = self.output_dir.replace(
            "neighbors_annotated", "neighbors")

        neighbors_metadata_path = os.path.join(neighbors_metadata_path,
                                               "metadata.json")
        if not os.path.isfile(neighbors_metadata_path):
            raise IOError("The metadata for the neighborhood generation task "
                          "was not found at "+neighbors_metadata_path)
        else:
            self.metadata["neighbors_metadata_path"] = neighbors_metadata_path
            neighbors_metadata = load_json(neighbors_metadata_path)
            self.metadata["embeddings"] = neighbors_metadata["embeddings"]
            self.embeddings = []
            for embedding in self.metadata["embeddings"]:
                self.embeddings.append(embedding["path"])

        self.message = "\n\nStarting LD annotation. This will take a while " \
                       "for " \
                       "the first files, but the remainder should go faster, " \
                       "because many neighbor pairs will be the same."

        # self.metadata["failed_pairs"] = []
        self.metadata["missed_pairs"] = []
        self.metadata["total_pairs"] = 0

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
                                'NeighborFrequency']

        corpus_specific = ["NonCooccurring", "TargetFrequency", "NeighborFrequency"]
        if not config["corpus"]:
            for i in [self.supported_vars, self.continuous_vars]:
                i = [x for x in i if not i in corpus_specific]

        self.binary_vars = [x for x in self.supported_vars if not \
            x in self.continuous_vars]

        ld_scores_error = "The ld_scores argument is invalid. It should be " \
                          "'all' for all supported relations, or a list with " \
                          "one or more of the following values:\n" + \
                          ", ".join(self.supported_vars)

        if ld_scores == "all":
            self._ld_scores = self.supported_vars

        elif ld_scores == "main":
            exclude = ["ShortestPath", "URLs", "Filenames", "Hashtags",
                       "Noise"]
            if not config["corpus"]:
                exclude += ["NonCooccurring", "GDeps", "TargetFrequency",
                            "NeighborFrequency"]
            self._ld_scores = [x for x in self.supported_vars if not x in
                                                                     exclude]
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

        self.metadata["ld_scores"] = self._ld_scores
        self.metadata["continuous_vars"] = self.continuous_vars
        self.metadata["binary_vars"] = self.binary_vars

        self.ldt_analyzer = ldt_analyzer

        # global metadata
        # metadata = self.metadata
        #
        # global global_analyzer
        # global_analyzer = ldt_analyzer
        # global_analyzer = init_analyzer(path=neighbors_metadata_path,
        #                                 analyzer=ldt_analyzer)


    def _load_dataset(self, dataset):
        """Dataset for generating vector neighborhoods was already processed in
        the previous stage of the experiment, so nothing needs to be done
        here."""
        pass

    def _process(self, embeddings_path):

        global prior_data
        prior_data = collect_prior_data(self.metadata["output_dir"])
        # print("collected prior data", len(prior_data))

        global metadata
        metadata = self.metadata

        global global_analyzer
        global_analyzer = self.ldt_analyzer

        filename = self.get_fname_for_embedding(embeddings_path)
        neighbor_file_path = os.path.join(self.output_dir.replace(
            "neighbors_annotated", "neighbors"), filename+".tsv")
        print("\nAnnotating "+neighbor_file_path)
        self.metadata["out_path"] = os.path.join(self.output_dir,
                                                 filename+".tsv")

        input_df = pd.read_csv(neighbor_file_path, header=0, sep="\t")
        self.metadata["total_pairs"] += len(input_df)
        dicts = input_df.to_dict(orient="records")

        if metadata["multiprocessing"] == 1:
            print("\nMultiprocessing: 1 core")
            newdicts = []
            for d in dicts:
                newdicts.append(_process_one_dict(d))
                # newdicts.append(self._process_one_dict_meth(d))
                dicts = newdicts
#            dicts = [_process_one_dict(x) for x in dicts]
#             self.save_results(dicts)
        else:
            print("\nMultiprocessing:", metadata["multiprocessing"], "cores")
        #python multiprocessing library
            # pool = Pool(metadata["multiprocessing"], initializer=initializer(global_analyzer))
            # dicts = pool.map(_process_one_dict, dicts)
        # #pathos.multiprocessing

        #     pool = ProcessingPool(nodes=metadata["multiprocessing"])
        #     dicts = pool.map(_process_one_dict, dicts)
        #try with method
            # t_dicts = []
            # for d in dicts:
            #     t_dicts.append((d,))
            pool = ProcessingPool(nodes=metadata["multiprocessing"])
            dicts = pool.map(self._process_one_dict_meth, dicts)

            # dicts = p_map(_process_one_dict, dicts, num_cpus=metadata["multiprocessing"])
            # self.save_results(dicts)
            # pool = MyPool(metadata["multiprocessing"])
            # dicts = pool.map(_process_one_dict, dicts)
            # pool.close()
            # pool.join()

        dicts = self.add_distr_data(dicts)
        self.save_results(dicts, overwrite=True)

    def save_results(self, dicts, overwrite=False):
        output_df = pd.DataFrame(dicts,
                                 columns=["Target", "Rank", "Neighbor",
                                          "Similarity"]+self._ld_scores)
        if not os.path.exists(self.metadata["out_path"]):
            output_df.to_csv(self.metadata["out_path"], index=False,
                             sep="\t", header=True)
        else:
            if not overwrite:
            # existing_df = pd.read_csv(self.metadata["out_path"], header=0, sep="\t")
            # existing_dicts = existing_df.to_dict(orient="records")
            # if not existing_dicts == dicts:
                output_df.to_csv(self.metadata["out_path"], index=False, sep="\t",
                                 mode="a", header=False)
            else:
                output_df.to_csv(self.metadata["out_path"], index=False,
                                 sep="\t", header=True)


    def _postprocess_metadata(self):
        """Helper method for logging unique failed target:neighbor pairs and
        calculating the overall coverage (considered as number of non-unique
        pairs for which dictionary data was successfully found)."""

        del self.metadata["continuous_vars"]
        del self.metadata["binary_vars"]

        # find missing data
        input_df = pd.read_csv(self.metadata["out_path"], header=0,
                               sep="\t")
        dicts = input_df.to_dict(orient="records")
        set_dicts = {}
        for i in dicts:
            set_dicts[i["Target"]+":"+i["Neighbor"]] = i
            if not self._ld_scores[0] in i:
                self.metadata["missed_pairs"].append(i["Target"]+":"+i["Neighbor"])
            else:
                try:
                    if np.isnan(i[self._ld_scores[0]]):
                        self.metadata["missed_pairs"].append(i["Target"] + ":" + i["Neighbor"])
                except TypeError:
                    continue
                try:
                    if pd.isnull(i[self._ld_scores[0]]):
                        self.metadata["missed_pairs"].append(i["Target"] + ":" + i["Neighbor"])
                except TypeError:
                    continue

        self.metadata["coverage"] = \
            1 - round(len(self.metadata["missed_pairs"]) / self.metadata[
                "total_pairs"], 2)

        #order the dataframe in the original order
        res = []
        input_neighbors_df = pd.read_csv(self.metadata["out_path"].replace(
                "neighbors_annotated", "neighbors"), header=0, sep="\t")
        neighbor_dicts = input_neighbors_df.to_dict(orient="records")
        for i in neighbor_dicts:
            k = i["Target"]+":"+i["Neighbor"]
            try:
                res.append(set_dicts[k])
            except KeyError:
                pass
        self.save_results(res, overwrite=True)
        print("\nAnnotation done.")




    def add_distr_data(self, dicts):
        distr_scores = ["NonCooccurring", "GDeps", "TargetFrequency", "NeighborFrequency"]
        scores = [x for x in distr_scores if x in self._ld_scores]
        if not scores:
            return dicts
        print("\nLoading and adding distributional data. This could take a few minutes for a large dataset.")
        gdeps = "GDeps" in self._ld_scores
        cooccurrence = "NonCooccurring" in self._ld_scores
        if gdeps or cooccurrence:
            wordlist = collect_targets_and_neighbors(dicts)
        else:
            wordlist = None
        frequencies = "TargetFrequency" in self._ld_scores or "NeighborFrequency" in self._ld_scores
        distr_dict = DistributionDict(gdeps=gdeps,
                                      cooccurrence=cooccurrence,
                                      wordlist=wordlist,
                                      frequencies=frequencies)
        for d in dicts:
            distr_scores = distr_dict.analyze(target=d["Target"],
                                              neighbor=d["Neighbor"])
            d.update(distr_scores)
        distr_dict = None
        return dicts

    def _process_one_dict_meth(self, col_dict):
        """Helper function that for performing the annotation in a
        multiprocessing-friendly way. Relies on global analyzer, metadata and
        prior_data objects."""
        # col_dict = col_dict[0]
        print(col_dict)
        neighbor = col_dict["Neighbor"]
        target = col_dict["Target"]
    #    print(target + ":" + neighbor in prior_data)
        if target + ":" + neighbor in prior_data:
    #        print("using prior results")
            # print(prior_data[target + ":" + neighbor])
            col_dict.update(prior_data[target + ":" + neighbor])
        else:
            # relations = self.analyzer.analyze(target, neighbor, silent=True,
            #                                   debugging=metadata["debugging"])
            relations = global_analyzer.analyze(target, neighbor,
                                                silent=True, debugging=metadata["debugging"])
            if relations:
                if not "Missing" in relations:
                    to_check_continuous = metadata["continuous_vars"]
                    to_check_binary = metadata["binary_vars"]
                else:
                    to_check_binary = [x for x in ["NonCooccurring", "GDeps"] if
                                       x in metadata["ld_scores"]]
                    to_check_continuous = [x for x in
                                           ["TargetFrequency", "NeighborFrequency"]
                                           if x in metadata["ld_scores"]]
                    metadata["missed_pairs"].append(tuple([target, neighbor]))
                for i in to_check_continuous:
                    if i in relations:
                        col_dict[i] = relations[i]
                for i in to_check_binary:
                    col_dict[i] = i in relations
        print("processed", col_dict)
        save_result(col_dict)
        return col_dict

def collect_targets_and_neighbors(dicts):

    """Collecting all the target and neighbor words produced by the
    neighbor extraction step, which will be used to filter off unneeded
    words in the large distributional resources and save memory."""

    # output_dir = self.output_dir.strip("metadata.json")
    # neighbor_files = os.listdir(self.output_dir)
    # if "metadata.json" in neighbor_files:
    #     neighbor_files.remove("metadata.json")
    # for f in neighbor_files:
    #     input_df = pd.read_csv(os.path.join(output_dir, f), header=0,
    #                            sep="\t")
    #     res += list(input_df["Target"])
    #     res += list(input_df["Neighbor"])
    # self.wordlist = res
    # return set(res)
    res = []
    for d in dicts:
        res.append(d["Target"])
        res.append(d["Neighbor"])
    res = set(res)
    return res



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
    print("\nCollecting prior data in", output_dir)
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

def init_analyzer(path, analyzer=None):

    """Helper for initializing the RelationsInPair instance if one is not
    provided, and updating it with the wordlist if one is provided"""

    wordlist = collect_targets_and_neighbors(path)
    print("\nLoading filtered distributional resources. This takes a while "
          "for a large experiment.")

    if analyzer:
        # todo move this to RelationsInPair
        if "GDeps" in metadata["ld_scores"] and config["corpus"]:
            analyzer._distr_dict._reload_resource(resource="gdeps",
                                                      wordlist=wordlist)
            analyzer._gdeps = True
        if "NonCooccurring" in metadata["ld_scores"] and config["corpus"]:
            analyzer._distr_dict._reload_resource(resource="cooccurrence",
                wordlist=wordlist)
            analyzer._cooccurrence = True

        return analyzer
    else:
        # setting up default ldt resources to be used
        normalizer = Normalization(language="English",
                                   order=("wordnet", "custom"),
                                   lowercasing=True)
        derivation = DerivationAnalyzer()
        lex_dict = MetaDictionary()

        analyzer = RelationsInPair(normalizer=normalizer,
                                   derivation_dict=derivation,
                                   lex_dict=lex_dict,
                                   gdeps="GDeps" in metadata["ld_scores"],
                                   cooccurrence="NonCooccurring" in metadata["ld_scores"],
                                   wordlist=wordlist)
        return analyzer

class initializer():
    def __init__(self, global_analyzer):
        self.analyzer = global_analyzer

    def __call__(self):
        global global_analyzer
        global_analyzer = self.analyzer

def _process_one_dict(col_dict):
    """Helper function that for performing the annotation in a
    multiprocessing-friendly way. Relies on global analyzer, metadata and
    prior_data objects."""
    neighbor = col_dict["Neighbor"]
    target = col_dict["Target"]
#    print(target + ":" + neighbor in prior_data)
    if target + ":" + neighbor in prior_data:
#        print("using prior results")
        # print(prior_data[target + ":" + neighbor])
        col_dict.update(prior_data[target + ":" + neighbor])
    else:
        relations = global_analyzer.analyze(target, neighbor, silent=True,
                                            debugging=metadata["debugging"])
        if relations:
            if not "Missing" in relations:
                to_check_continuous = metadata["continuous_vars"]
                to_check_binary = metadata["binary_vars"]
            else:
                to_check_binary = [x for x in ["NonCooccurring", "GDeps"] if
                                   x in metadata["ld_scores"]]
                to_check_continuous = [x for x in
                                       ["TargetFrequency", "NeighborFrequency"]
                                       if x in metadata["ld_scores"]]
                metadata["missed_pairs"].append(tuple([target, neighbor]))
            for i in to_check_continuous:
                if i in relations:
                    col_dict[i] = relations[i]
            for i in to_check_binary:
                col_dict[i] = i in relations
    save_result(col_dict)
    return col_dict

def save_result(dicts, overwrite=False):
    if isinstance(dicts, dict):
        dicts = [dicts]
    output_df = pd.DataFrame(dicts,
                             columns=["Target", "Rank", "Neighbor",
                                      "Similarity"]+metadata["ld_scores"])
    if not os.path.exists(metadata["out_path"]):
        output_df.to_csv(metadata["out_path"], index=False,
                         sep="\t", header=True)
    else:
        if not overwrite:
            output_df.to_csv(metadata["out_path"], index=False, sep="\t",
                             mode="a", header=False)
        else:
            output_df.to_csv(metadata["out_path"], index=False,
                             sep="\t", header=True)


if __name__ == '__main__':
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
    annotation = AnnotateVectorNeighborhoods(experiment_name="testing",
                                             overwrite=True,
                                             ldt_analyzer=analyzer,
                                             ld_scores="all",
                                             multiprocessing=4, debugging=True)
    annotation.get_results()


