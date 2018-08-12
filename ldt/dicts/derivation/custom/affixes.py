# -*- coding: utf-8 -*-
""" This module provides interface for the productive morphological patterns
in LDT.

The current functionality includes loading of language-specific resources
(prefixes, suffixes, etc):

    Todo:

        * check what happens when lists in yaml are empty
        * implement replacements in compounds (prazdnoshatayushchijsya) and
            joining symbols (German "s")
        * replace simple dictionary checks with lemmatization checks


"""

import os
import ruamel.yaml as yaml


from ldt.dicts.base.custom.en import BaseCustomDict as BaseCustomDict
from ldt.load_config import config as config
from ldt.helpers.formatting import rreplace as rreplace
from ldt.helpers.formatting import dash_suffix as dash_suffix
from ldt.helpers.formatting import _check_res as _check_res
from ldt.helpers.exceptions import ResourceError as ResourceError

#pylint: disable=too-many-instance-attributes
class Affixes(BaseCustomDict):
    """This class implements a generic interface for custom
    language-specific processig of productive affixes."""

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
        super(Affixes, self).__init__(language=language)

        self.dictionary = dictionary
        self.morph_dictionary = morph_dictionary

        self.equidistant_patterns = []

        # resources_path = "."+self.language+ ".yaml"
        dir_path = os.path.dirname(os.path.realpath(__file__))
        resources_path = os.path.join(dir_path, self.language+"/"+self.language+ ".yaml")
        # print(resources_path)
        if not os.path.isfile(resources_path):
            raise ResourceError(self.language+".yaml not found.")

        with open(resources_path) as stream:
            try:
                resources = yaml.safe_load(stream)
            except yaml.YAMLError:
                raise ResourceError("Something is wrong with the .yaml file "
                                    "for this language.")

            self.vowels = set(resources["vowels"])
            self.prefixes = resources["prefixes"]
            self.suffixes = resources["suffixes"]
            self.suffix_families = resources["suffix_families"]
            self.exceptions = resources["exceptions"]
            self.replacements_before_vowels = resources[
                "replacements_before_vowels"]
            self.replacements_before_consonants = resources[
                "replacements_before_consonants"]
            self.replacements_in_suffixes = resources[
                "replacements_in_suffixes"]
            self.replacements_in_prefixes = resources[
                "replacements_in_prefixes"]
            self.insertions_before_vowels = resources[
                "insertions_before_vowels"]
            self.insertions_before_consonants = resources[
                "insertions_before_consonants"]

    def is_a_vowel(self, letter):
        """Returns True is the letter is a vowel

        Args:
            letter (str): the letter to check

        Returns:
            (bool): True if the letter is a vowel

        """
        if letter in self.vowels:
            return True
        return False

    def check_exceptions(self, word, res=None):

        """Method for retrieving derivational info that requires only simple
        lookup in in the `DerivationCustomDict.exceptions`.

        Args:
            word_ (str): the word to analyze
            res (dict): if present, this dictionary will be updated

        Returns:
            (dict): updated or newly created dictionary with derivational data

        """

        res = _check_res(res)

        if not self.equidistant_patterns:
            for affix in self.exceptions.keys():
                for key, value in self.exceptions[affix].items():
                    if key == word:
                        res["suffixes"].append(affix)
                        res["roots"].append(value)
        else:
            for affix in self.exceptions.keys():
                for key, value in self.exceptions[affix].items():
                    if key == word:
                        res["suffixes"].append(affix)
                        res["roots"].append(value)
                    elif affix in self.equidistant_patterns:
                        if value == word:
                            res["suffixes"].append(affix)
                            res["roots"].append(key)
        return res

    # def _check_res(self, res):
    #     """Helper for avoiding empty dictionary as function argument"""
    #     if not res:
    #         res = {
    #             "suffixes": [], "prefixes": [], "roots": [], "other": [],
    #             "original_word": []
    #         }
    #     return res

    def decompose_prefixes(self, word, res=None):

        """Basic checking a list of productive prefixes
        Args:
            word (str): a potential nonce-word
            res (dict): if present, this dictionary will be updated

        Returns:
            (dict): updated or newly created dictionary with derivational data

        """

        res = _check_res(res)

        for prefix in self.prefixes:
            if word.startswith(prefix):
                if word.startswith(prefix+"-") and len(word) > len(prefix)+1:
                    # if ldt.dict.noise.is_a_word(word[len(p) + 1:]):
                    if self.dictionary.is_a_word(word[len(prefix) + 1:]):
                        res["prefixes"].append(prefix + "-")
                        res["roots"].append(word[len(prefix) + 1:])
                else:
                    if len(word) > len(prefix) +2:
                        if self.dictionary.is_a_word(word[len(prefix):]):
                            res["prefixes"].append(prefix + "-")
                            res["roots"].append(word[len(prefix):])
        return res

    def _decompose_by_suffix_family(self, word, res=None):
        """Simple suffix replacements in the complex > simple direction

        Args:
            word (str): a potential nonce-word
            res (dict): if present, this dictionary will be updated

        Returns:
            (dict): updated or newly created dictionary with derivational data

        """
        res = _check_res(res)

        for key, value in self.suffix_families.items():
            key_suffix = key
            suffixes = value
            for suffix in suffixes:
                if word.endswith(suffix) and len(word[:-len(suffix)]) > 2:
                    candidate = word[:-len(suffix)]+key_suffix
                    if self.dictionary.is_a_word(candidate):
                        res["suffixes"].append(dash_suffix(suffix))
                        res["roots"].append(candidate)
        return res

    def _decompose_suffix_simple(self, word, res=None):
        """The most basic decomposition of suffixes: no change to the stem.

        Example:

                >>> test_dict._decompose_suffix_simple("kingdom")
                {'suffixes': ['-dom'], 'prefixes': [], 'roots': ['king'],
                'other': [], 'original_word': []}

        Args:
            word (str): a potential nonce-word
            res (dict): if present, this dictionary will be updated

        Returns:
            (dict): updated or newly created dictionary with derivational data

        """
        res = _check_res(res)

        for suffix in self.suffixes:

            if word.endswith(suffix) and len(word[:-len(suffix)]) > 2:

                candidate = word[:-len(suffix)]
                if self.dictionary.is_a_word(candidate):
                    res["suffixes"].append(dash_suffix(suffix))
                    res["roots"].append(candidate)
        return res

    def _decompose_suffix_doubling(self, word, res=None):
        """Decomposing vowel suffixes that led to doubling of the final
        consonant of the root.

        Example:

                >>> test_dict._decompose_suffix_doubling("kingdom")
                {'suffixes': ['-dom'], 'prefixes': [], 'roots': ['king'],
                'other': [], 'original_word': []}

        Args:
            word (str): a potential nonce-word
            res (dict): if present, this dictionary will be updated

        Returns:
            (dict): updated or newly created dictionary with derivational data

        """
        res = _check_res(res)

        for suffix in self.suffixes:

            if self.is_a_vowel(suffix[0]):
                if word.endswith(suffix) and len(word[:-len(suffix)]) > 2:
                    if word[-(len(suffix)+1)] == word[-(len(suffix)+2)]:
                        candidate = word[:-len(suffix)-1]
                        if self.dictionary.is_a_word(candidate):
                            res["suffixes"].append(dash_suffix(suffix))
                            res["suffixes"].append(suffix)
                            res["roots"].append(candidate)
        return res

    def _decompose_suffix_replacements(self, word, res=None):
        """Decomposing suffixes with phonetic changes before vocalic or
        consonantal suffixes.

        Example:

                >>> test_dict._decompose_suffix_replacements("happily")
                {'suffixes': ['-ly'], 'prefixes': [], 'roots': ['happy'],
                'other': [], 'original_word': []}

        Args:
            word (str): a potential nonce-word
            res (dict): if present, this dictionary will be updated

        Returns:
            (dict): updated or newly created dictionary with derivational data

        """
        res = _check_res(res)

        for suffix in self.suffixes:

            if word.endswith(suffix) and len(word[:-len(suffix)]) > 2:

                if self.is_a_vowel(suffix[0]):
                    replacements = self.replacements_before_vowels
                else:
                    replacements = self.replacements_before_consonants

                for pair in replacements:

                    if word.endswith(pair[1]+suffix):
                        candidate = rreplace(word.strip(suffix), pair[1],
                                             pair[0])
                        if self.dictionary.is_a_word(candidate):
                            res["suffixes"].append(dash_suffix(suffix))
                            res["roots"].append(candidate)
            # else:
        return res

    def _decompose_suffix_insertions(self, word, res=None):
        """Decomposing suffixes with insertions before vocalic or consonantal
        suffixes.

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

            if word.endswith(suffix) and len(word[:-len(suffix)]) > 2:

                if self.is_a_vowel(suffix[0]):
                    insertions = self.insertions_before_vowels
                else:
                    insertions = self.insertions_before_consonants

                for insert in insertions:

                    candidate = word[:-len(suffix)] + insert
                    if self.dictionary.is_a_word(candidate):
                        res["suffixes"].append(dash_suffix(suffix))
                        res["roots"].append(candidate)
        return res

    def _decompose_suffix_blend(self, word, res=None):
        """Decomposing suffixes with replacements (typically due to the
        blending of identical sounds at the affix border).

        Example:

                >>> test_dict._decompose_suffix_e("historic")
                {'suffixes': ['-ic'], 'prefixes': [], 'roots': ['history'],
                'other': [], 'original_word': []}

        Args:
            word (str): a potential nonce-word
            res (dict): if present, this dictionary will be updated

        Returns:
            (dict): updated or newly created dictionary with derivational data

        """
        res = _check_res(res)

        for suffix in self.suffixes:

            if word.endswith(suffix) and len(word[:-len(suffix)]) > 2:

                for pair in self.replacements_in_suffixes:
                    if suffix[0] == pair[1]:

                        candidate = word.strip(suffix)+pair[0]
                        if self.dictionary.is_a_word(candidate):
                            res["suffixes"].append(dash_suffix(suffix))
                            res["roots"].append(candidate)
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

        The basic abstract class just includes the simple suffix
        addition. Override this method with any combination of the above for
        your language.

        Example:

                >>> test_dict.decompose_suffixes("kingdom")
                {'suffixes': ['-dom'], 'prefixes': [], 'roots': ['king'],
                'other': [], 'original_word': []}

        Args:
            word (str): a potential nonce-word
            res (dict): if present, this dictionary will be updated

        Returns:
            (dict): updated or newly created dictionary with derivational data

        """
        res = _check_res(res)
        res = self._decompose_suffix_simple(word, res)
        # res = self._decompose_suffix_doubling(word, res)
        # res = self._decompose_suffix_replacements(word, res)
        # res = self._decompose_suffix_insertions(word, res)
        # res = self._decompose_suffix_blend(word, res)
        return res

    def analyze_affixes(self, word, depth=2):
        """Combining the analysis of prefixes, suffixes and exceptions.

        Example:
            >>> test_dict.decompose_affixes("anti-intellectual")
            {'suffixes': ['-ual'], 'prefixes': ['anti-'],
             'roots': ['intellect', 'intellectual'], 'other': [],
             'original_word': ['anti-intellectual']}

        Args:
            word (str): a potential nonce-word
            depth (int): how many passes of analysis to make

        Returns:
            (dict): updated or newly created dictionary with derivational data
        """
        res = _check_res(res=None)
        res["original_word"] = [word]
        # start the list of stems to process

        processed_stems = set()
        stems_to_process = [word]
        if "-" in word:
            stems_to_process.append(word.replace("-", ""))

        processed_r = set()
        processed_p = set()
        processed_s = set()

        to_process = [k for k in stems_to_process if not k in processed_stems]

        for counter in range(10):

            subword = to_process[counter]

            if not subword in processed_r:
                processed_r.add(subword)
                res = self.check_exceptions(subword, res)
                to_process = to_process + \
                             [i for i in res["roots"] if not i in to_process]

            if not subword in processed_p:
                processed_p.add(subword)
                res = self.decompose_prefixes(subword, res)
                to_process = to_process + \
                             [i for i in res["roots"] if not i in to_process]

            if not subword in processed_s:
                processed_s.add(subword)
                res = self.decompose_suffixes(subword, res)
                to_process = to_process + \
                             [i for i in res["roots"] if not i in to_process]

            processed_stems.add(subword)
            if counter == depth or counter == len(to_process)-1:
                for key in res:
                    res[key] = list(set(res[key]))
                return res
