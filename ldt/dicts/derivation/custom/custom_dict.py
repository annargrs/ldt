# -*- coding: utf-8 -*-
""" This module provides interface for the productive morphological patterns
in LDT.

The current functionality includes loading of language-specific resources
(prefixes, suffixes, etc):

    Todo:

        * check what happens when lists in yaml are empty
        * implement replacements in compounds (prazdnoshatayushchijsya) and
            joining symbols (German "s")

"""

from ldt.load_config import config as config
from ldt.dicts.derivation.custom.affixes import Affixes as Affixes
from ldt.dicts.derivation.custom.compounds import Compounds as Compounds

class DerivationCustomDict(Affixes, Compounds):
    """This class implements a generic interface for custom
    language-specific derivational dictionaries."""

    def __init__(self, language=config["default_language"], dictionary=None,
                 morph_dictionary=None):
        """ Initializing the base class.

        Args:
            language (str): the language of the dictionary (only
                English currently supported)
            dictionary (base dictionary object): an LDT dictionary inheriting
                from one of the classes in ``ldt.dicts.base``.
            morph_dictionary (morph dictionary object): an LDT dictionary
                inheriting from one of the classes in ``ldt.dicts.morphology``.

        Note:

            Using WordNets as a base dictionary for derivational analysis is
            not recommended, as they do not include many closed-class parts
            of speech that may occur in compounds.

        """
        super(DerivationCustomDict, self).__init__(language=language,
                                                   dictionary=dictionary,
                                                   morph_dictionary=
                                                   morph_dictionary)
