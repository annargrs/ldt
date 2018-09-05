# -*- coding: utf-8 -*-
""" This module provides base interface for Wiktionary.

    The current functionality includes:

     - Retrieving Wiktionary Data with WiktionaryParser;
     - Determining whether a word entry exists;
     - Optionally caching the latest list of page titles for determining
       whether pages exist;
     - Automatically formatting the dictionary language argument as required.

    Todo:
        * silent cache loading,
        * silent cache update every 2 weeks
        * sleep option
"""

import functools

from wiktionaryparser import WiktionaryParser

from ldt.helpers.resources import lookup_language as lookup_language
from ldt.helpers.wiktionary_cache import load_wiktionary_cache as \
    load_wiktionary_cache
from ldt.dicts.dictionary import Dictionary as Dictionary
from ldt.load_config import config as config


class BaseWiktionary(Dictionary):
    """The class providing base Wiktionary interface.

    At the moment this class relies on the WiktionaryParser library,
    some  Wiktionary content might be missing.

    It optionally uses a cached list of Wiktionary pages to reduce server
    load and speed  up analysis by only querying pages that actually exist
    for a given language (see :mod:`ldt.helpers.wiktionary_cache`).

    Note:
        The language argument used for Wiktionary cache files and in Wiktionary
        API is in 2-letter-code format, while WiktinaryParser requires a
        `canonical language name
        <https://en.wiktionary.org/wiki/Wiktionary:List_of_languages>`_.
        LDT provides on-the-fly conversion as needed.

    Todo:

        * Alternative parsing for wiktionary xml

    """
    # pylint: disable=unused-argument
    def __init__(self, cache=config["wiktionary_cache"], language=config[
        "default_language"], lowercasing=config["lowercasing"],
                 split_mwu=config["split_mwu"]):
        """ Initializing the Wiktionary class.

        Unlike the basic Dictionary class, Wiktionary checks the language
        argument upon initialization and converts it to the 2-letter code if
        necessary. A None cache is also initialized.

        Args:
            cache (bool): *True* if lists of entries for a given
            language should be cached to speed up queries

        """
        super(BaseWiktionary, self).__init__(language=language,
                                             lowercasing=lowercasing,
                                             split_mwu=split_mwu)
        self.language = language
        if len(self.language) > 2:
            self.language = lookup_language(self.language, reverse=True)
        # self._language = language
        if not cache:
            self.cache = None
        else:
            self.load_cache()
        # self.supported_relations = ("synonyms", "antonyms", "hyponyms",
        #                             "hypernyms", "meronyms", "holonyms",
        #                             "troponyms", "coordinate terms", "other")


    def _set_language(self, language):
        """This method ensures the language arg is a 2-letter code."""
        if len(language) > 2:
            language = lookup_language(language, reverse=True)
        self._language = language

    def load_cache(self):
        """Loading the cached list of titles of existing Wiktionary pages.
        If it doesn't exist, this list is created in the ldt resources directory
        specified in the config file."""

        self.cache = load_wiktionary_cache(language=self._language,
                                           lowercasing=self.lowercasing,
                                           path_to_cache=config[
                                               "path_to_resources"],
                                           wikisaurus=False)

    def is_a_word(self, word):
        """ Determines whether a Wiktionary entry exists for this word.

        If cache has been loaded, it is used to determine whether a word exists.
        Otherwise, Wiktionary is queried.

        Args:
            word (str): the input word to look up.

        Returns:
            (bool): True if the word entry was found.

        """
        if self.cache:
            if word in self.cache:
                return True
            return False
        else:
            if self.query(word):
                return True
            return False

    @functools.lru_cache(maxsize=None)
    def query(self, word):
        """A method to retrieve Wiktionary data online.

        A wrapper for `WiktionaryParser
        <https://www.github.com/Suyash458/WiktionaryParser>`_.

        Args:
            word (str): word to be queried.

        Returns:
            a list of Wiktionary data points

        Todo:
            Find the specific error that is thrown when too many
            requests are made in parallel.
        """

        #convert from language code to canonical name for Wiktionary parser
        language = lookup_language(self._language)

        #set language
        parser = WiktionaryParser()
        parser.set_default_language(language)

        if not self.cache:
            try:
                return parser.fetch(word)
            except:
                print("LDT couldn't reach Wiktionary. Your connection may be "
                      "down or refused by the server.")
                return None

        else:
            if not word in self.cache:
                return None
            else:
                try:
                    return parser.fetch(word)
                except:
                    print("LDT couldn't reach Wiktionary. Your connection may "
                          "be down or refused by the server.")
                    return None
