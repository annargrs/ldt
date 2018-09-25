# -*- coding: utf-8 -*-
""" This module provides interface for splitting compound words and/or
possible misspellings in LDT.

    Todo:

        * options for choosing the best analysis by sem similarity, ngrams
            and frequency

"""
import os
import ruamel.yaml as yaml

from ldt.dicts.base.custom.en import BaseCustomDict
from ldt.load_config import config
from ldt.helpers.formatting import rreplace
from ldt.helpers.formatting import _check_res
from ldt.helpers.exceptions import ResourceError


class Compounds(BaseCustomDict):
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
        super(Compounds, self).__init__(language=language)

        self.dictionary = dictionary
        self.morph_dictionary = morph_dictionary

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

            self.replacements_in_compounds = resources[
                "replacements_in_compounds"]
            self.insertions_in_compounds = resources[
                "insertions_in_compounds"]

    def split_on_dash(self, word, res=None):
        """Splitting dashed compounds, attempting to lemmatize all the parts

        Example:
            >>> test_dict.split_on_dash("god-knows-what")
            {'suffixes': [], 'prefixes': [], 'roots': ['god', 'know', 'what'],
            'other': [], 'original_word': 'god-knows-what'}

        Args:
            word (str): a potential nonce-word

        Returns:
            (dict): updated or newly created dictionary with derivational data
        """

        if not res:
            res = _check_res(res)

        if not "-" in word:
            return res

        else:

            words = word.split("-")
            checked = []
            for subword in words:
                lemmas = self.morph_dictionary.lemmatize(subword)
                if lemmas:
                    checked += lemmas
                else:
                    if self.dictionary.is_a_word(subword):
                        checked.append(subword)
        if len(checked) >= len(words):
            res["roots"] += checked
            res["original_word"] = word
        return res


    def _in_vocab(self, word):
        """Returning a normalized version of a root: lemmatization, regular
        insertions and replacements (if any are defined for a language).

        Args:
            word (str): the word to split

        Returns:
            (str): a normalized word found in dictionaries, or *False* if none
                can be found
        """

        lemmas = self.morph_dictionary.lemmatize(word)
        for lemma in lemmas:
            if self.dictionary.is_a_word(lemma):
                return lemma

        if self.dictionary.is_a_word(word):
            return word

        for insertion in self.insertions_in_compounds:
            candidate = word.rstrip(insertion)
            if self.dictionary.is_a_word(candidate):
                return candidate

        for replacement in self.replacements_in_compounds:
            candidate = rreplace(word, replacement[1], replacement[0])
            if self.dictionary.is_a_word(candidate):
                return candidate
        return False

    def split_compound(self, word, min_length=3, filtering="min_split_3"):

        """ Recursive splitting of compounds, with lemmatization and optional
        language-specific replacement and insertion patterns (see
        :meth:`_in_vocab`). By default filters out analyses with overly
        short subwords, and does not handle short words.

        Example:
            >>> print(split_compound("tomcat", min_length=3))
            [['tom', 'cat']]

        Args:
            word (str): the word to analyze
            min_length (int): do not attempt to break up words shorter than that.
            filter (str): what filtering function to use.

                * *min_split_length*: reject analyses that contain over 50%
                  items shorter than the final number in the parameter
                  (e.g. min_split_2)

        Todo:

            * if lemmatized word form is found, discard the ending
              ("tortoiseshell" > "tortoises + hell"

        Returns:
            (list): list of lists of stems, one per an alternative analysis

        """

        if len(word) < min_length:
            return [[word]]

        def build_stem_tree(compound):
            """Helper for building the tree-like dictionary structure with
                all possible splits of the word

            Args:
                compound (str): the word to analyze

            Returns:
                (dict): nested dictionaries with keys for split nodes

            Todo:
                * filtering by frequency
                * filtering by embedding similarity
                * filtering by ngrams

            """

            if not isinstance(compound, dict):
                res = {compound + " ": {}}
            for i in res:
                for k in range(1, len(i)):
                    if self._in_vocab(i[:k]) and i[:k] != i:
                        res[i][i[:k]] = build_stem_tree(i[k:].strip())
            return res

        tree = build_stem_tree(word)

        lists = []
        #pylint: disable=dangerous-default-value
        def tree_traverse_iter(tree, prefix=[]):
            """Helper for flattening the dictionary tree structure into a
            list of lists with all possible splits"""
            for key in tree:
                if tree[key] == {}:
                    lists.append(prefix + [key])
                else:
                    tree_traverse_iter(tree[key], prefix + [key])

        tree_traverse_iter(tree)
        cleaned = []
        for i in range(len(lists)):
            cleaned_list = [lists[i][ind] for ind in range(len(lists[i])) if
                            int(ind/2) != ind/2]
            cleaned.insert(i, cleaned_list)

        cleaned = [i for i in cleaned if i != [word]]

        if filtering:
            if filtering.startswith("min_split"):
                min_length = int(filtering.strip("min_split_"))
                cleaned = filter_by_min_length(cleaned, min_length)

        return cleaned


    def decompose_compound(self, word, res=None, split_known_words=True):

        """ Combined analysis of compounds: dashed words and recursive
        splitting, with lemmatization and optional language-specific
        replacement and insertion patterns (see :meth:`_in_vocab`).

        Example:
            >>> test_dict.split_on_dash("god-knows-what")
            {'suffixes': [], 'prefixes': [], 'roots': ['god', 'know', 'what'],
            'other': [], 'original_word': 'god-knows-what'}

        Args:
            word (str): the word to analyze

        Returns:
            (dict): updated or newly created dictionary with derivational data

        """

        res = _check_res(res)

        if "-" in word:
            return self.split_on_dash(word, res)

        if len(word) < 6:
            return res

        if not split_known_words:
            lemmas = self.morph_dictionary.lemmatize(word)
            for lemma in lemmas:
                if self.dictionary.is_a_word(lemma):
                    res["original_word"] = word
                    return res

        splits = self.split_compound(word)
        if splits:
            for split in splits:
                res["roots"] += split
        return res


def filter_by_min_length(splits, min_length, threshold=0.1):
    """Filtering out those compound analyses that contain over a
    threshold ratio of words over specified length.

        Example:
            >>> splits = [['t', 'o', 'm', 'c', 'a', 't'],\
                          ['t', 'o', 'm', 'c', 'at'],\
                          ["tom", "cat"]]
            >>> print(filter_by_min_length(splits, min_length=3))
            [['tom', 'cat']]

    Args:
        splits (list): list of lists
        min_length (int): the minimum length of words in an acceptable
            analysis
        threshold: the acceptable ratio of short to longer words in the
            analysis

    Returns:
        (list): filtered list of analyses
    """
    filtered = []
    for split in splits:
        too_short = [w for w in split if len(w) < min_length]
        score = len(too_short)/len(split)
        if score < threshold:
            filtered.append(split)
    return filtered
