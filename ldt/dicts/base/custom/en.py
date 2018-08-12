# -*- coding: utf-8 -*-
""" This module provides base interface for the LDT custom base dictionary.

    Currently only English is supported.

     - Raising DictError on setting the language other than English
     - Adding a Dictionary argument for is_a_word method.

    Todo:

        - Handling other languages on initialization

"""


from ldt.dicts.dictionary import Dictionary as Dictionary
from ldt.helpers.exceptions import LanguageError as LanguageError

class BaseCustomDict(Dictionary):
    """The class providing the basic LDT dictionary class that implements
    custom morphological rules. Any further extensions will have to implement
    similar classes for other languages.

    """

    def __init__(self, **kw):  #pylint: disable=unused-argument
        """ Initializing the BaseLDT class.

        Sets language to "en"

        """

        super(BaseCustomDict, self).__init__()
        self._language = "en"

    def _set_language(self, language):
        """This ensures the language is suppported."""
        if language not in ["English", "english", "en"]:
            raise LanguageError("Only English is supported at the moment.")
        self._language = language

    #pylint: disable=arguments-differ
    def is_a_word(self, word, dictionary):
        """ Determines whether a WordNet entry exists for this word.

        Args:
            word (str): the input word to look up.

        Returns:
            (bool): *True* if the word entry was found.

        """

        pass
