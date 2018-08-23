# -*- coding: utf-8 -*-
"""This module provides an alternative, word-based interface for
assembling all the information from all the ldt resources.

Example:

    >>> word = ldt.relations.word.Word("government")
    >>> word.all_info()
    is_a_filename :  False
    is_a_hashtag :  False
    is_a_lemma :  True
    is_a_number :  False
    is_a_proper_noun :  False
    is_a_url :  False
    is_foreign :  False
    is_misspelled :  False
    is_noise :  False
    lemmas :  ['government']
    original_spelling :  government
    pos :  ['noun']
    prefixes :  []
    related_words :  ['governor', 'governance', 'governing', 'government']
    roots :  ['govern']
    semantics :  {'synonyms': ['administration', 'authorities', 'governance',
    'governing', 'government', 'government_activity', 'political_science',
    'politics', 'regime'], 'hyponyms': ['ancien_regime', 'authoritarian_regime',
    'authoritarian_state', 'big government', 'bureaucracy', 'court',
    'downing_street', 'empire', 'federal government', 'federal_government',
    'geopolitics', 'government-in-exile', 'lawmaking', 'legislating',
    'legislation', 'local government', 'local_government', 'military government',
    'military_government', 'minority government', 'misgovernment', 'misrule',
    'municipal government', 'palace', 'papacy', 'parliamentary government',
    'petticoat government', 'pontificate', 'practical_politics', 'pupet_regime',
    'puppet government', 'puppet_government', 'puppet_state', 'realpolitik',
    'representative government', 'royal_court', 'shadow government', 'state',
    'state_government', 'stratocracy', 'totalitarian_state', 'totalitation_regime',
    'trust_busting', 'unitary government'], 'hypernyms': ['polity',
    'social_control', 'social_science', 'system', 'system_of_rules'], 'meronyms':
    ['administration', 'bench', 'brass', 'division', 'establishment', 'executive',
    'general_assembly', 'governance', 'governing_body', 'government_department',
    'government_officials', 'judicatory', 'judicature', 'judicial_system',
    'judiciary', 'law-makers', 'legislative_assembly', 'legislative_body',
    'legislature', 'officialdom', 'organisation', 'organization']}
    suffixes :  ['-ment']

Todo:

    * better controls on the initialization parameters of constituent
    dictionaries.
    * pretty printing per category info
    * "senator" etymologies

"""

import inspect

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
        self._normalize(self.original_spelling)

        if not derivation_dict:
            self._derivation_dict = DerivationAnalyzer()
        else:
            self._derivation_dict = derivation_dict

        if not lex_dict:
            self._lex_dict = MetaDictionary()
        else:
            self._lex_dict = lex_dict

        if self.is_a_number or self.is_a_proper_noun or self.is_noise or \
                self.is_a_url or self.is_a_filename or self.is_foreign:
            lookup = False
        else:
            lookup = True
        if lookup:
            self._analyze_derivation(self.lemmas[0])
            self._get_lex_relations(self.lemmas[0])


    def _normalize(self, word):
        """Bringing in the information from the _normalizer class."""
        res = self._normalizer.normalize(word)
        if res["word_categories"]:
            self.is_a_proper_noun = "Names" in res["word_categories"]
            self.is_noise = "Noise" in res["word_categories"]
            self.is_a_number = "Numbers" in res["word_categories"]
            self.is_a_url = "URLs" in res["word_categories"]
            self.is_a_hashtag = "Hashtags" in res["word_categories"]
            self.is_a_filename = "Filenames" in res["word_categories"]
            self.is_foreign = "Foreign" in res["word_categories"]
            self.is_misspelled = "Misspellings" in res["word_categories"]
            if not res["lemmas"]:
                res["lemmas"] = []
            if len(res["lemmas"]) == 1 and res["lemmas"][0] == \
                    self.original_spelling:
                self.is_a_lemma = True
            else:
                self.is_a_lemma = False
            self.lemmas = res["lemmas"]
            if res["pos"]:
                self.pos = res["pos"]
            else:
                self.pos = ["unclear"]


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
        self.roots = res["roots"]
        self.suffixes = res["suffixes"]
        self.prefixes = res["prefixes"]
        self.related_words = res["related_words"]
        self.deriv_other = res["other"]

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
            self.semantics = res

    def all_info(self):
        """Pretty printing all the attributes of the word object."""
        for i in inspect.getmembers(self):
            if not i[0].startswith('_'):
                if not inspect.ismethod(i[1]):
                    print(i[0], ": ", i[1])
