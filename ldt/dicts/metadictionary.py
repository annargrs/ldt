# -*- coding: utf-8 -*-
"""This module provides functionality for aggregating relations information
from WordNet and Wiktionary.

Adding BabelNet to this mixture does not really make sense, since BabelNet
already combines both of these sources and probably regularly updates
Wiktionary information. This module is intended for cases when using
BabelNet is impractical.

Todo:
    * default caching on, once it's silenced

"""

from ldt.dicts.dictionary import Dictionary as Dictionary
from ldt.dicts.semantics.wikisaurus import Wikisaurus
from ldt.dicts.semantics.wiktionary import Wiktionary
from ldt.dicts.semantics.wordnet.en import WordNet


# from ldt.config import lowercasing as config_lowercasing
# from ldt.config import language as config_language
# from ldt.config import split_mwu as config_split_mwu
# from ldt.config import wiktionary_cache as config_wiktionary_cache
from ldt.load_config import config as config

class MetaDictionary(Dictionary):

    def __init__(self, language=config["default_language"],
                 lowercasing=config["lowercasing"],
                 split_mwu=config["split_mwu"],
                 cache=config["wiktionary_cache"]):
        self.language = language

        self.wiktionary = Wiktionary(language=language,
                                     lowercasing=lowercasing,
                                     split_mwu=split_mwu,
                                     cache=cache)
        self.wikisaurus = Wikisaurus(language=language,
                                     lowercasing=lowercasing,
                                     split_mwu=split_mwu,
                                     cache=cache)
        if language.lower() in ["en", "english"]:
            self.wn = WordNet(lowercasing, split_mwu)
            self._dicts = (self.wn, self.wikisaurus, self.wiktionary)
        else:
            self._dicts = (self.wikisaurus, self.wiktionary)
        self.supported_relations = ("synonyms", "antonyms", "hyponyms",
                                    "hypernyms", "meronyms", "holonyms",
                                    "troponyms", "coordinate terms", "other")

    def is_a_word(self, word):
        """ Determining if a word has an entry in at least one resource.

        Args:
            word (str): the word to be looked up

        Returns:
            (bool): whether the target word has an entry in the resource

        """
        for dictionary in self._dicts:
            if dictionary.is_a_word(word):
                return True

    def get_relations(self, word, relations="main"):
        """Combining relations data from all available sources.

        Args:
            word (str): the word to be looked up
            relations (tuple, string): the relations to look up

        Returns:
            (dict): dictionary with relations as keys and lists of words as
            values

        """
        res = {}

        for dictionary in self._dicts:
            if dictionary.is_a_word(word):
                relation_dict = dictionary.get_relations(word, relations,
                                                         reduce=True)
                # print(relation_dict)
                for relation in relation_dict:
                    if not relation in res:
                        res[relation] = relation_dict[relation]
                    else:
                        res[relation] += relation_dict[relation]
        for relation in res:
            res[relation] = list(set(res[relation]))
            res[relation] = sorted(res[relation])
        return res

    def get_relation(self, word, relation):
        """Wrapper for :meth:`get_relations` for one-relation use.

        Some resources like WordNet have detailed interfaces for different
        relations, while others (including BabelNet and Wiktionary) have
        a single interface for them all. This method can be simply inherited
        for the second type of resources, and overridden in the first type case.

        Args:
            word (str): the word to be looked up
            relation (str): the relation to look up

        Returns:
            (list): the list of words related to the target word with the
            specified relation
        """

        res = []
        for dictionary in self._dicts:
            if dictionary.is_a_word(word):
                if relation in dictionary.supported_relations:
                    res += dictionary.get_relation(word, relation)
        res = list(set(res))
        res = sorted(res)
        return res


# @functools.lru_cache(maxsize=None)
# def get_semantic_relations(word):
#     spellings = list(word.spellings.keys())
#     stems = list(word.stems.keys())
#     sem = {}
#     stem_sem = {}
#     for s in spellings:
#         rels = collect_all_semantic_relations(s)
#         sem.update(rels)
#     for stem in stems:
#         rels = collect_all_semantic_relations(stem)
#         stem_sem.update(rels)
#     #lowercase and set all words in relations
#     for rel in stem_sem:
#         stem_sem[rel] = set(w.lower() for w in stem_sem[rel])
#     for rel in sem:
#         sem[rel] = set(w.lower() for w in sem[rel])
#     word.semantics = sem
#     word.stem_semantics = stem_sem
#     return word