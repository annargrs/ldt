# -*- coding: utf-8 -*-
""" This module provides interface for retrieving derivation information from
Wiktionary.

    The current functionality includes lookup of the words listed as
    "derivationally related" in Wiktionary, and also rule-based parsing of
    its etymologies.

"""

from difflib import SequenceMatcher
import functools

from ldt.helpers.formatting import strip_non_alphabetical_characters
from ldt.dicts.base.wiktionary import BaseWiktionary
from ldt.dicts.semantics.wiktionary import Wiktionary
from ldt.load_config import config

class DerivationWiktionary(BaseWiktionary):
    """This class implements querying morphological information from
    Wiktionary. At the moment, only POS tags can be obtained."""

    def __init__(self, language=config["default_language"],
                 cache=config["wiktionary_cache"]):
        """ Initializing the base class.

        Args:
            language (str): the query language
            cache (bool): whether wiktionary cache shuld be used

        """

        super(DerivationWiktionary, self).__init__(language=language,
                                                   cache=cache)
    def _get_etymologies(self, word):
        """Getting basic list of etymology sections from Wiktionary

        Args:
            word (str): the word to look up

        Returns:
            (list): a list of etymology entries
        """
        word = self.query(word)
        if word:
            etymologies = []
            for i in word:
                if " " in i["etymology"]:
                    if "+\u200e" in i["etymology"]:
                        etymologies.append(i["etymology"])
            #     for subentry in i.items():
            #         if " " in i["etymology"]:
            #             if "+\u200e" in i["etymology"]:
            #                 etymologies.append(i["etymology"])
            # etymologies = list(set(etymologies))
            return etymologies


    @functools.lru_cache(maxsize=config["cache_size"])
    def get_etymologies(self, word, exclude_old_sources=None):
        """Rule-based parsing of Wiktionary etymologies.

        Wiktionary etymologies are a mess. This method goes through the
        "etymology" section, looking for prefixes and suffixes
        (assuming that they will have a dash, e.g. *-ness*), and then also for
        potential stems that are at least 0.7 similar to the source word
        (as measured by SequenceMatcher).

        Args:
            word_string (str): a potential derived word
            exclude_old_sources (LDT dictionary object: if not None,
            the specified dictionary is used to filter out any words not
            found as separate entries (see :meth:`is_a_word`) of
            `ldt.dicts.base` classes.

        .. note::
            Filtering by modern dictionaries is not perfect. Without
            *exclude_old_sources* option, you will get e.g. *'brotherhede'*
            as source for *brotherhood*, but even with it, you still get
            *brotherred*, as it is registered as a separate entry in Wiktionary.

        Returns:
            tuple: ([list of found stems or obsolete forms of the target word],
            [list of found affixes])

        """

        # todo experiment with ldt spellchecker instead of pyenchant default
        # word = dict.noise.query(word_string)

        etymologies = self._get_etymologies(word)
        if not etymologies:
            return None

        useful = _separate_affixes(etymologies)
        affixes = useful[1]
        words = useful[0]
        if not affixes:
            return None

        res = []
        for i in words:  #pylint: disable=too-many-nested-blocks
            candidate_word = strip_non_alphabetical_characters(i)
            if candidate_word and candidate_word != word:
                for affix in affixes:

                    if affix[0] == "-":
                        candidate = candidate_word[:-1] + affix.strip("-")
                    elif affix[-1] == "-":
                        candidate = strip_non_alphabetical_characters(affix) \
                                    + candidate_word

                    if SequenceMatcher(None, word, candidate).ratio() > 0.7:
                        if exclude_old_sources:
                            if exclude_old_sources.is_a_word(candidate_word):
                                res.append(candidate_word)
                        else:
                            res.append(candidate_word)
        return (list(set(res)), affixes,)

    def get_related_words(self, word, dictionary=None):
        """A wrapper for methods in semantic Wiktionary dictionary

        Args:
            word (str): the word to look up
            dictionary (ldt Wiktionary object): if provided, it will be used
                for retrieving relations. Otherwise an object will be
                instantiated.

        Returns:
            (list): the words listed as derivationally related to the target
            word
        """
        if not dictionary:
            dictionary = Wiktionary(language=self.language, cache=self.cache)
        related_terms = dictionary.get_relation(word, relation="derived terms")
        return related_terms

# todo derivational families through the sem dict methods


def _separate_affixes(etymologies):
    """Helper for :meth:`get_etymologies`.

    Args:
        etymologies (list): the list of etymology entries

    Returns:
        (tuple): ([a list of words in etymologies], [a list of potential
        prefixes and/or suffixes])

    """
    affixes = []
    for etymology in etymologies:
        words = etymology.split()
    cleaned = []
    for etymology in words:
        if not "+" in etymology:
            cleaned.append(etymology)
    words = cleaned

    # try to find suffixes or the prefixes:
    for i in words:
        if i[0] == "-" or i[-1] == "-":
            affixes.append(i)
    cleaned_affixes = []
    for affix in affixes:
        cleaned_affixes.append(
            strip_non_alphabetical_characters(affix, ignore=["-"]))
    affixes = cleaned_affixes
    return (words, affixes,)
