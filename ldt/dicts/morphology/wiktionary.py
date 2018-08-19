# -*- coding: utf-8 -*-
""" This module provides interface for the morphological information in
Wiktionary.

    The current functionality includes retrieving POS information.

"""

from ldt.dicts.base.wiktionary import BaseWiktionary as BaseWiktionary
from ldt.dicts.morphology.morph_dictionary import MorphDictionary as \
    MorphDictionary
from ldt.load_config import config as config

class MorphWiktionary(MorphDictionary, BaseWiktionary):
    """This class implements querying morphological information from
    Wiktionary. At the moment, only POS tags can be obtained."""

    def __init__(self, cache=config["wiktionary_cache"], language=config[
        "default_language"], lowercasing=config["lowercasing"],
                 split_mwu=config["split_mwu"]):
        """ Initializing the base class.

        Args:
            language (str): the query language
            cache (bool): whether wiktionary cache shuld be used

        """

        super(MorphWiktionary, self).__init__(cache=cache, language=language,
                                              lowercasing=lowercasing,
                                              split_mwu=split_mwu)

    def get_pos(self, word, formatting="dict"):
        """Retrieving parts of speech for a given word.

        Args:
            word (str): the word to be looked up
            formatting (str): the format of output:

                *dict* for a dictionary of part-of-speech-tags, with number
                of senses with that POS as values
                *list*: a list of all available POS tags for the word

        Returns:
            (list): part-of-speech tags for the given word

        Todo:
            * pos format
        """

        word = self.query(self._lowercase(word))

        if not word:
            return {}
        poses = []
        res = {}
        for i in word:
            #        print(i)
            for entry in i.items():
                if entry[0] == "definitions":
                    for line in entry[1]:
                        poses.append(line["partOfSpeech"])
        for pos in list(set(poses)):
            res[pos] = poses.count(pos)
        if format == "list":
            res = list(res.keys())
        return res

    def lemmatize(self, word):
        """Wiktionary currently does not support lookup in non-lemmatized
        forms. If a word is found, LDT assumes that it is a lemma.

        Args:
            word (str): the word to be looked up

        Returns:
            (list): lemma(s) of the given word

        Todo:
        """
        if self.is_a_word(word):
            return [word]
