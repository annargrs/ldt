# -*- coding: utf-8 -*-
"""This module provides an alternative, word-based interface for
assembling all the information from all the ldt resources.

Example:

    >>> word = ldt.relations.word.Word("government")
    >>> word.all_info()
    ======MORPHOLOGICAL INFO======
    POS :  ['adjective']
    IsLemma :  True
    Lemmas :  ['fishy']
    ======DERIVATIONAL INFO======
    Stems :  ['fish']
    Suffixes :  ['-y']
    Prefixes :  []
    OtherDerivation :  []
    RelatedWords :  ['cold fish', 'fishline', 'fishwoman', 'fish pondfishpond', 'fishery', 'fishmoth', 'unfishy', 'fishmonger', 'fish sauce', 'starfish', 'fish feed', 'jellyfish', 'shellfish', 'fishgig', 'fish tankfishtank', 'fish bowlfishbowl', 'surgeonfish', 'fishnetfishnet stockings', 'fishpox', 'theres plenty more fish in the sea', 'have other fish to fry', 'fishcake', 'fish hookfishhook', 'fish slice', 'fishling', 'drink like a fish', 'tuna fish', 'fishpound', 'lumpfish', 'queer fish', 'overfish', 'like shooting fish in a barrel', 'fish and chips', 'swim like a fish', 'fish pastefishpaste', 'fishless', 'fishtail', 'fish food', 'fishable', 'fishbrain', 'fishmeal', 'goatfish', 'dragonfish', 'goldfish', 'fishing', 'fisher', 'unfishiness', 'fishly', 'fish finger', 'fish-eating grin', 'fish out', 'give a man a fish and you feed him for a day teach a man to fish and you feed him for a lifetime', 'silverfish', 'fish', 'big fish in a small pond', 'fish ladder', 'fishskin', 'fish out of water', 'fish tape', 'fishkill', 'fishroom', 'fishworm', 'neither fish nor fowl', 'fishful', 'fishway', 'fishy', 'sailfish', 'fishwife', 'fishlike', 'fishskin disease', 'fisherman', 'fish supper', 'fishkind', 'bony fish']
    ======SEMANTIC INFO======
    Synonyms :  ['fishlike', 'fishly', 'fishy', 'fishy wishy', 'funny', 'ichthyic', 'piscine', 'shady', 'suspect', 'suspicious']
    ======EXTRA WORD CLASSES======
    ProperNouns :  False
    Noise :  False
    Numbers :  False
    URLs :  False
    Hashtags :  False
    Filenames :  False
    ForeignWords :  False
    Misspellings :  False

Todo:

    * better controls on the initialization parameters of constituent
    dictionaries.
    * incorporate categories into the .info dict
    * check parsing of "senator" etymologies
    * pprint from yaml

"""

import inspect
import functools

from ldt.dicts.normalize import Normalization as Normalizer
from ldt.dicts.derivation.meta import DerivationAnalyzer as \
    DerivationAnalyzer
from ldt.dicts.metadictionary import MetaDictionary as MetaDictionary

