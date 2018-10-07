
"""Full LDT workflow.

This module provides full ldt analysis workflow with default
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
import ldt

from ldt.experiments.metadata import Experiment
from ldt.experiments.neighbors import VectorNeighborhoods
from ldt.experiments.annotate import AnnotateVectorNeighborhoods
from ldt.experiments.analyze import LDScoring

from ldt.dicts.normalize import Normalization
from ldt.dicts.derivation.meta import DerivationAnalyzer
from ldt.dicts.semantics.metadictionary import MetaDictionary
from ldt.relations.pair import RelationsInPair

from ldt.load_config import config

def default_workflow(experiment_name=config["experiments"]["experiment_name"],
                     overwrite=config["experiments"]["overwrite"],
                     top_n=config["experiments"]["top_n"]):

    #getting vector neighborhoods
    neighborhoods = ldt.experiments.VectorNeighborhoods(
        experiment_name=experiment_name, overwrite=overwrite, top_n=top_n)
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
        derivation_dict=derivation, lex_dict=lex_dict)

    # performing annotation
    annotation = ldt.experiments.AnnotateVectorNeighborhoods(
        experiment_name=experiment_name, overwrite=overwrite,
        ldt_analyzer=analyzer)
    annotation.get_results()

    # analysing the results
    scoring = ldt.experiments.LDScoring(experiment_name=experiment_name,
                                        overwrite=overwrite)
    scoring.get_results()


if __name__ == "__main__":
    default_workflow()