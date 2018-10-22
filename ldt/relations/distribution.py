# -*- coding: utf-8 -*-
"""This module provides functionality for retrieval of distributional
information."""

from ldt.dicts.resources import ResourceDict
from ldt.load_config import config

class DistributionDict():

    """The class provides a single interface to retrieving distributional
    information in ldt: cooccurrence in the specified corpus, in google
    dependency ngrams, and freqnuency in the specified corpus.

    Args:
        language (str): the language of the resource
        corpus (str): the corpus, for which the distributional information is
            to be retrieved
        gdeps (bool): whether to use google dependency resource
            (memory-intensive)
        cooccurrence (bool): whether to use cooccurrence information
            (memory-intensive)
        cooccurrence_freq (bool): if True, cooccurrence counts are returned
            rather than booleans (even more memory-intensive)
        wordlist (list of str): if a wordlist is provided, the resources
            with distributional data will be filtered down to the words in
            the wordlist, significantly decreasing the memory usage

    """

    def __init__(self, language=config["default_language"],
                 corpus=config["corpus"], gdeps=False,
                 cooccurrence=False, cooccurrence_freq=False, wordlist=None):

        super(DistributionDict, self).__init__()

        #: str: the language of the resource
        self.language = language

        if gdeps:
            #: ResourceDict: google dependency resource
            self.gdeps = ResourceDict(resource="gdeps", language=language)
            if wordlist:
                self.gdeps.data = _filter_by_list(self.gdeps.data, wordlist)

        if cooccurrence:
            #: ResourceDict: cooccurrence resource
            self.cooccurrence = ResourceDict(resource="cooccurrence",
                                             corpus=corpus,
                                             freq=cooccurrence_freq)
            if wordlist:
                self.cooccurrence.data = _filter_by_list(
                        self.cooccurrence.data, wordlist)

        #: hidden parameter for :meth:`cooccur_in_corpus`
        self._freq = cooccurrence_freq
        #: ResourceDict: frequency dictionary
        self.freqdict = ResourceDict(resource="freqdict", corpus=corpus)




    def frequency_in_corpus(self, word):
        """Wrapper method for retrieving word frequency.

        Args:
            word (str): the word to look up.

        Returns:
            (int): the frequency of the word in the corpus.

        """
        try:
            return int(self.freqdict.data[word])
        except KeyError:
            return 0

    def cooccur_in_corpus(self, word1, word2):
        """Wrapper method for retrieving cooccurrence information.

        Args:
            word (str): the word to look up.

        Returns:
            (bool): True if the two words do cooccur.

        """
        if hasattr(self, "cooccurrence"):
            return self.cooccurrence.are_related(word1, word2, freq=self._freq)
        return False


    def cooccur_in_gdeps(self, word1, word2):
        """Wrapper method for retrieving cooccurrence information for google
        dependency ngram resource.

        Args:
            word (str): the word to look up.

        Returns:
            (bool): True if the two words do cooccur in google dependency
            ngrams.

        """
        if hasattr(self, "gdeps"):
            return self.gdeps.are_related(word1, word2)
        return False

def _filter_by_list(data, wordlist):
    """Helper for loading larger dictionary-based resources:
    memory will be freed by only keeping the words relevant for the
    given session"""
    new_data = {}
    for i in wordlist:
        if i in data:
            new_data[i] = data[i]
    return new_data