# -*- coding: utf-8 -*-
"""This module provides an interface to all the individual ontology
resources. Each language-specific module must implement a `get_shortest_path`
function that takes two words (strings) and outputs a similarity score.

Examples:
    >>> test_dict = ldt.relations.ontology_path.ontodict.OntoDict(language="English")
    >>> test_dict.get_shortest_path("tree", "apple")
    0.05
    >>> test_dict.get_shortest_path("tree", "cider")
    0.07142857142857142

"""

from importlib import import_module
from ldt.dicts.dictionary import Dictionary
from ldt.helpers.resources import lookup_language_by_code

class OntoDict(Dictionary):
    """The class providing the interface to different language-specific
    _ontodict resource. Only English is currently supported (using WordNet
    similarity paths as distance measure).

    """

    def __init__(self, **kw):  #pylint: disable=unused-argument
        """ Initializing the OntoDict class.

        """

        super(OntoDict, self).__init__(**kw)
        if len(self.language) > 2:
            self.language = lookup_language_by_code(self.language, reverse=True)

        try:
            self._ontodict = import_module(
                'ldt.relations.ontology_path.'+self.language)
        #pylint: disable=bare-except
        except:
            print("Something went wrong. If the language " +
                  self.language + "is supposed to be supported, check the "
                  "module ldt.relations.ontology_path."
                  + self.language+".py.")

    def is_a_word(self, word):
        raise NotImplementedError

    def get_shortest_path(self, word1, word2):
        """Wrapper for language-specific function `get_shortest_path`."""
        return self._ontodict.get_shortest_path(word1, word2)
