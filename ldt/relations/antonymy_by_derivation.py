# -*- coding: utf-8 -*-
"""Sometimes dictionaries lack antonymy relations for derivational pairs
where one of the word has a negative suffix or prefix (e.g. *regular ~
irregular*). LDT attempts to establish the relation through lists of
such language-specific suffixes/prefixes that negate the meaning of the stem.

It is also possible to detect pairs of words with complementary affixes,
such as *-ful* and *-less* in *careful : careless*.

Example:
    >>> test_dict = ldt.relations.antonymy_by_derivation.DerivationalAntonymy(language="English")
    >>> test_dict.detect_anonymy("regular", "irregular")
    True
    >>> test_dict.detect_anonymy("pre-war", "post-war")
    True
    >>> test_dict.detect_anonymy("regular", "cat")
    False

"""

import os
from ldt.helpers.loading import load_language_file
from ldt.helpers.resources import lookup_language_by_code
from ldt.relations.word import Word

class DerivationalAntonymy(object):
    """Dictionary of language-specific derivational patterns that could be
    used to detect derivational antonymy."""
    def __init__(self, language):

        if len(language) > 2:
            language = lookup_language_by_code(language.lower(), reverse=True)
        self.language = language

        dir_path = os.path.dirname(os.path.realpath(__file__))
        resources_path = os.path.join(dir_path,
                                      "antonymy_by_derivation/" + language +
                                      ".yaml")
        resources = load_language_file(resources_path, self.language)
        self.resources = resources


    def are_related(self, target, neighbor):
        """
        The main method for detecting derivational antonyms.

        Args:

            target, neighbor (ldt Word obj or str): the words to check for this
            relationship;

        Returns:
             (bool): True if derivational antonymy was detected.

        """

        if isinstance(target, str):
            target = Word(target)
        if isinstance(neighbor, str):
            neighbor = Word(neighbor)

        def detect_affixes(word1, word2, affix="Prefixes"):
            """Helper function for handling negative prefixes and affixes."""
            if word1.info[affix]:
                for i in word1.info[affix]:
                    if i in self.resources[affix]:
                        if affix == "Prefixes":
                            if word2.info["OriginalForm"] in word1.info["Stems"] \
                                    and i.strip("-") + word2.info["OriginalForm"]\
                                    == word1.info["OriginalForm"]:
                                return True
                        elif affix == "Suffixes":
                            if word2.info["OriginalForm"] in word1.info["Stems"] \
                                    and word2.info["OriginalForm"] + i.strip("-") \
                                    == word1.info["OriginalForm"]:
                                return True
            return False


        def detect_affix_pairs(word1, word2, affix="Prefixes"):
            """Helper function for handling pairs of affixes. Word length
            serves as the final check on whether the decomposition is
            complete."""
            for pair in self.resources[affix[:-2]+"_pairs"]:
                if pair[0] in word1.info[affix] and pair[1] in word2.info[affix]:
                    shared_stem = set(word1.info["Stems"]).intersection(
                        word2.info["Stems"])
                    if shared_stem:
                        len_word = len(list(shared_stem)[0]) + len(pair[0])-1
                        if len_word == len(word1.info["OriginalForm"]):
                            return True
                        elif word1.info["OriginalForm"].count("-") == 1 and \
                                len_word+1 == len(word1.info["OriginalForm"]):
                            return True
            return False

        checks = [detect_affixes(target, neighbor, affix="Prefixes"),
                  detect_affixes(neighbor, target, affix="Prefixes"),
                  detect_affixes(neighbor, target, affix="Suffixes"),
                  detect_affixes(target, neighbor, affix="Suffixes"),
                  detect_affix_pairs(target, neighbor, affix="Suffixes"),
                  detect_affix_pairs(neighbor, target, affix="Suffixes"),
                  detect_affix_pairs(neighbor, target, affix="Prefixes"),
                  detect_affix_pairs(target, neighbor, affix="Prefixes")]

        for check in checks:
            if check:
                return True
        return False
