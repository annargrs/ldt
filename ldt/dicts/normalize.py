# -*- coding: utf-8 -*-
""" This module brings together multiple resources for either:

 * confirming that a word is found in resources;
 * confirming that the word is of a category that excludes its being in
   resources (e.g. it is a proper noun, a foreign word or a number);
 * attempting to lemmatize by productive rules;
 * attempting to normalize the spelling.

Examples:
    >>> test_dict.normalize("#cat")
    {is_standard: False, "lemmas": ["cat"], "word_categories": ["hashtag"],
    "found_in": ["WordNet"]}
    >>> test_dict.normalize("cat")
    {"lemmas": ["cat"], "word_categories": ["hashtag"]}

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

from ldt.dicts.dictionary import Dictionary as Dictionary
from ldt.dicts.morphology.meta import MorphMetaDict as MorphMetaDict
from ldt.dicts.resources import NumberDictionary as NumberDictionary
from ldt.dicts.resources import NameDictionary as NameDictionary
from ldt.dicts.resources import WebDictionary as WebDictionary
from ldt.dicts.resources import FileDictionary as FileDictionary
from ldt.dicts.spellcheck.en.en import SpellcheckerEn as Spellchecker

from ldt.load_config import config as config



def contains_a_letter(word):
    """Helper for :meth:`analyze`"""
    for char in word:
        if char.isalpha():
            return True
    return False

#%%
def contains_non_letters(word):
    """Helper for :meth:`analyze`"""
    for char in word:
        if not char.isalpha():
            if not char in ["'", "-"]:
                return True
    return False

#%%
def contains_splittable_chars(word):
    """Helper for :meth:`analyze`"""
    for char in word:
        if char in ["'", "-"]:
            return True
    return False

@functools.lru_cache(maxsize=None)
def denoise(word):
    '''
    Remove trash symbols, if any
    '''
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

# def hyphenation(word)
#     if "-" in word:
#         if not "-free" in word and not "-in" in word and not "-like" in word and not "-stricken" in word and not "-to-be" in word:
#             if check_in_dictionaries(word.replace("-","")):
#                 candidates.append(word.replace("-",""))
#             elif check_in_dictionaries(word.replace("-","_")):
#                 candidates.append(word.replace("-","_"))
#     if "_" in word:
#         if check_in_dictionaries(word.replace("_", "-")):
#             candidates.append(word.replace("_", "-"))
#     return candidates


class Normalization(MorphMetaDict):

    def __init__(self, language=config["default_language"],
                 lowercasing=config["lowercasing"], order=("wordnet",
                                                           "wiktionary",
                                                           "custom")):
        """ Initializing the base class.

        Args:
            language (str): the query language
            lowercasing (bool): whether all input should be lowercased

        """

        super(Normalization, self).__init__(language=language,
                                            lowercasing=lowercasing,
                                            order=order)
        # self.basedict = MorphMetaDict(order="wordnet", "babelnet")
        self.namedict = NameDictionary(language=language, lowercasing=lowercasing)
        self.numberdict = NumberDictionary(language=language, lowercasing=lowercasing)
        self.webdict = WebDictionary(lowercasing=lowercasing)
        self.filedict = FileDictionary(lowercasing=lowercasing)
        self.spelldict = Spellchecker()

    def _noise(self, word):
        res = {}
        if word.isnumeric():
            res["word_categories"] = ["Numbers"]
        else:
            res["word_categories"] = ["Noise"]
        return res

    def _resources(self, word):

        res = {}

        if self.numberdict.is_a_word(word):
            res["word_categories"] = ["Numbers"]
        if self.webdict.is_a_word(word):
            res["word_categories"] = ["URLs"]
        elif self.filedict.is_a_word(word):
            res["word_categories"] = ["Filenames"]
        if word.startswith("#"):
            attempt = self.is_a_word(word.strip("#"))
            if attempt:
                res["word_categories"] = ["Hashtags"]
                res["found_in"] = attempt
                res["lemmas"] = self.lemmatize(word.strip("#"))
        return res

    def _word(self, word):

        res = {}

        num = self.numberdict.is_a_word(word)
        if num:
            res["word_categories"] = ["Numbers"]

        attempt = self.is_a_word(word)
        if attempt:
            res["found_in"] = attempt
            res["lemmas"] = self.lemmatize(word)
        if self.namedict.is_a_word(word):
            res["word_categories"] = ["Names"]
            res["lemmas"] = [word]
        else:
            if self.spelldict.is_foreign(word):
                res["word_categories"] = ["Foreign"]
        return res

    def _fix(self, word):
        res = {}
        attempt = denoise(word)
        lemmas = self.lemmatize(attempt)
        if lemmas:
            res["lemmas"] = lemmas
        return res

    def normalize(self, word):

        word = str(word)

        res = {}
        while not res:

            if not contains_a_letter(word):
            # the word contains nothing to analyze
                res = self._noise(word)

            elif contains_non_letters(word):
            # URLs, filenames, numbers etc
                res = self._resources(word)

        # the word is correctly spelled and is in dict, is a name or a
        # foreign word
            else:
                res = self._word(word)

        # # the word has to be modified
        #     res = self._fix(word)
        return res


if __name__ == "__main__":
    d = Normalization()
    print(d.normalize("apt500"))