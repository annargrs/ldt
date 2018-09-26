# -*- coding: utf-8 -*-
""" This module provides interface for the extra lemmatization routines in LDT.

    The current functionality includes:

     - Simple rule-based lemmatization for words with inflections *-s, -ed,
       -ing, -er, -est*.

    Todo:
        * more rules for -ed & -ing

"""

import inflect
import functools

from ldt.dicts.morphology.morph_dictionary import MorphDictionary
from ldt.dicts.base.custom.en import BaseCustomDict
from ldt.dicts.base.wordnet.en import BaseWordNet
from ldt.load_config import config


class MorphCustomDict(MorphDictionary, BaseCustomDict):
    """This class implements an interface for retrievning POS
    information from NLTK WordNet and lemmatization."""

    def __init__(self, language=config["default_language"], dictionary=None):
        """ Initializing the base class.

        Args:
            language (str): the language of the dictionary (only
              English currently supported)
            dictionary (BaseDictionary subclass): the dictionary in which the
              presence or absence of a word entry should be checked

        """

        super(MorphCustomDict, self).__init__(language=language)
        if dictionary:
            self.dictionary=dictionary
        else:
            fallback = BaseWordNet()
            self.dictionary = fallback

    def get_form(self, word):
        pass

    @functools.lru_cache(maxsize=config["cache_size"])
    def is_a_word(self, word):
        if self._lemmatize(word):
            return True
        return False

    @functools.lru_cache(maxsize=config["cache_size"])
    def _lemmatize(self, word):
        """ A crude rule-based fallback for (frequent) cases where WordNet
        lemmatizer fails.

        Args:
            word (str): the word to uninflect

        Note:

            * currently skipping on some of the finer rules like "ie -> y",
              assuming that most such cases will be handled by WordNet and not
              make it to this method.
            * for "s" and "ing" endings simply assumes that these words can
              be both nouns and verbs.

        Returns:
            (dict): possible lemmas listed for each possible part of speech

        """
        res = {}
        if word.endswith("er"):
            if self.dictionary.is_a_word(word[:-2]):
                res["adjective"] = [word[:-2]]
        elif word.endswith("'s"):
            if self.dictionary.is_a_word(word[:-2]):
                res["noun"] = [word[:-2]]
        elif word.endswith("es"):
            if self.dictionary.is_a_word(word[:-2]):
                res["noun"] = [word[:-2]]
                res["verb"] = [word[:-2]]
        elif word.endswith("est"):
            if self.dictionary.is_a_word(word[:-3]):
                res["adjective"] = [word[:-3]]
        elif word.endswith("s"):
            inflect_engine = inflect.engine()
            attempt = inflect_engine.singular_noun(word)
            if self.dictionary.is_a_word(attempt):
                res["noun"] = [attempt]
                res["verb"] = [attempt]

        if word.endswith("ing"):
            attempt = self._ing(word)
            if attempt:
                res["noun"] = attempt
                res["verb"] = attempt

        if word.endswith("ed"):
            attempt = self._ed(word)
            if attempt:
                res["verb"] = attempt
        if not res:
            return None
        return res

    def get_pos(self, word, minimal=True, formatting="list"):
        """ A crude rule-based fallback for (frequent) cases where WordNet
        lemmatizer fails. Returns lists of possible POSes.

        Args:
            word (str): the word to uninflect
            dictionary (BaseDictionary subclass): the dictionary in which the
            presence or absence of a word entry should be checked

        Note:

            * for "s" and "ing" endings simply assumes that these words can
              be both nouns and verbs.

        Returns:
            (list): possible POSes for the target word.

        """
        if formatting != "list":
            return None
        res = list(self._lemmatize(word).keys())
        if len(res) == 1:
            return res
        else:
            return list(set(res))

    def lemmatize(self, word):
        """ A crude rule-based fallback for (frequent) cases where WordNet
        lemmatizer fails. Returns lists of possible lemmas.

        Args:
            word (str): the word to uninflect
            dictionary (BaseDictionary subclass): the dictionary in which the
            presence or absence of a word entry should be checked

        Returns:
            (list): possible lemmas for the target word.

        """
        candidate_dict = self._lemmatize(word)
        res = []
        for k, v in candidate_dict.items():
            res += v
        res = list(set(res))
        if len(res) == 1:
            return res
        else:
            return list(set(res))

    def _ing(self, word):
        """Helper for :meth:`lemmatize`, simple rules for -ing ending"""
        res = []
        attempt = word[:-3]
        if self.dictionary.is_a_word(attempt):
            res.append(attempt)
        elif word[:-3][-1] == word[:-3][-2] and self.dictionary.is_a_word(
                word[:-4]):
            res.append(word[:-4])
        elif self.dictionary.is_a_word(attempt+"e"):
            res.append(attempt+"e")
        return res

    def _ed(self, word):
        """Helper for :meth:`lemmatize`, simple rules for -ed ending"""
        res = []
        if self.dictionary.is_a_word(word[:-2]):
            res.append(word[:-2])
        elif word.endswith("ied") and self.dictionary.is_a_word(word[:-3] + "y"):
            res.append(word[:-3] + "y")
        elif word[:-2][-1] == word[:-2][-2] and self.dictionary.is_a_word(word[
                                                                      :-3]):
            res.append(word[:-3])
        elif self.dictionary.is_a_word(word[:-1]):
            res.append(word[:-1])
        return res