class Word(object):
    """Class that binds together all linguistic information about a word from
    across ldt.dicts modules. This is simply to provide an alternative interface
    to all the information in the setting where all the different types of
    information are queried across vocabulary. If only a few resources are
    needed, it is more efficient to use the necesary dicts modules directly.

    Todo:

        * passable _normalizer dict parameter of what languages to consider
          foreign

    """

    def __init__(self, original_spelling, derivation_dict=None,
                 normalizer=None, lex_dict=None):
        """
        Initialize the word entry to be queried across the ldt.dicts resources.
        """
        #: str : the original spelling of a word

        self.original_spelling = original_spelling

        #: obj : the ldt.dicts.normalize  dictionary object
        if not normalizer:
            self._normalizer = Normalizer(language="English",
                                          order=("wordnet", "custom"),
                                          lowercasing=True)
        else:
            self._normalizer = normalizer

        if not derivation_dict:
            self._derivation_dict = DerivationAnalyzer()
        else:
            self._derivation_dict = derivation_dict

        if not lex_dict:
            self._lex_dict = MetaDictionary()
        else:
            self._lex_dict = lex_dict
        self.analyze(self.original_spelling)



    @functools.lru_cache(maxsize=None)
    def analyze(self, word):
        self.info = {}
        self._normalize()

        lookup = True
        for i in ["Numbers", "ProperNouns", "Noise", "URLs", "Filenames",
                  "ForeignWords"]:
            if self.info[i]:
                lookup = False
                break
        if lookup:
            self._analyze_derivation(self._lemma)
            self._get_lex_relations(self._lemma)

    def _normalize(self):
        """Bringing in the information from the _normalizer class."""
        res = self._normalizer.normalize(self.original_spelling)
        if res["word_categories"]:
            self.info["ProperNouns"] = "Names" in res["word_categories"]
            self.info["Noise"] = "Noise" in res["word_categories"]
            self.info["Numbers"] = "Numbers" in res["word_categories"]
            self.info["URLs"] = "URLs" in res["word_categories"]
            self.info["Hashtags"] = "Hashtags" in res["word_categories"]
            self.info["Filenames"] = "Filenames" in res["word_categories"]
            self.info["ForeignWords"] = "Foreign" in res["word_categories"]
            self.info["Misspellings"] = "Misspellings" in res["word_categories"]
            self.info["OriginalForm"] = self.original_spelling
            if not "lemmas" in res:
                res["lemmas"] = []

            if len(res["lemmas"]) == 1 and res["lemmas"][0] == \
                    self.original_spelling:
                self.info["IsLemma"] = True
            else:
                self.info["IsLemma"] = False
            if res["lemmas"]:
                self._lemma = res["lemmas"][0]
            self.info["Lemmas"] = frozenset(res["lemmas"])
            if res["pos"]:
                self.info["POS"] = frozenset(res["pos"])
            else:
                self.info["POS"] = frozenset(["unclear"])


    def _analyze_derivation(self, word):
        """Query the morphological metadictionary for the information on
        semantic relations of the target word.

        Args:
            word (str): the word to look up.

        Returns:
            (None): the roots, prefixes, suffixes, related_words attributes of
            the Word object are updated with the derivational information.
        """
        res = self._derivation_dict.analyze(word)
        self.info["Stems"] = frozenset(res["roots"])
        self.info["Suffixes"] = frozenset(res["suffixes"])
        self.info["Prefixes"] = frozenset(res["prefixes"])
        self.info["RelatedWords"] = frozenset(res["related_words"])
        self.info["OtherDerivation"] = frozenset(res["other"])

    def _get_lex_relations(self, word):
        """Query the lexicographic metadictionary for the information on
        semantic relations of the target word.

        Args:
            word (str): the word to look up.

        Returns:
            (None): the semantics attribute of the Word object is updated
            with the dictionary containing relation information.
        """
        res = self._lex_dict.get_relations(word)
        if res:
            for rel in res:
                if rel.capitalize() in ["Synonyms", "Antonyms", "Hypernyms",
                                        "Meronyms", "Hyponyms"]:
                    self.info[rel.capitalize()] = frozenset(res[rel])
                else:
                    if not "OtherRelations" in self.info:
                        self.info["OtherRelations"] = res[rel]
                    else:
                        self.info["OtherRelations"] += res[rel]
            if "OtherRelations" in self.info:
                self.info["OtherRelations"] = frozenset(self.info["OtherRelations"])

    def all_info(self):
        """Pretty printing all the attributes of the word object."""

        def print_rel(i, dictionary):
            """Printing helper"""
            if i in dictionary:
                if isinstance(dictionary[i], frozenset):
                    print(i, ": ", ', '.join(dictionary[i]))
                else:
                    print(i, ": ", dictionary[i])

        print("\n======MORPHOLOGICAL INFO======")
        for i in ["OriginalForm", "POS", "IsLemma", "Lemmas"]:
            print_rel(i, self.info)
        print("\n======DERIVATIONAL INFO======")
        for i in ["Stems", "Suffixes", "Prefixes", "OtherDerivation",
                  "RelatedWords"]:
            print_rel(i, self.info)
        print("\n======SEMANTIC INFO======")
        for i in ["Synonyms", "Antonyms", "Meronyms", "Hyponyms",
                  "Hypernyms", "Other"]:
            print_rel(i, self.info)
        print("\n======EXTRA WORD CLASSES======")
        for i in ["ProperNouns", "Noise", "Numbers", "URLs", "Hashtags", "Filenames", \
    "ForeignWords", "Misspellings"]:
            print_rel(i, self.info)

