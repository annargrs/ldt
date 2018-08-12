# -*- coding: utf-8 -*-
""" This module provides base interface for the NLTK's Princeton WordNet.

    The current functionality includes:

     - Determining whether a word entry exists;
     - Raising DictError for any language other than English

    Todo:
        * a wordnet metaclass that would call language-specific wordnets

"""


# import functools
# import timeout_decorator

from nltk.corpus import wordnet as wn


from ldt.dicts.dictionary import Dictionary as Dictionary
from ldt.helpers.exceptions import LanguageError as LanguageError


class BaseWordNet(Dictionary):
    """The class providing the basic English WordNet interface.

    Since WordNets are language-specific, any further additions will have to
    implement similar classes for other languages.

    Todo:

        * Definitions and examples

    """

    def __init__(self, **kw):  #pylint: disable=unused-argument
        """ Initializing the BaseWordNet class.

        Sets language to "en"

        """

        super(BaseWordNet, self).__init__()
        self._language = "en"

    def _set_language(self, language):
        """This ensures the language is suppported."""
        if language not in ["English", "english", "en"]:
            raise LanguageError("Only English WordNet is supported at the "
                                "moment.")
        self._language = language

    def is_a_word(self, word):
        """ Determines whether a WordNet entry exists for this word.

        Args:
            word (str): the input word to look up.

        Returns:
            (bool): *True* if the word entry was found.

        """

        if wn.synsets(word):
            return True
        return False
