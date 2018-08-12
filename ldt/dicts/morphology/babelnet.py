# -*- coding: utf-8 -*-
""" This module provides interface for the morphological information in
BabelNet.

    The current functionality includes retrieving POS information.

"""

from ldt.dicts.base.babelnet import BaseBabelNet as BaseBabelNet
from ldt.dicts.morphology.morph_dictionary import MorphDictionary as \
    MorphDictionary
from ldt.load_config import config as config

class MorphBabelNet(MorphDictionary, BaseBabelNet):
    """This class implements querying morphological information from
    BabelNet. At the moment, only POS tags can be obtained."""

    def __init__(self, language=config["default_language"],
                 babelnet_key=config["babelnet_key"]):
        """ Initializing the base class.

        Args:
            language (str): the language of the query
            babelnet_key (bool): the user key for BabelNet API

        """

        super(MorphBabelNet, self).__init__(language=language,
                                            babelnet_key=babelnet_key)

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

        word = self.get_ids(word, full=True)

        if not word:
            return {}

        res = {}
        for entry in word:
            if entry["pos"] not in res:
                res[entry["pos"]] = 1
            else:
                res[entry["pos"]] += 1
        res = {k.lower(): v for k, v in res.items()}

        if format == "list":
            res = list(res.keys())
        return res

    def lemmatize(self, word):
        """BabelNet currently does not support lookup of non-lemmatized forms.

        Args:
            word (str): the word to be looked up

        Returns:
            (list): lemma(s) of the given word

        Todo:
        """

        raise NotImplementedError()
