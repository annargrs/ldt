"""This module implements lookup of the minimal path similarity between all
synsets of two words in WordNet.

Examples:

    >>> ldt.relations.ontology_path.en.get_wn_paths("tree", "apple")
    0.05
    >>> ldt.relations.ontology_path.en.get_wn_paths("tree", "cider")
    0.07142857142857142

"""


import timeout_decorator
import functools

from nltk.corpus import wordnet as wn
from ldt.load_config import config


@timeout_decorator.timeout(10, use_signals=False)
@functools.lru_cache(maxsize=config["cache_size"])
def _get_wn_paths(word1, word2):
    """Getting the minimal path similarity between a pair of words in wordnet
    _ontodict.

    Args:
        word1 (str), word2 (str): the words to look up.

    Returns:
        (float): the minimal path found between the two words.

    Note:

        The algorithm changed in v. 0.1.1: the absence of paths between words
        is no longer considered as zero.

    Todo:

        - Experiment with NaNs for missed paths instead of zeros.

    """
    all_sim = []
    for s1 in wn.synsets(word1):
        for s2 in wn.synsets(word2):
            similarity = s1.path_similarity(s2)
            if similarity:
                all_sim.append(similarity)
            # else:
            #     all_sim.append(0)
    if len(all_sim) > 0:
        shortest = min(all_sim)
    else:
        shortest = 0
    return shortest

@functools.lru_cache(maxsize=config["cache_size"])
def get_shortest_path(word1, word2):
    """Wrapper for `:func:_get_wn_paths` that enables the use of timeout
    decorator.

    Todo:

        - Experiment with NaNs for missed paths instead of zeros.

    """
    try:
        return _get_wn_paths(word1, word2)
    except timeout_decorator.timeout_decorator.TimeoutError:
        return 0