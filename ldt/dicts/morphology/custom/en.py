# -*- coding: utf-8 -*-
""" This module provides interface for the extra lemmatization routines in LDT.

    The current functionality includes:

     - Simple rule-based lemmatization for words with inflections *-s, -ed,
       -ing, -er, -est*.

    Todo:
        * more rules for -ed & -ing

"""

import inflect

from ldt.dicts.morphology.morph_dictionary import MorphDictionary as \
    MorphDictionary
from ldt.dicts.base.custom.en import BaseCustomDict as BaseCustomDict
from ldt.load_config import config as config


class MorphCustomDict(MorphDictionary, BaseCustomDict):
    """This class implements an interface for retrievning POS
    information from NLTK WordNet and lemmatization."""

    def __init__(self, language=config["default_language"]):
        """ Initializing the base class.

        Args:
            language (str): the language of the dictionary (only
            English currently supported)

        """

        super(MorphCustomDict, self).__init__(language=language)

    def get_form(self, word):
        pass

    #pylint: disable=arguments-differ
    def lemmatize(self, word, dictionary):
        """ A crude fallback for (frequent) cases where WordNet lemmatizer fails

        Args:
            word (str): the word to uninflect
            dictionary (BaseDictionary subclass): the dictionary in which the
            presence or absence of a word entry should be checked

        Note:
            skipping on some of the finer rules like "ie -> y", assuming that
            most such cases will be handled by WordNet and not make it to
            this method.

        Returns:
            (list): possible lemmas

        """
        res = []
        if word.endswith("er"):
            if dictionary.is_a_word(word[:-2]):
                res.append(word[:-2])
        elif word.endswith("est"):
            if dictionary.is_a_word(word[:-3]):
                res.append(word[:-3])
        elif word.endswith("s"):
            inflect_engine = inflect.engine()
            attempt = inflect_engine.singular_noun(word)
            if attempt:
                res.append(attempt)

        if word.endswith("ing"):
            res = _ing(word, dictionary)

        if word.endswith("ed"):
            res = _ed(word, dictionary)

        return res

    def get_pos(self, word, formatting="dict"):
        pass

def _ing(word, dictionary):
    """Helper for :meth:`lemmatize`, simple rules for -ing ending"""
    res = []
    attempt = word[:-3]
    if dictionary.is_a_word(attempt):
        res.append(attempt)
    elif word[:-3][-1] == word[:-3][-2] and dictionary.is_a_word(
            word[:-4]):
        res.append(word[:-4])
    elif dictionary.is_a_word(attempt+"e"):
        res.append(attempt+"e")
    return res

def _ed(word, dictionary):
    """Helper for :meth:`lemmatize`, simple rules for -ed ending"""
    res = []
    if dictionary.is_a_word(word[:-2]):
        res.append(word[:-2])
    elif word.endswith("ied") and dictionary.is_a_word(word[:-3] + "y"):
        res.append(word[:-3] + "y")
    elif word[:-2][-1] == word[:-2][-2] and dictionary.is_a_word(word[:-3]):
        res.append(word[:-3])
    elif dictionary.is_a_word(word[:-1]):
        res.append(word[:-1])
    return res
