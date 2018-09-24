# -*- coding: utf-8 -*-
"""This module provides functionality for detecting relations in a pair of
words.

Examples:
    >>> test_dict = ldt.relations.RelationsInPair()
    >>> test_dict.analyze("black", "white")
    ['SharedPOS', 'SharedMorphForm', 'Antonyms']
    >>> test_dict.analyze("happy", "happily")
    ['Synonyms', 'SharedMorphForm', 'SharedDerivation']


Todo:
   - morph form detection (cat, cats)

"""

import functools

from ldt.dicts.dictionary import Dictionary as Dictionary
from ldt.dicts.normalize import Normalization as Normalizer
from ldt.dicts.derivation.meta import DerivationAnalyzer as \
    DerivationAnalyzer
from ldt.dicts.semantics.metadictionary import MetaDictionary as MetaDictionary
from ldt.relations.word import Word as Word
from ldt.relations.ontology_path.ontodict import OntoDict as OntoDict
from ldt.load_config import config as config
from ldt.dicts.resources import AssociationDictionary as AssociationDictionary
from ldt.relations.distribution import DistributionDict as DistributionDict

class RelationsInPair(Dictionary):
    """This class implements analyzer for all possible relation types in a word
    pair."""
    def __init__(self, language=config["default_language"],
                 lowercasing=config["lowercasing"],
                 derivation_dict=None, normalizer=None,
                 lex_dict=None, distr_dict=None, gdeps=False,
                 cooccurrence=False):

        super(RelationsInPair, self).__init__(language=language,
                                              lowercasing=lowercasing)

        self.OntoDict = OntoDict(language=language)
        self.AssociationDictionary = AssociationDictionary(language=language)

        if not normalizer:
            self._normalizer = Normalizer(language=self.language,
                                          order=("wordnet", "custom"),
                                          lowercasing=True)
        else:
            self._normalizer = normalizer


        if not derivation_dict:
            self._derivation_dict = DerivationAnalyzer()
        else:
            self._derivation_dict = derivation_dict


        if not lex_dict:
            self._lex_dict = MetaDictionary()
        else:
            self._lex_dict = lex_dict

        if not distr_dict:
            self._distr_dict = DistributionDict(language=language,
                                                gdeps=gdeps,
                                                cooccurrence=cooccurrence)

    def is_a_word(self, word):
        raise NotImplementedError

    @functools.lru_cache(maxsize=None)
    def analyze(self, target, neighbor, silent=True):
        """The main function for analyzing the input strings and identifying
        any relations the two words may share.

        Args:
            target (str): the target word to analyze.
            neighbor (str): the neighbor word to analyze:
            silent (bool): if False, the information retrieved for both words
                is printed for reference.

        Returns:
              (list of str): what the two words have in common.
        """

        target = Word(target, self._derivation_dict, self._normalizer,
                      self._lex_dict)
        neighbor = Word(neighbor, self._derivation_dict, self._normalizer,
                        self._lex_dict)
        if not silent:
            print(target.pp_info())
            print(neighbor.pp_info())
        rels = _binary_rels(target, neighbor)
        res = {}
        for rel in rels:
            res[rel] = True
        shortest_path = self.OntoDict.get_shortest_path(target.info[
                                                       "OriginalForm"],
                                                   neighbor.info[
                                                       "OriginalForm"])
        res["ShortestPath"] = shortest_path
        if self.AssociationDictionary.are_related(target.info["OriginalForm"],
                                                  neighbor.info["OriginalForm"]):
            res["Associations"] = True
        if not self._distr_dict.cooccur_in_corpus(target.info[
                                                      "OriginalForm"],
                                                  neighbor.info["OriginalForm"]):
            res["NonCooccurring"] = True
        if self._distr_dict.cooccur_in_gdeps(target.info["OriginalForm"],
                                             neighbor.info["OriginalForm"]):
            res["GDeps"] = True
        res["TargetFrequency"] = self._distr_dict.frequency_in_corpus(
            target.info["OriginalForm"])
        res["NeighborFrequency"] = self._distr_dict.frequency_in_corpus(
            neighbor.info["OriginalForm"])
        return res

def _binary_rels(target, neighbor):
    """Helper function for identifying intersections in the property lists
    of the target and neighbor word.

    Args:
        target (ldt Word object): the object holding the data for the
            target word.
        neighbor (ldt Word object): the object holding the data for the
            neighbor word.

    Returns:
          (list of str): what the two words have in common.
    """
    res = []
    for wordclass in ["Numbers", "ProperNouns", "Noise", "URLs",
                      "Filenames", "ForeignWords", "Hashtags"]:
        if target.info[wordclass] == neighbor.info[wordclass] == True:
            res.append(wordclass)
    if target.info["POS"].intersection(neighbor.info["POS"]):
        res.append("SharedPOS")
    if target.info["IsLemma"] == neighbor.info["IsLemma"] == True:
        res.append("SharedMorphForm")
    for pattern in ["Stems", "Prefixes", "Suffixes", "OtherDerivation"]:
        if pattern in target.info and pattern in neighbor.info:
            if target.info[pattern].intersection(neighbor.info[pattern]):
                res.append("SharedDerivation")
    shared_lex = are_related_as(target, neighbor)
    res += shared_lex
    return list(set(res))


def are_related_as(target, neighbor):
    """Helper function for identifying matches in lexicgraphic relations.

    All relations except hyponymy and hypernymy are treated as symmetrical;
    hyponymy and hypernymy are identified in the target:neighbor direction.

    Args:
        target: the ldt word object for the target word.
        neighbor: the ldt word object for the neighbor word.

    Returns:
        (list of str): the lexicographic relations that the two words are
        related as.

    Todo:

        * antonymy by derivation
    """

    res = []
    for rel in ["Hyponyms", "Hypernyms"]:
        if rel in target.info:
            for word in [neighbor.info["OriginalForm"]] + list(neighbor.info["Lemmas"]) + list(neighbor.info["Stems"]):
                if word in target.info[rel]:
                    res.append(rel)

    rels = ["Synonyms", "Antonyms", "Meronyms", "OtherRelations"]
    for rel in rels:
        if rel in neighbor.info and rel in target.info:
            for word in [target.info["OriginalForm"]] + list(target.info["Lemmas"]) + list(target.info["Stems"]):
                if word in target.info[rel]:
                    res.append(rel)
        if rel not in res:
            if rel in neighbor.info and rel in target.info:
                for word in [target.info["OriginalForm"]] + list(target.info["Lemmas"]) + list(target.info["Stems"]):
                    if word in neighbor.info[rel]:
                        res.append(rel)
    return list(set(res))

