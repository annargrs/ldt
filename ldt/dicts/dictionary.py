# -*- coding: utf-8 -*-
""" Dictionary class

This module creates the base ldt dictionary class that is inherited by
classes for individual resources. It stores the global variables that are
either set by the user or read from the config.py file in the user's home
directory.

Basic functionality required in any subclass:

    * checking if the queried word has an entry in the resource;
    * retrieve the list of word with the specified relation;
    * retrieve a dictionary with specified relations as values and lists of
      related words as values

Todo:
    * creation of default config file upon installation
    * the right error path in NLTK tokenizer
    * add .citation property, and print it out on initialization
        WordNet 1.5, NLTK implementation. Use .citation to get the full
        citation for this resource.
"""

import abc
#from abc import ABCMeta, abstractmethod
from nltk.tokenize import word_tokenize

#from ldt.config import path_to_resources, lowercasing, language, split_mwu
from ldt.helpers.exceptions import DictError as DictError
from ldt.helpers.resources import load_stopwords as load_stopwords
from ldt.helpers.resources import lookup_language_by_code as lookup_language
from ldt.helpers.formatting import get_spacing_variants as get_spacing_variants
from ldt.helpers.formatting import remove_text_inside_brackets as \
    remove_text_inside_brackets
#from ldt.config import path_to_resources as config_path_to_resources
# from ldt.config import lowercasing as config_lowercasing
# from ldt.config import language as config_language
# from ldt.config import split_mwu as config_split_mwu
from ldt.load_config import config as config

class Dictionary(metaclass=abc.ABCMeta):
    """The base LDT dictionary class.

    It stores the global variables that are used by all LDT dictionary
    classes. These variables can be set individually at any point in work. If
    none are provided, the default values from ldt config file are used.

    Note:
        Any future resources extending LDT should inherit from this class.

    """

    def __init__(self, language=config["default_language"],
                 lowercasing=config["lowercasing"],
                 split_mwu=config["split_mwu"]):
        """ Initializing the generic dictionary class

        Args:
            language (str): the language of the dictionary
            lowercasing (bool): True if all data should be lowercased
            split_mwu (bool): True if in addition to underscored spellings of
                multi-word-expressions their dashed and spaced versions should
                also be produced (e.g. 'good night', 'good_night', "good-night")
            main_relations (tuple): the relations that are currently defined
                in all LDT resources

        """

        self._language = language
        self.lowercasing = lowercasing
        self.split_mwu = split_mwu

    @property
    def language(self):
        """Gets or sets the language of the current dictionary. Depending on
        the dictionary, this may involve additional processing."""
        return self._get_language()

    @language.setter
    def language(self, language):
        return self._set_language(language)

    def _get_language(self):
        return self._language

    def _set_language(self, language):
        self._language = language

    def _lowercase(self, word):
        if self.lowercasing:
            return word.lower()
        return word

    @abc.abstractmethod
    def is_a_word(self, word):
        """Stub for the compulsory method for all subclasses that
        determines the existence of an entry.

        Args:
            word (str): the word to be looked up

        Returns:
            (bool): whether the target word has an entry in the resource
        """

        pass