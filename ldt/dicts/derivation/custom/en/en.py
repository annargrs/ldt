# -*- coding: utf-8 -*-
"""
This module provides interface for the productive morphological patterns.

The current functionality includes:

* Methods for identifying roots and productive affixes
* Lookup from the dictionary of exceptions

Examples:

    >>> test_dict = ldt.dicts.derivation.custom.en.EnglishDerivation()
    >>> test_dict.analyze_affixes("kindness")
    {'original_word': ['kindness'], 'other': [], 'prefixes': [], 'roots': [
    'kind'], 'suffixes': ['-ness']}
    >>> test_dict.analyze_affixes("antiestablishment")
    {'original_word': ['antiestablishment'], 'other': [], 'prefixes': [
    'anti-'], 'roots': ['establishment', 'establish'], 'suffixes': ['-ment']}
    >>> test_dict.analyze_affixes("bleed")
    'original_word': ['bleed'], 'other': ['root_vowel_n/a>v'], 'prefixes': [
    ], 'roots': ['blood', 'bleed'], 'suffixes': []}
    >>> test_dict.decompose_compound("toothpaste")
    {'original_word': [], 'other': [], 'prefixes': [], 'roots': ['tooth',
    'paste'], 'suffixes': []}

Todo:

    * Error on non-english language of the dictionary

"""

from ldt.dicts.base.wordnet.en import BaseWordNet

from ldt.dicts.derivation.custom.custom_dict import DerivationCustomDict
from ldt.helpers.formatting import dash_suffix
from ldt.helpers.formatting import _check_res
from ldt.dicts.morphology.wordnet.en import MorphWordNet

class EnglishDerivation(DerivationCustomDict):
    """This class implements an interface for retrievning POS
    information from NLTK WordNet and lemmatization."""

    def __init__(self, dictionary=None, morph_dictionary=None, language="en"):
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

        super(EnglishDerivation, self).__init__(language=language)
        if dictionary:
            self.dictionary = dictionary
        else:
            self.dictionary = BaseWordNet()
        if morph_dictionary:
            self.morph_dictionary = morph_dictionary
        else:
            self.morph_dictionary = MorphWordNet()
        self.equidistant_patterns = ("root_vowel_n/a>v", "root_vowel_v>v")

    def _suffix_sion(self, word, res=None):
        """ Custom processing of -sion suffix, which has several idiosyncratic
        patterns and exceptions.

        Example:

                >>> test_dict._suffix_sion("corrosion")
                {'suffixes': ['-sion'], 'prefixes': [], 'roots': ['corrode'],
                'other': [], 'original_word': []}

        Args:
            word (str): a potential nonce-word
            res (dict): if present, this dictionary will be updated

        Returns:
            (dict): updated or newly created dictionary with derivational data

        """

        res = _check_res(res)

        if word in ["mission", "passion", "session", "pension"]:
            return res

        if word.endswith("ssion"):
            if self.dictionary.is_a_word(word[:-3]):
                return word[:-3]
            else:
                endings = ["d", "t", "de", "se"]
                for end in endings:
                    for i in [word[:-4] + end, word[:-5] + end]:
                        if self.dictionary.is_a_word(i):
                            res["suffixes"].append("-sion")
                            res["roots"].append(i)
        elif word.endswith("sion"):
            endings = ["d", "t", "de", "se"]
            for end in endings:
                for i in [word[:-3] + end, word[:-4] + end]:
                    if self.dictionary.is_a_word(i):
                        res["suffixes"].append("-sion")
                        res["roots"].append(i)
        return res

    def _decompose_language_specific_suffixes(self, word, res=None):
        """Binder for any language-specific affix patterns that may be
        required"""
        res = self._suffix_sion(word, res)
        return res

    def decompose_suffixes(self, word, res=None):
        """The basic method for decomposing words with suffixes.

        The language-specific lists of affixes and replacement patterns are
        provided as yaml files in the corresponding submodules of
        `ldt.dicts.derivation.custom`.

        The currently implemented patterns include:

            * simple appending of suffixes (kingdom > king + -dom)
                (:meth:`_decompose_suffix_simple`)
            * doubling of final consonants (stopper > stop + -er)
                (:meth:`_decompose_suffix_doubling`)
            * replacements before vocalic and consonantal suffixes (happily >
                happy + -ly) (:meth:`_decompose_suffix_replacements`)
            * insertions before vocalic and consonantal suffixes (imaginable >
                imagine + -able) (:meth:`_decompose_suffix_insertions`)
            * blending of the end of the stem with the beginning of the suffix
                (historic > history + -ic) (:meth:`_decompose_suffix_blend`)


        In addition to that, :meth:`_decompose_language_specific_suffixes`
        binds any additional language-specific methods, which will be
        processed before the above generic ones.

        Example:

                >>> test_dict.decompose_suffixes("historic")
                {'suffixes': ['-ic'], 'prefixes': [], 'roots': ['history'],
                'other': [], 'original_word': []}

        Args:
            word (str): a potential nonce-word
            res (dict): if present, this dictionary will be updated

        Returns:
            (dict): updated or newly created dictionary with derivational data

        """
        res = _check_res(res)
        res = self._decompose_language_specific_suffixes(word, res)
        res = self._decompose_suffix_simple(word, res)
        res = self._decompose_suffix_doubling(word, res)
        res = self._decompose_suffix_replacements(word, res)
        res = self._decompose_suffix_insertions(word, res)
        res = self._decompose_suffix_blend(word, res)

        return res

    def _decompose_suffix_e(self, word, res=None):
        """Decomposing consonant suffixes before which final "e" was dropped.

        Example:

                >>> test_dict._decompose_suffix_e("imaginable")
                {'suffixes': ['-able'], 'prefixes': [], 'roots': ['imagine'],
                'other': [], 'original_word': []}

        Args:
            word (str): a potential nonce-word
            res (dict): if present, this dictionary will be updated

        Returns:
            (dict): updated or newly created dictionary with derivational data

        """
        res = _check_res(res)

        for suffix in self.suffixes:

            if word.endswith(suffix) and self.is_a_vowel(suffix[0]):

                candidate = word[:-len(suffix)] + "e"
                if self.dictionary.is_a_word(candidate):
                    res["suffixes"].append(dash_suffix(suffix))
                    res["roots"].append(candidate)
        return res