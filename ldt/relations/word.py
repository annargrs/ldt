# -*- coding: utf-8 -*-
"""This module provides an alternative, word-based interface for
assembling all the information from all the ldt resources.

Example:

    >>> word = ldt.relations.word.Word("fishy")
    >>> word.pp_info()
    ======MORPHOLOGICAL INFO======
    POS :  ['adjective']
    IsLemma :  True
    Lemmas :  ['fishy']
    ======DERIVATIONAL INFO======
    Stems :  ['fish']
    Suffixes :  ['-y']
    Prefixes :  []
    OtherDerivation :  []
    RelatedWords :  ['cold fish', 'fishline', 'fishwoman', 'fish
    pondfishpond', 'fishery', 'fishmoth', 'unfishy', 'fishmonger',
    'fish sauce', 'starfish', 'fish feed', 'jellyfish', 'shellfish',
    'fishgig', 'fish tankfishtank', 'fish bowlfishbowl', 'surgeonfish',
    'fishnetfishnet stockings', 'fishpox', 'theres plenty more fish in the
    sea', 'have other fish to fry', 'fishcake', 'fish hookfishhook',
    'fish slice', 'fishling', 'drink like a fish', 'tuna fish', 'fishpound',
    'lumpfish', 'queer fish', 'overfish', 'like shooting fish in a barrel',
    'fish and chips', 'swim like a fish', 'fish pastefishpaste', 'fishless',
    'fishtail', 'fish food', 'fishable', 'fishbrain', 'fishmeal',
    'goatfish', 'dragonfish', 'goldfish', 'fishing', 'fisher',
    'unfishiness', 'fishly', 'fish finger', 'fish-eating grin', 'fish out',
    'give a man a fish and you feed him for a day teach a man to fish and
    you feed him for a lifetime', 'silverfish', 'fish', 'big fish in a small
    pond', 'fish ladder', 'fishskin', 'fish out of water', 'fish tape',
    'fishkill', 'fishroom', 'fishworm', 'neither fish nor fowl', 'fishful',
    'fishway', 'fishy', 'sailfish', 'fishwife', 'fishlike', 'fishskin
    disease', 'fisherman', 'fish supper', 'fishkind', 'bony fish']
    ======SEMANTIC INFO======
    Synonyms :  ['fishlike', 'fishly', 'fishy', 'fishy wishy', 'funny',
    'ichthyic', 'piscine', 'shady', 'suspect', 'suspicious']
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

import functools

from ldt.dicts.normalize import Normalization as Normalizer
from ldt.dicts.derivation.meta import DerivationAnalyzer
from ldt.dicts.semantics.metadictionary import MetaDictionary
from ldt.load_config import config

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
            self._normalizer = Normalizer()
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



    @functools.lru_cache(maxsize=config["cache_size"])
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
            self._analyze_derivation()
            self._get_lex_relations()

    def _normalize(self):
        """Bringing in the information from the _normalizer class."""

        self.info["OriginalForm"] = self.original_spelling

        res = self._normalizer.normalize(self.original_spelling)
        categories = ["Noise", "Numbers", "URLs", "Hashtags", "Filenames",
                      "Misspellings", "ProperNouns", "ForeignWords"]
        if res["word_categories"]:
            if not "Missing" in res["word_categories"]:
                for cat in categories:
                    self.info[cat] = cat in res["word_categories"]
            else:
                for cat in categories:
                    self.info[cat] = None

            # self.info["Noise"] = "Noise" in res["word_categories"]
            # self.info["Numbers"] = "Numbers" in res["word_categories"]
            # self.info["URLs"] = "URLs" in res["word_categories"]
            # self.info["Hashtags"] = "Hashtags" in res["word_categories"]
            # self.info["Filenames"] = "Filenames" in res["word_categories"]
            # self.info["Misspellings"] = "Misspellings" in res["word_categories"]

            self.info["Missing"] = "Missing" in res["word_categories"]

            # self.info["ProperNouns"] = "Names" in res["word_categories"]
            # self.info["ForeignWords"] = "Foreign" in res["word_categories"]


            if not "lemmas" in res:
                res["lemmas"] = []

            if len(res["lemmas"]) == 1 and res["lemmas"][0] == \
                    self.original_spelling:
                self.info["IsLemma"] = True
            elif self.info["Missing"]:
                self.info["IsLemma"] = None
            else:
                self.info["IsLemma"] = False
            self.info["Lemmas"] = frozenset(res["lemmas"])
            if "pos" in res:
                self.info["POS"] = frozenset(res["pos"])
            # else:
            #     self.info["POS"] = frozenset(["unclear"])


    def _analyze_derivation(self):
        """Query the morphological metadictionary for the information on
        semantic relations of the target word.

        Args:
            word (ldt.Word object): the word to look up.

        Returns:
            (None): the roots, prefixes, suffixes, related_words attributes of
            the Word object are updated with the derivational information.
        """
        fields = {"roots":"Stems", "suffixes":"Suffixes",
            "prefixes":"Prefixes", "related_words":"RelatedWords",
            "other":"OtherDerivation"}

        for lemma in self.info["Lemmas"]:

            res = self._derivation_dict.analyze(lemma)
            for i in res.keys():
                if not i in self.info:
                    self.info[i] = res[i]
                else:
                    self.info[i] += res[i]

            for i in fields.keys():
                self.info[i] = frozenset(self.info[i])
                self.info[fields[i]] = self.info.pop(i)

    def _get_lex_relations(self):
        """Query the lexicographic metadictionary for the information on
        semantic relations of the target word.

        Args:
            word (str): the word to look up.

        Returns:
            (None): the semantics attribute of the Word object is updated
            with the dictionary containing relation information.
        """
        main_rels = ["Synonyms", "Antonyms", "Hypernyms", "Meronyms",
                     "Hyponyms"]

        for lemma in self.info["Lemmas"]:
            res = self._lex_dict.get_relations(lemma)

            if res:
                for rel in res:
                    rel_cap = rel.capitalize()
                    if rel_cap in main_rels:
                        if not rel_cap in self.info:
                            self.info[rel_cap] = res[rel]
                        else:
                            self.info[rel_cap] += res[rel]
                    else:
                        if not "OtherRelations" in self.info:
                            self.info["OtherRelations"] = res[rel]
                        else:
                            self.info["OtherRelations"] += res[rel]

        for rel in main_rels+["OtherRelations"]:
            if rel in self.info:
                self.info[rel] = frozenset(self.info[rel])
            else:
                self.info[rel] = frozenset()

    def pp_info(self):
        """Pretty printing all the attributes of the word object."""

        def print_rel(i, dictionary):
            """Printing helper"""
            if i in dictionary:
                if isinstance(dictionary[i], frozenset):
                    print(i, ": ", ', '.join(dictionary[i]))
                else:
                    print(i, ": ", dictionary[i])

        print("\n\n====== "+self.info["OriginalForm"].upper()+" ======")

        print("\n====== MORPHOLOGICAL INFO ======")
        for i in ["OriginalForm", "POS", "IsLemma", "Lemmas"]:
            print_rel(i, self.info)
        print("\n====== DERIVATIONAL INFO ======")
        for i in ["Stems", "Suffixes", "Prefixes", "OtherDerivation",
                  "RelatedWords"]:
            print_rel(i, self.info)
        print("\n====== SEMANTIC INFO ======")
        for i in ["Synonyms", "Antonyms", "Meronyms", "Hyponyms",
                  "Hypernyms", "Other"]:
            print_rel(i, self.info)
        print("\n====== EXTRA WORD CLASSES ======")
        for i in ["ProperNouns", "Noise", "Numbers", "URLs", "Hashtags", "Filenames", \
    "ForeignWords", "Misspellings", "Missing"]:
            print_rel(i, self.info)
        print("\n")

# if __name__ == '__main__':
#     cat = Word("cat")
#     cat.pp_info()
