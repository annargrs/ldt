# -*- coding: utf-8 -*-
""" This module brings together multiple resources for either:

 * confirming that a word is found in what resources;
 * confirming that the word is of a category that excludes its being in
   resources (e.g. it is a proper noun, a foreign word or a number);
 * attempting to lemmatize by productive rules;
 * attempting to normalize the hyphenation and tokenization errors;
 * attempting to

Examples:
    >>> test_dict = ldt.dicts.normalize.Normalization(language="English",
                                              order=("wordnet", "wiktionary"),
                                              custom_base="wiktionary")
    >>> test_dict.normalize("grammar")
    {'found_in': ['wordnet'], 'lemmas': ['grammar'], 'word_categories': [
    'Lexicon'], 'pos': ['noun']}
    >>> test_dict.normalize("grammars")
    {'found_in': ['wordnet'], 'lemmas': ['grammar'], 'word_categories': [
    'Lexicon'], 'pos': ['noun']}
    >>> test_dict.normalize("grammarxyz")
    None
    >>> test_dict.normalize("alice")
    {'lemmas': ['alice'], 'word_categories': ['Names'], 'pos': ['noun']}
    >>> test_dict.normalize("grammaire")
     {'word_categories': ['Foreign']}
    >>> test_dict.normalize("gramar")
    {'found_in': ['wordnet'], 'lemmas': ['grammar'], 'word_categories': [
    'Misspellings'], 'pos': ['noun']}
    >>> test_dict.normalize("%grammar")
    {'found_in': ['wordnet'], 'lemmas': ['grammar'], 'word_categories': [
    'Misspellings'], 'pos': ['noun']}
    >>> test_dict.normalize("grammar.com")
    {'word_categories': ['URLs'], 'pos': ['noun']}
    >>> test_dict.normalize("grammar.jpg")
    {'word_categories': ['Filenames'], 'pos': ['noun']}
    >>> test_dict.normalize("gram-mar")
    {'found_in': ['wordnet'], 'lemmas': ['grammar'], 'word_categories': [
    'Misspellings'], 'pos': ['noun']}
    >>> test_dict.normalize("grammar.lexicon")
    {'found_in': ['wordnet'], 'lemmas': ['grammar', "lexicon],
    'word_categories': ['Misspellings'], 'pos': ['noun']}
    >>> test_dict.normalize("grammarlexicon")
    {'found_in': ['wordnet'], 'lemmas': ['grammar', "lexicon],
    'word_categories': ['Misspellings'], 'pos': ['noun']}

Todo:
    * check the checking of foreign words against wiktionary output
    * binding spellcheckers and wordnets by languages
    * creation of default config file upon installation
    * the right error path in NLTK tokenizer
    * add .citation property, and print it out on initialization
        WordNet 1.5, NLTK implementation. Use .citation to get the full
        citation for this resource.
"""

import functools

from ldt.dicts.morphology.meta import MorphMetaDict
from ldt.dicts.resources import NumberDictionary
from ldt.dicts.resources import NameDictionary
from ldt.dicts.resources import WebDictionary
from ldt.dicts.resources import FileDictionary
from ldt.dicts.spellcheck.en.en import SpellcheckerEn as Spellchecker
from ldt.dicts.derivation.custom.compounds import Compounds
from ldt.dicts.morphology.wordnet.en import MorphWordNet

from ldt.load_config import config



def contains_a_letter(word):
    """Helper for :meth:`analyze`"""
    for char in word:
        if char.isalpha():
            return True
    return False

def contains_non_letters(word):
    """Helper for :meth:`analyze`"""
    for char in word:
        if not char.isalpha():
            if not char in ["'", "-"]:
                return True
    return False

@functools.lru_cache(maxsize=config["cache_size"])
def denoise(word):
    """Remove non-alpha symbols, if any."""
    trash = []
    for char in list(word):
        if not char.isalnum():
            trash.append(char)
    for char in trash:
        word = word.strip(char)
    if not contains_non_letters(word):
        return word
    else:
        #if something in the middle of the word, like gr#eef
        for char in trash:
            if char not in ["-", "'"]:
                word = word.replace(char, "")
    return word


