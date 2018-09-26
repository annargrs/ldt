# -*- coding: utf-8 -*-
""" This module provides interface for retrieving derivationally related
    words from NLTK's Princeton WordNet.

"""

from nltk.corpus import wordnet as wn

from ldt.dicts.base.wordnet.en import BaseWordNet
from ldt.load_config import config


class DerivationWordNet(BaseWordNet):
    """This class implements an interface for retrievning derivationally
    related words from NLTK WordNet."""

    def __init__(self, language=config["default_language"]):
        """ Initializing the base class.

        Args:
            language (str): the language of the dictionary (only
            English WordNet currently supported)

        """

        super(DerivationWordNet, self).__init__(language=language)

    def get_related_words(self, word):
        """Method for retrieving words that are listed as
        derivationally related in WordNet.

        A wrapper for NLTK's `derivationally_related_forms()
        <http://www.nltk.org/api/nltk.corpus.reader.html#nltk.corpus.reader
        .wordnet.Lemma.derivationally_related_forms>`_
        function that processes all possible synsets of the input word.

        Args:
            word (str): a word for which derivationally related words
            will be returned

        Returns:
            list: a list of words derivationally related to the input one in
            any of its senses

        """
        if not self.is_a_word(word):
            return None

        res = []
        for synset in wn.synsets(word):
            if word in synset.name():
                for lemma in synset.lemmas():
                    string = str(lemma).split(".")
                    if word in string[-1]:
                        for w in lemma.derivationally_related_forms():
                            res.append(w.name())
        if res:
            return list(set(res))
        return res