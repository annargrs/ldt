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

from ldt.helpers.exceptions import AuthorizationError

from ldt.dicts.dictionary import Dictionary
from ldt.dicts.semantics.wikisaurus import Wikisaurus
from ldt.dicts.semantics.wiktionary import Wiktionary
from ldt.dicts.semantics.wordnet.en import WordNet
from ldt.dicts.semantics.babelnet import BabelNet

from ldt.load_config import config

class MetaDictionary(Dictionary):
    """Class implementing a collection of dictionaries which are queried in
    the specified oder (either the entire collection or until the first
    match is found).

    Examples:
        >>> meta = ldt.dicts.metadictionary.MetaDictionary(languge="English")
        # each constituent dictionary is accessible as an attribute on the
        # meta-dictionary, with all their functionality:
        >>> meta.wiktionary.is_a_word("cat")
        True
        # or via the _dicts attribute, which contains a dictionary with
        # dictionary types as keys
        >>> meta.wiktionary._dicts["wiktionary"].is_a_word("cat")
        True
        # the list of constituent dictionaries that should be initialized,
        # and the order in which they should be queried are set with order
        # parameter:
        >>> meta = ldt.dicts.metadictionary.MetaDictionary(order=['wordnet',
        'wiktionary', 'wikisaurus'], languge="English")
        >>> meta._order
        ['wordnet', 'wiktionary', 'wikisaurus']
        # this is the order in which the dictionaries should be queried for
        the # minimal-result setting
        >>> meta._is_a_word("cat", minimal=True)
        ["wordnet]
        >>> meta._is_a_word("cat", minimal=False)
        ['wordnet', 'wiktionary', 'wikisaurus']

    """
    def __init__(self, order=("wordnet", "wiktionary", "wikisaurus",
                              "babelnet"),
                 language=config["default_language"],
                 lowercasing=config["lowercasing"],
                 split_mwu=config["split_mwu"],
                 cache=config["wiktionary_cache"],
                 babelnet_key=config["babelnet_key"]):

        self.language = language
        self._dicts = {}
        self._order = []

        for dictionary in order:

            if dictionary == "wiktionary":
                self.wiktionary = Wiktionary(language=language,
                                             lowercasing=lowercasing,
                                             split_mwu=split_mwu,
                                             cache=cache)
                self._dicts[dictionary] = self.wiktionary
                self._order.append(dictionary)
            if dictionary == "wikisaurus":
                self.wikisaurus = Wikisaurus(language=language,
                                             lowercasing=lowercasing,
                                             split_mwu=split_mwu,
                                             cache=cache)
                self._dicts[dictionary] = self.wikisaurus
                self._order.append(dictionary)
            if dictionary == "babelnet":
                try:
                    self.babelnet = BabelNet(language=language,
                                             lowercasing=lowercasing,
                                             split_mwu=split_mwu,
                                             babelnet_key=babelnet_key)
                    self._dicts[dictionary] = self.babelnet
                    self._order.append(dictionary)
                except AuthorizationError:
                    pass
            if dictionary == "wordnet" and language.lower() in ["en", "english"]:
                self.wordnet = WordNet(lowercasing, split_mwu)
                self._dicts[dictionary] = self.wordnet
                self._order.append(dictionary)

        self.supported_relations = ("synonyms", "antonyms", "hyponyms",
                                    "hypernyms", "meronyms", "holonyms",
                                    "troponyms", "coordinate terms", "other")

    def is_a_word(self, word, minimal=True):
        """ Returning the name of the resource containing an entry for the
        queried word (the first in the pre-defined order).

        Examples:
            >>> meta = ldt.dicts.metadictionary.MetaDictionary(cache=False)
            >>> meta.is_a_word("cat")
            ['wordnet']
            >>> meta.is_a_word("cat", minimal=False)
            ['wordnet', 'wiktionary', 'wikisaurus', "babelnet"]

        Args:
            word (str): the word to be looked up.
            minimal (bool): if True, only the first matching dictionary is
            returned

        Returns:
            (list): which resource(s) contains an entry for the queried word,
            if any

        """
        res = []
        for dictionary in self._order:
            if self._dicts[dictionary].is_a_word(word):
                res.append(dictionary)
                if minimal:
                    return res
        if res:
            return res
        return None

    def get_relations(self, word, minimal=False, relations="main"):
        """Combining relations data from all available sources.

        Args:
            word (str): the word to be looked up
            minimal (bool): if True, only the first matching resource will be
                queried
            relations (tuple, string): the relations to look up

        Returns:
            (dict): dictionary with relations as keys and lists of words as
                values

        Todo:

            * component dicts should just ignore relations that they don't have
            * include babelnet relations in supported_relations

        """
        res = {}

        dicts = self.is_a_word(word, minimal)
        for i in dicts:
                relation_dict = self._dicts[i].get_relations(word, relations,
                                                             reduce=True)
                # print(relation_dict)
                for relation in relation_dict:
                    if relation_dict[relation]:
                        if not relation in res:
                            res[relation] = relation_dict[relation]
                        else:
                            res[relation] += relation_dict[relation]
        for relation in res:
            res[relation] = list(set(res[relation]))
            res[relation] = sorted(res[relation])
        return res

    def get_relation(self, word, relation, minimal=False):
        """Wrapper for :meth:`get_relations` for one-relation use.

        Some resources like WordNet have detailed interfaces for different
        relations, while others (including BabelNet and Wiktionary) have
        a single interface for them all. This method can be simply inherited
        for the second type of resources, and overridden in the first type case.

        Args:
            word (str): the word to be looked up
            relation (str): the relation to look up
            minimal (bool): if True, only the first matching resource will be
                queried

        Returns:
            (list): the list of words related to the target word with the
            specified relation
        """

        res = []
        dicts = self.is_a_word(word, minimal)
        for i in dicts:
                if relation in self._dicts[i].supported_relations:
                    res += self._dicts[i].get_relation(word, relation)
        res = list(set(res))
        res = sorted(res)
        return res
