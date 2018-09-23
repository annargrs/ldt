# -*- coding: utf-8 -*-
"""The base metadictionary class identifies resources which have an entry
for the queried word, implementing optional lookup hierarchy. BabelNet
comprises both WordNet and Wiktionary and could just be used on its own,
but usage limits can make that impractical. Moreover, lookups in local NLTK
data are faster and cover a lot of the most frequent words.

Examples:
        # the list of constituent dictionaries that should be initialized,
        # and the order in which they should be queried are set with order
        # parameter:
        >>> meta = ldt.dicts.morphology.meta.MetaDictionary(order=['wordnet',
        'wiktionary', 'babelnet'], languge="English")
        >>> meta._order
        ['wordnet', 'wiktionary', 'babelnet']
        # this is the order in which the dictionaries should be queried for
        the # minimal-result setting
        >>> meta._is_a_word("cat", minimal=True)
        ["wordnet]
        >>> meta._is_a_word("cat", minimal=False)
        ['wordnet', 'wiktionary', 'babelnet']

TODO:

 * init imports of all dicts classes to the dicts init

"""

import functools

from ldt.helpers.exceptions import AuthorizationError

from ldt.dicts.dictionary import Dictionary as Dictionary
from ldt.dicts.morphology.wiktionary import MorphWiktionary
from ldt.dicts.morphology.wordnet.en import MorphWordNet
from ldt.dicts.morphology.babelnet import MorphBabelNet
from ldt.dicts.morphology.custom.en import MorphCustomDict
from ldt.load_config import config as config

class MorphMetaDict(Dictionary):
    """Class implementing a collection of dictionaries which are queried in
    the specified oder (either the entire collection or until the first
    match is found).

    Examples:
        >>> meta = ldt.dicts.morphology.meta.MorphMetaDict(languge="English")
        # each constituent dictionary is accessible as an attribute on the
        # meta-dictionary, with all their functionality:
        >>> meta.wiktionary.is_a_word("cat")
        True
        # or via the _dicts attribute, which contains a dictionary with
        # dictionary types as keys
        >>> meta.wiktionary._dicts["wiktionary"].is_a_word("cat")
        True

    """
    def __init__(self, order=("wordnet", "wiktionary", "babelnet"),
                 language=config["default_language"],
                 lowercasing=config["lowercasing"],
                 cache=config["wiktionary_cache"],
                 babelnet_key=config["babelnet_key"], custom_base="wiktionary"):

        super(MorphMetaDict, self).__init__(language=language,
                                            lowercasing=lowercasing)

        self.language = language
        self._dicts = {}
        self._order = []

        for dictionary in order:

            if dictionary == "wiktionary":
                self.wiktionary = MorphWiktionary(language=self.language,
                                                 lowercasing=False,
                                                 cache=cache)
                self._dicts[dictionary] = self.wiktionary
                self._order.append(dictionary)
            if dictionary == "babelnet":
                try:
                    self.babelnet = MorphBabelNet(language=self.language,
                                                 lowercasing=False,
                                                 babelnet_key=babelnet_key)
                    self._dicts[dictionary] = self.babelnet
                    self._order.append(dictionary)
                except AuthorizationError:
                    pass
            if dictionary == "wordnet" and language.lower() in ["en", "english"]:
                self.wordnet = MorphWordNet()
                self._dicts[dictionary] = self.wordnet
                self._order.append(dictionary)

        if language.lower() in ["en", "english"] and custom_base in self._dicts:
            self.custom = MorphCustomDict(dictionary=self._dicts[custom_base])
            self._dicts[dictionary] = self.custom
            self._order.append(dictionary)

    @functools.lru_cache(maxsize=None)
    def is_a_word(self, word, minimal=True):
        """ Returning the name of the resource containing an entry for the
        queried word (the first in the pre-defined order).

        Examples:
            >>> meta = ldt.dicts.base.meta.BaseMetaDictionary()
            >>> meta.is_a_word("cat")
            ['wordnet']
            >>> meta.is_a_word("cat", minimal=False)
            ['wordnet', 'wiktionary', "babelnet"]

        Args:
            word (str): the word look up.
            minimal (bool): if True, only the results from the first matching
              dictionary are returned.

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

    @functools.lru_cache(maxsize=None)
    def get_pos(self, word, minimal=True):
        """Getting the possible POSes for the word.

        Examples:
            >>> meta = ldt.dicts.base.meta.BaseMetaDictionary(order=("wordnet", "custom",))
            >>> meta.wordnet.is_a_word(("poshest"))
            >>> meta.get_pos("poshest")
            ['adjective']


        Args:
            word (str): the word look up.
            minimal (bool): if True, only the results from the first matching
              dictionary are returned.

        Returns:
            (list): which resource(s) contains an entry for the queried word,
            if any

        """
        res = []
        dicts = self.is_a_word(word, minimal)
        if dicts:
            if not minimal:
                for dictionary in dicts:
                    candidates = self._dicts[dictionary].get_pos(word, formatting="list")
                    if candidates:
                        res += candidates
            else:
                res = self._dicts[dicts[0]].get_pos(word, formatting="list")
        if res:
            return list(set(res))
        return None

    @functools.lru_cache(maxsize=None)
    def lemmatize(self, word):
        """Returns a list of lemmas of the target word.

        Args:
            word (str): the word to look up

        Returns:
            (list): lemmas of the word
        """
        res = []

        if "wordnet" in self._dicts:
            wordnet = self._dicts["wordnet"].lemmatize(word)
            if wordnet:
                return wordnet
        if hasattr(self, "custom"):
            res = self.custom.lemmatize(word)
            if res:
                return res
        return None