# -*- coding: utf-8 -*-
""" Lexicographic Dictionary classes

This module implements the base Lexicographic dictionary class that is
inherited by classes for resources from which semantic relations can be
obtained. There is also a separate DictionaryWithDefinitions class for
resources which also provide lists of definitions and examples per word sense.

Basic functionality required in any subclass:

    * retrieve the list of word with the specified relation;
    * retrieve a dictionary with specified relations as values and lists of
      related words as values

Todo:
    * creation of default config file upon installation
    * the right error path in NLTK tokenizer
"""

# import abc
from abc import ABCMeta, abstractmethod
from nltk.tokenize import word_tokenize

from ldt.dicts.dictionary import Dictionary as Dictionary
from ldt.helpers.exceptions import DictError as DictError
from ldt.helpers.resources import load_stopwords as load_stopwords
from ldt.helpers.resources import lookup_language as lookup_language
from ldt.helpers.formatting import get_spacing_variants as get_spacing_variants
from ldt.helpers.formatting import remove_text_inside_brackets as \
    remove_text_inside_brackets
#from ldt.config import path_to_resources as config_path_to_resources
# from ldt.config import lowercasing as config_lowercasing
# from ldt.config import language as config_language
# from ldt.config import split_mwu as config_split_mwu

# class LexicographicDictionary(Dictionary, metaclass=ABCMeta):
class LexicographicDictionary(Dictionary, metaclass=ABCMeta):
    """A super-class for resources with relations functionality

    """
    def __init__(self, **kw):
    # def __init__(self, lowercasing=config_lowercasing,
    #              split_mwu=config_split_mwu):
        """ Initializing the base class.

        Args:
            lowercasing (bool): *True* if all data should be lowercased
            split_mwu (bool): *True* if in addition to underscored
                spellings of multi-word expressions their dashed and spaced
                versions should also be produced (e.g. 'good night',
                'good_night', "good-night")

        """

        super(LexicographicDictionary, self).__init__()
        self.main_relations = ("synonyms", "antonyms", "hyponyms",
                               "hypernyms", "meronyms")
        self.supported_relations = self.main_relations

    def check_relation(self, relation):
        """Helper method for :meth:`get_relation`. Checks if relations are
        supported by a given resource.

        Args:
            relations (str): the particular relation to check

        Returns:
            (str): the verified relation

        Raises:
            DictError: the requested relation are not supported

        """

        if relation not in self.supported_relations:
            raise DictError("Unknown relation. The supported relations are: " +
                            ", ".join(self.supported_relations))
        return relation

    def check_relations(self, relations, reduce=False):
        """Helper method for :meth:`get_relations`. Checks if relations are
        supported by a given resource.

        Args:
            reduce (bool): if *True*, and unknown relation is encountered,
                the requested list is reduced to the available relations.
                Otherwise DictError arises.
            relations (tuple or string):

               * the particular relations to check,
               * "main" for a predefined list of main relations (synonyms,
                  antonyms, meronyms, hyponyms, hypernyms)
               * "all" for all supported relations

        Returns:
            (tuple): the verified relations

        Raises:
            DictError: the requested relations are not supported
        """

        if isinstance(relations, tuple):
            if not reduce:
                for i in relations:
                    if not i in self.supported_relations:
                        raise DictError("Unknown relation. The supported "
                                        "relations are: " +
                                        ", ".join(self.supported_relations))
            else:
                filtered_rels = [i for i in relations if i in
                                 self.supported_relations]
                relations = tuple(filtered_rels)

        elif isinstance(relations, str):
            if relations == "main":
                relations = self.main_relations
            elif relations == "all":
                relations = self.supported_relations
            elif "nyms" in relations:
                if reduce:
                    try:
                        relations = (self.check_relation(relations),)
                    except DictError:
                        return None
                else:
                    relations = (relations,)
        return relations

    def get_relation(self, word, relation):
        """Wrapper for :meth:`get_relations` for one-relation use.

        Some resources like WordNet have detailed interfaces for different
        relations, while others (including BabelNet and Wiktionary) have
        a single interface for them all. This method can be simply inherited
        for the second type of resources, and overridden in the first type case.

        Args:
            word (str): the word to be looked up
            relation (str): the relation to look up

        Returns:
            (list): the list of words related to the target word with the
            specified relation
        """

        relation = self.check_relation(relation)
        res = self.get_relations(word, (relation))
        if relation in res:
            return res[relation]
        else:
            return []


    @abstractmethod
    def get_relations(self, word, relations):
        """Stub for the compulsory method for all subclasses that
        returns the specified list of relations for the given word.

        Args:
            word (str): the word to be looked up
            relations (tuple, string): the relations to look up

        Returns:
            (dict): dictionary with relations as keys and lists of words as
            values
        """
        pass

    def post_process(self, wordlist):
        """Helper for processing the wordlists from different resources
        according to general config presets.

        At the moment, the results can be automatically:

          * lowercased (``self.lowercasing = True``);
          * multi-word expressions can be split and added in all spacing
                variations (``split_mwu = True``);

        Args:
            wordlist: the list of words to process

        Returns:
            (list): post-processed list of words

        Todo:
            * partial matches
            * spacing for underscored words?
        """

        if self.lowercasing:
            wordlist = [w.lower() for w in wordlist]

        if self.split_mwu:
            newres = []
            for mwu in wordlist:
                newres += get_spacing_variants(mwu)
            wordlist = newres
        wordlist = list(set(wordlist))
        return wordlist

