# -*- coding: utf-8 -*-
"""Sometimes dictionaries lack antonymy relations for derivational pairs
where one of the word has a negative suffix or prefix (e.g. *regular ~
irregular*). LDT attempts to establish the relation through lists of
such language-specific suffixes/prefixes.

Example:
    >>> test_dict = ldt.relations.RelationsInPair()
    >>> test_dict.analyze("black", "white")
    ['SharedPOS', 'SharedMorphForm', 'Antonyms']
    >>> test_dict.analyze("happy", "happily")
    ['Synonyms', 'SharedMorphForm', 'SharedDerivation']

"""

import os
from ldt.helpers.loading import load_language_file as load_language_file
from ldt.helpers.resources import lookup_language_by_code as \
    lookup_language_by_code

class DerivationalAntonymy(object):

    def __init__(self, language):

        if len(language) > 2:
            language = lookup_language_by_code(language.lower(), reverse=True)
        self.language = language

        dir_path = os.path.dirname(os.path.realpath(__file__))
        resources_path = os.path.join(dir_path,
                                      "antonymy_by_derivation/" + language +
                                      ".yaml")
        resources = load_language_file(resources_path, self.language)
        self.prefixes = resources["prefixes"]
        self.suffixes = resources["suffixes"]


def detect_antonymy(self, target, neighbor):
    """
    establish the antonymy relation
    :param neighbor, : ldt word object
    :return: ldt word object
    """


    for i in prefixes:
        if i in neighbor.affixes:
            for w in list(neighbor.spellings.keys()) + [
                neighbor.original_spelling]:
                if w.startswith(i[:-1]):
                    stem = w[len(i) - 1:]
                    #                elif w.startswith(i[:-1]):
                    if stem in target.spellings:
                        return True
    for i in suffixes:
        if i in neighbor.affixes:
            for w in list(neighbor.spellings.keys()) + [
                neighbor.original_spelling]:
                if w.endswith(i[1:]):
                    stem = w[:len(i)]
                    if stem in target.spellings:
                        return True
    return False