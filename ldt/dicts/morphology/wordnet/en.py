# -*- coding: utf-8 -*-
""" This module provides interface for the morphological information in NLTK's
Princeton WordNet.

    The current functionality includes:

     - Retrieving POS information;
     - Retrieving morphological form of an entry;
     - Retrieving possible lemmas of a word.

Note:

  This class relies on a pre-build list of WordNet lemmas (``en.vocab``),
  since it is not accessible directly in NLTK and re-building it every time
  is too slow. It will need updating in future releases.

    Todo:
        * a wordnet metaclass that would call language-specific wordnets
        * "governess" gets lemmatized as "govern"

"""

import os

from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

from ldt.dicts.base.wordnet.en import BaseWordNet
from ldt.dicts.morphology.morph_dictionary import MorphDictionary
from ldt.load_config import config
from ldt.helpers.loading import load_resource


class MorphWordNet(MorphDictionary, BaseWordNet):
    """This class implements an interface for retrievning POS
    information from NLTK WordNet and lemmatization."""

    def __init__(self, language=config["default_language"],
                 lowercasing=config["lowercasing"]):
        """ Initializing the base class.

        Args:
            language (str): the language of the dictionary (only
            English WordNet currently supported)

        """

        super(MorphWordNet, self).__init__(language=language,
                                           lowercasing=lowercasing)

        # loading a pre-built list of wordnet lemmas. building it anew on
        # initialization of dictionary is too slow.
        dir_path = os.path.dirname(os.path.realpath(__file__))
        lemmas_path = os.path.join(dir_path, "en.vocab")
        lemmas = load_resource(lemmas_path)
        self.lemmas = lemmas
        # all_wn_lemmas = []
        # for synset in wn.all_synsets():
        #     all_wn_lemmas += synset.lemma_names()
        # self.lemmas = set(all_wn_lemmas)

    def get_pos(self, word, formatting="dict"):
        """Stub for the method of all subclasses of MorphDictionary that
        returns parts of speech for a given word.

        Args:
            word (str): the word to be looked up
            formatting (str): the format of output:

                *dict* for a dictionary of part-of-speech-tags, with number
                of senses with that POS as values
                *list*: a list of all available POS tags for the word

        Note:
            LDT ignores the distingion between "head" and "satellite"
            adjectives that Princeton WordNet makes (both "s" and "a" tags
            are mapped to "adjective")

        Returns:
            (dict, list): a list of part-of-speech tags for the given word,
            or a

        Todo:
            * pos format
        """
        word = self._lowercase(word)
        poses = []
        res = {}
        tags = [".v.", ".n.", ".a.", ".r.", ".s."]
        for synset in wn.synsets(word):
            name = synset.name()
            #        ss.append(s.name())
            for tag in tags:
                if tag in name:
                    poses.append(tag.strip("."))
        for pos in list(set(poses)):
            res[pos] = poses.count(pos)
        # normalize the pos tags
        new_tags = {
            "n": "noun", "v": "verb", "a": "adjective", "r": "adverb",
            "s": "adjective"
        }
        new_res = {new_tags[k]: res[k] for k in res}
        if formatting == "list":
            new_res = list(new_res.keys())
        return new_res

    def lemmatize(self, word):
        """The method returning all possible dictionary form(s) for a given
        word.

        Only the orthographically unique lemmas are returned. For example,
        *walks* could be lemmatized as *walk* both as a noun and as a verb,
        but only one *walk* is returned.

        Args:
            word (str): the word to be looked up

        Returns:
            (list): lemma(s) of the given word

        Todo:
        """
        word = self._lowercase(word)
        res = []
        if word in self.lemmas:
            res.append(word)
        if word[-1] in ["e", "t", "n", "d", "w", "g", "k", "l", "s", "y",
                        "m", "n"]:
            verb = WordNetLemmatizer().lemmatize(word, 'v')
            if verb != word:
                res.append(verb)
        if word.endswith("er") or word.endswith("est"):
            adjective = WordNetLemmatizer().lemmatize(word, 'a')
            if adjective != word:
                res.append(adjective)
        if word.endswith("s"):
            noun = WordNetLemmatizer().lemmatize(word, 'n')
            if noun != word:
                res.append(noun)
        if not res:
            if self.is_a_word(word):
                res.append(word)
        # for synset in wn.synsets(word):
        #     if synset.name().split(".")[0] == word:
        #         res.append(word)
        #         break
        return list(set(res))