# class DictionaryWithDefinitions(LexicographicDictionary, metaclass=ABCMeta):
class DictionaryWithDefinitions(LexicographicDictionary, metaclass=ABCMeta):
    """A super-class for resources with definition functionality

    """

    # def __init__(self, lowercasing=config_lowercasing,
    #              split_mwu=config_split_mwu):
    def __init__(self):
        """ Initializing the base class.

        Args:
            lowercasing (bool): *True* if all data should be lowercased
            split_mwu (bool): *True* if in addition to underscored
                spellings of multi-word expressions their dashed and spaced
                versions should also be produced (e.g. 'good night',
                'good_night', "good-night")

        """

        super(DictionaryWithDefinitions, self).__init__()

    # def is_a_word(self, word):
    #     """Stub for the compulsory method for all subclasses that
    #     determines the existence of an entry.
    #
    #     Args:
    #         word (str): the word to be looked up
    #
    #     Returns:
    #         (bool): whether the target word has an entry in the resource
    #     """
    #     raise NotImplementedError()
    #     # pass

    def get_relations(self, word, relations):
        """Stub for the compulsory method for all subclasses that
        returns the specified list of relations for the given word.

        Args:
            word (str): the word to be looked up
            relations (tuple, string): the relations to look up

        Returns:
            (dict): dictionary with relations as keys and lists of words as
            values
        """
        raise NotImplementedError()

    @abstractmethod
    def get_definitions(self, word, remove_notes=True):
        """Stub for the compulsory method for all subclasses of
        DictionaryWithDefinitions that returns a sense inventory for the
        given word.

        Args:
            word (str): the word to be looked up
            remove_notes (bool): if *True*, attempts to remove the
                lexicographic notes such as *(obsolete)* from the definition

        Returns:
            (dict): dictionary with sense numbers as keys and
            subdictionaries with "def" and "ex" as values
        """
        raise NotImplementedError()

    def get_words_in_definitions(self, word, stopwords=False,
                                 remove_notes=True, examples="add"):

        """

        A method returning a list of words found in all definitions
        and/or examples of the target word

        Args:

            word (str or dict): word to be queried for defintions, or a sense
                inventory dictionary returned by the :meth:`get_definitions`
                in the dictionaries that support it (WordNet, Wiktionary).
            remove_notes (bool): if *True*, attempts to remove the lexicographic
                notes such as *(obsolete)* from the definition
            stopwords (bool): if *True*, the words in NLTK stopword lists for
                the given language (if it exists) are filtered out
            examples (str): Possible values:

              * **add**: words in both examples and definitions are
                collected;
              * **only**: the words in definitions are ignored;
              * **ignore**: only words in definitions are returned.

        Returns:
            (list): a list of words in definitions of the target word,
            with or without examples and/or stopwords
        """

        if isinstance(word, str):
            defs = self.get_definitions(word, remove_notes)
        elif isinstance(word, dict) and 1 in word.keys():
            defs = word

        text = ""

        for i in defs.keys():
            if "def" in defs[i].keys() and examples != "only":
                text += " "+defs[i]["def"]
            if "ex" in defs[i].keys():
                if examples == "add" or examples == "only":
                    text += " " + " ".join(defs[i]["ex"])

        text = text.replace("  ", " ")
        if remove_notes:
            text = remove_text_inside_brackets(text)
        # words = text.split()

        if len(self.language) == 2:
            nltk_language = lookup_language(self.language).lower()
        else:
            nltk_language = self.language.lower()
        # try:
        words = word_tokenize(text, language=nltk_language)

        # except LookupError("No NLTK tokenizer for "+nltk_language):
        # problem: TypeError: catching classes that do not inherit from BaseException is not allowed
        if isinstance(words, str):
            words = words.split()
        words = list(set(words))

        if stopwords:
            stopwordlist = set(load_stopwords(nltk_language))
            words = [w for w in words if not w in stopwordlist]

        #todo add cleanup individual words

        return words

# poses
# lemmatization
# retrieving word forms

#
#
# def get_words_in_definitions(word, stopwords=False, lowercasing=
#                                         lowercasing,
#                                         remove_notes=True, examples = "add"):
#     '''
#
#     A function returning a list of words found in all WN definitions and/or
#  examples of the target word
#
#     Args:
#
#         word (str): the word to look up
#         lowercasing (Bool): if not set, the global config variable is used.
#         True (default) lowercases all vocab.
#         remove_notes (bool): if True, attempts to remove the
#         lexicographic notes such as (obsolete) from the definition
#         stopwords (bool): if True, the words in NLTK stopword lists for
# English are filtered out
#         examples (str): if "add", words in both examples and definitions
# are collected. if "only", the words in definitions are ignored,
#         if "ignore", only words in definitions are returned.
#
#     Returns:
#         (list): a list of words in WordNet definitions in the target word,
#         with or without examples and/or stopwords
#
#     '''
#
#     defs = get_definitions(word, remove_notes=remove_notes, lowercasing=lowercasing)
# #
# #     text = ""
# #
# #     for i in defs.keys():
# #         if "def" in defs[i].keys() and examples != "only":
# #             text += " "+defs[i]["def"]
# #         if "ex" in defs[i].keys():
# #             if examples == "add" or examples == "only":
# #                 text += " " + defs[i]["ex"]
# #
# #     text = text.replace("  ", " ")
# #     words = text.split()
# #     words = list(set(words))
# #
# #     if stopwords:
# #         stopWords = ldt.resources.load_stopwords(language)
# #         words = [w for w in words if not w in stopWords]
# #
# #     #todo add cleanup individual words
# #
# #     return words
# #
# # #res = list(set(res))