
"""Full LDT default_workflow.

This module provides full ldt analysis default_workflow with default
resources for English, with one-button-press.

The output is saved in the experiments/analysis/your_experiment_name
subfolder of the ldt resource folder specified in the configuration file.
These are tab-separated data files with columns that contain ld
scores, as described `here <http://ldtoolkit.space/ldscores/>`_.

These scores are the basic profile of the information captured by a given
word embedding. They can be used for evaluation, error analysis, parameter
tuning and hypothesis-driven model development, as described `here
<http://ldtoolkit.space/analysis/examples/>`_.

"""

import sys
import os
import ruamel.yaml as yaml

import ldt
from ldt.load_config import config
import ruamel.yaml as yaml

def default_workflow(experiment_name=
                     config["experiments"]["experiment_name"],
                     overwrite=config["experiments"]["overwrite"],
                     top_n=config["experiments"]["top_n"]):
    """Full LDT default_workflow for English, with most LDT resources used for
    analysis of relations (except BabelNet). Modify this script as needed.
    Descriptions of available settings for all resources are available in
    their respective documentation."""

    #getting vector neighborhoods
    neighborhoods = ldt.experiments.VectorNeighborhoods(
        experiment_name=experiment_name, overwrite=False, top_n=top_n)
    neighborhoods.get_results()

    #setting up ldt resources for annotation with default settings: English,
    # custom derivational analysis, no BabelNet
    normalizer = ldt.dicts.normalize.Normalization(language="English",
                                                   order=("wordnet", "custom"),
                                                   lowercasing=True)
    derivation = ldt.dicts.derivation.meta.DerivationAnalyzer(language="English")
    lex_dict = ldt.dicts.semantics.metadictionary.MetaDictionary(
        language="English", order=("wordnet", "wiktionary"))

    analyzer = ldt.relations.pair.RelationsInPair(normalizer=normalizer,
                                                  derivation_dict=derivation,
                                                  lex_dict=lex_dict,
                                                  gdeps=True,
                                                  cooccurrence=True)

    # performing annotation
    annotation = ldt.experiments.AnnotateVectorNeighborhoods(
        experiment_name=experiment_name, overwrite=overwrite,
        ldt_analyzer=analyzer)
    annotation.get_results()

    # analysing the results
    scoring = ldt.experiments.LDScoring(experiment_name=experiment_name,
                                        overwrite=overwrite)
    scoring.get_results()
