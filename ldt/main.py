"""Welcome to ldt.

This is the entry point of the ldt application.
"""

import argparse

import ldt.utils.config as config_utils

from ldt.dicts.derivation.meta import DerivationAnalyzer
from ldt.experiments import LDScoring
from ldt.experiments.neighbors import AnnotateVectorNeighborhoods
from ldt.experiments.neighbors import VectorNeighborhoods
from ldt.dicts.normalize import Normalization
from ldt.relations.pair import RelationsInPair
from ldt.dicts.semantics.metadictionary import MetaDictionary


def _experiment(args):
    config = config_utils.load(args.config)
    #  getting vector neighborhoods
    neighborhoods = VectorNeighborhoods(
        experiment_name=config['experiments']['experiment_name'],
        overwrite=config['experiments']['overwrite'],
        top_n=config['experiments']['top_n'])
    neighborhoods.get_results()

    #  setting up ldt resources for annotation with default settings: English,
    # custom derivational analysis, no BabelNet
    normalizer = Normalization(language='English', order=('wordnet', 'custom'),
                               lowercasing=True)
    derivation = DerivationAnalyzer(language='English')
    lex_dict = MetaDictionary(
        language='English', order=('wordnet', 'wiktionary'))

    analyzer = RelationsInPair(normalizer=normalizer,
                               derivation_dict=derivation, lex_dict=lex_dict)

    # performing annotation
    annotation = AnnotateVectorNeighborhoods(
        experiment_name=config['experiments']['experiment_name'],
        overwrite=config['experiments']['overwrite'],
        ld_scores='main', debugging=True, ldt_analyzer=analyzer)
    annotation.get_results()

    # analysing the results
    scoring = LDScoring(
        experiment_name=config['experiments']['experiment_name'],
        overwrite=config['experiments']['overwrite'], ld_scores='main')
    scoring.get_results()


def main():
    """Launch the ldt application."""
    parser = argparse.ArgumentParser(prog='ldt')
    subparsers = parser.add_subparsers()
    parser_xp = subparsers.add_parser(
        'experiment', formatter_class=argparse.RawTextHelpFormatter,
        help='Run experiments according to the setup specified in the input '
             'YAML config file')
    parser_xp.set_defaults(func=_experiment)
    parser_xp.add_argument('--with', dest='config',
                           help='A YAML config file to specify the '
                                'experimental setup')
    args = parser.parse_args()
    args.func(args)