def turn_to_words(word):
    """Split on non-alphanumeric characters, if any."""
    res = []
    subword = ""
    for char in list(word):
        if char.isalnum():
            subword = subword + char
        else:
            if subword:
                res.append(subword)
            subword = ""
    res.append(subword)
    return res

class Normalization(MorphMetaDict):
    """The _normalizer class brings together many ldt resources for
    fixing frequent tokenization and spelling problems in the word
    embeddings vocabulary."""

    def __init__(self, language=config["default_language"],
                 lowercasing=config["lowercasing"], order=("wordnet",
                                                           "wiktionary"),
                 custom_base="wiktionary"):
        """ Initializing the _normalizer class.

        Args:
            language (str): the query language
            lowercasing (bool): whether all input should be lowercased
            order (tuple of str): the resources that should be used to check the
              existence of an entry, in that order

        """

        super(Normalization, self).__init__(language=language,
                                            lowercasing=lowercasing,
                                            order=order)
        #: ldt names dictionary object
        self.namedict = NameDictionary(language=language, lowercasing=lowercasing)
        #: ldt number object
        self.numberdict = NumberDictionary(language=language, lowercasing=lowercasing)
        #: ldt web dictionary object
        self.webdict = WebDictionary(lowercasing=lowercasing)
        #: ldt filename dictionary object
        self.filedict = FileDictionary(lowercasing=lowercasing)
        #: ldt spelldictionary dictionary object
        self.spelldict = Spellchecker()

        morph_dict = MorphWordNet()
        #: ldt compound splitter object
        self.splitter = Compounds(dictionary=self.wordnet,
                                  morph_dictionary=morph_dict)

    def _noise(self, word):
        """Handling the cases where the input doesn't contain any letters.

        Args:
            word (str): the word to check.

        Returns:
            (dict): word category labels and found lemmas, if any.
        """
        res = {}
        if word.isnumeric():
            res["word_categories"] = ["Numbers"]
            res["pos"] = ["numeral"]
        else:
            res["word_categories"] = ["Noise"]
        return res

    def _resources(self, word):
        """Handling the cases where the input is contains something
        non-alphanumeric and belongs to some unanalyzable category like
        filenames, or punctuation it can be split on.

        Args:
            word (str): the word to check.

        Returns:
            (dict): word category labels and found lemmas, if any.
        """
        res = {}

        if self.numberdict.is_a_word(word):
            res["word_categories"] = ["Numbers"]
            res["pos"] = ["numeral"]
        elif self.webdict.is_a_word(word):
            res["word_categories"] = ["URLs"]
            res["pos"] = ["noun"]
        elif self.filedict.is_a_word(word):
            res["word_categories"] = ["Filenames"]
            res["pos"] = ["noun"]
        elif word.startswith("#"):
            attempt = self.is_a_word(word.strip("#"))
            if attempt:
                res["word_categories"] = ["Hashtags"]
                res["found_in"] = attempt
                res["lemmas"] = self.lemmatize(word.strip("#"))
                res["pos"] = self.get_pos(word.strip("#"), minimal=True)
        else:
            res = self._subwords(word)
        if res:
            return res



    def _subwords(self, word):
        """Handling the cases where the input doesn't contain any letters.

        Args:
            word (str): the word to check.

        Note:
            The _normalizer class should include at least wiktionary in the
            dictionary order option to be able to handle articles,
            prepositions etc. that are erroneously appended to a word (e.g.
            "cats.and"), as they are not included in WordNet.

        Returns:
            (dict): word category labels and found lemmas, if any.
        """
        # need at least wiktionary to handle "cat.and"
        subwords = turn_to_words(word)
        if len(subwords) > 1:
            res = {}
            res["lemmas"] = []
            res["found_in"] = []
            res["word_categories"] = ["Misspellings"]
            res["pos"] = []
            for subword in subwords:
                lemmas = self.lemmatize(subword)
                if not lemmas:
                    return None
                else:
                    res["lemmas"] += lemmas
                    res["found_in"] += self.is_a_word(subword, minimal=True)
                    res["pos"] += self.get_pos(lemmas[0])
            # if len(res["found_in"]) == len(subwords):
            res["lemmas"] = list(set(res["lemmas"]))
            res["found_in"] = list(set(res["found_in"]))
            res["pos"] = list(set(res["pos"]))
            return res

    def _word(self, word):
        """Handling the cases where the input doesn't contain any
        non-letter characters: straightforward lemmatization, name detection,
        correction of frequent misspellings.

        Args:
            word (str): the word to check.

        Returns:
            (dict): word category labels and found lemmas, if any.
        """
        res = {"word_categories": []}

        num = self.numberdict.is_a_word(word)
        if num:
            res["word_categories"].append("Numbers")
            res["lemmas"] = [word]
            res["pos"] = ["numeral"]

        attempt = self.is_a_word(word)
        if attempt:
            res["found_in"] = attempt
            res["lemmas"] = self.lemmatize(word)
            res["word_categories"].append("Lexicon")
            res["pos"] = self.get_pos(word, minimal=True)
        if self.namedict.is_a_word(word):
            res["word_categories"].append("ProperNouns")
            res["lemmas"] = [word]
            res["pos"] = ["noun"]
        if not res["word_categories"]:
            if self.spelldict.is_foreign(word):
                res["word_categories"].append("ForeignWords")

        if not res["word_categories"]:
            misspelled = self.spelldict.spelling_nazi(word)
            if misspelled:
                lemmas = self.lemmatize(misspelled)
                if lemmas:
                    res["found_in"] = self.is_a_word(lemmas[0])
                    res["lemmas"] = lemmas
                    res["word_categories"] = ["Misspellings"]
                    res["pos"] = self.get_pos(lemmas[0])

        return res

    def _fix(self, word):
        """Cleaning up the cases where noise symbols can be removed (*"%cat*).

        Args:
            word (str): the word to check.

        Returns:
            (dict): word category labels and found lemmas, if any.
        """
        res = {}
        #denoising
        attempt = denoise(word)
        if attempt != word:
            lemmas = self.lemmatize(attempt)
            if lemmas:
                res["lemmas"] = lemmas
                res["found_in"] = self.is_a_word(lemmas[0])
                res["word_categories"] = ["Misspellings"]
                res["pos"] = self.get_pos(lemmas[0])
            if res:
                return res


    def _dash(self, word):
        """Cleaning up the cases where the word is erroneously hyphenated.

        Args:
            word (str): the word to check.

        Returns:
            (dict): word category labels and found lemmas, if any.
        """
        res = {}
        dashes = ["―", "—", "–", "-", "‒"]
        for dash in dashes:
            if dash in word:
                attempt = word.replace(dash, "")
                dicts = self.is_a_word(attempt)
                if dicts:
                    res["found_in"] = dicts
                    res["lemmas"] = [attempt]
                    res["word_categories"] = ["Misspellings"]
                    res["pos"] = self.get_pos(attempt)
                    return res

    def _unspaced(self, word):
        """Cleaning up the cases where the word is erroneously joined.

        Args:
            word (str): the word to check.

        Todo:
           * the min split length parameter to be settable in the _normalizer
           dictionary

        Returns:
            (dict): word category labels and found lemmas, if any.
        """
        res = {"word_categories": ["Misspellings"], "lemmas":[], "pos":[]}
        splits = self.splitter.split_compound(word, filtering="min_split_4")
        if splits:
            for split in splits:
                for subword in split:
                    dicts = self.is_a_word(subword)
                    if dicts:
                        res["found_in"] = dicts
                        res["lemmas"].append(subword)
                        res["pos"] += self.get_pos(subword)
        res["pos"] = list(set(res["pos"]))
        return res

    def normalize(self, word):
        """The main _normalizer function bringing together all functonality.

        Args:
            word (str): the word to check.

        Returns:
            (dict): word category labels and found lemmas, if any.
        """
        word = str(word)
        if not contains_a_letter(word):
        # the word contains nothing to analyze
            res = self._noise(word)
            if res:
                return res
        res = self._dash(word)
        if res:
            return res

        if contains_non_letters(word):
            # URLs, filenames, numbers etc
            res = self._resources(word)
            if res:
                return res

        # the word is correctly spelled and is in dict, is a name or a
        # foreign word
        else:
            res = self._word(word)
            if res["word_categories"]:
                return res
            else:
                res = self._unspaced(word)
                if res["lemmas"]:
                    return res

        # # the word has to be modified
        res = self._fix(word)
        if res:
            if res["lemmas"]:
                return res
        # give up
        else:
            return {"word_categories": "Missing"}
