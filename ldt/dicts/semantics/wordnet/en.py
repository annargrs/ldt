# -*- coding: utf-8 -*-
""" This module provides interface for the NLTK's Princeton WordNet.

    The current functionality includes:

     - Retrieving lists of words related to the target word with a
       certain relation type;
     - Aggregating that info;
     - Protecting from timeouts in computing synsets closures;
     - Retrieving definition lists.

"""


import functools
import timeout_decorator

from nltk.corpus import wordnet as wn


from ldt.dicts.semantics.lex_dictionary import DictionaryWithDefinitions as \
    DictionaryWithDefinitions
from ldt.dicts.base.wordnet.en import BaseWordNet as BaseWordNet
from ldt.helpers.formatting import remove_text_inside_brackets as \
    remove_text_inside_brackets
from ldt.load_config import config as config


# class WordNet(DictionaryWithDefinitions, BaseWordNet):
class WordNet(BaseWordNet, DictionaryWithDefinitions):
    """The class providing the English WordNet interface.

    Since WordNets are language-specific, any further additions will have to
    implement similar classes for other languages.

    Todo:

        * Definitions and examples

    """

    def __init__(self, lowercasing=config["lowercasing"],
                 split_mwu=config["split_mwu"]):
        """ Initializing the WordNet class.

        Args:
            lowercasing (bool): *True* if all data should be lowercased
            split_mwu (bool): *True* if in addition to underscored spellings of
            multi-word expressions their dashed and spaced versions should also
            be produced (e.g. 'good night', 'good_night', "good-night")

        """
        super(WordNet, self).__init__(
            lowercasing=lowercasing, split_mwu=split_mwu)

        # DictionaryWithDefinitions.__init__(lowercasing, split_mwu)
        # BaseWordNet.__init__(lowercasing, split_mwu)
        # BaseWordNet.__init__(self)
        # DictionaryWithDefinitions.__init__(self)
        # super().__init__()

        # self._language = "en"
        self.supported_relations = ("synonyms", "antonyms", "hyponyms",
                                    "hypernyms", "part_meronyms",
                                    "member_meronyms", "substance_meronyms",
                                    "meronyms")

    # def _set_language(self, language):
    #     """This ensures the language is suppported."""
    #     if language not in ["English", "english", "en"]:
    #         raise LanguageError("Only English WordNet is supported at the "
    #                             "moment.")
    #     self._language = language
    #
    # def is_a_word(self, word):
    #     """ Determines whether a WordNet entry exists for this word.
    #
    #     Args:
    #         word (str): the input word to look up.
    #
    #     Returns:
    #         (bool): *True* if the word entry was found.
    #
    #     """
    #
    #     if wn.synsets(word):
    #         return True
    #     return False

    @functools.lru_cache(maxsize=None)
    def _get_all_synonyms(self, word):
        """A helper method for :func:`get_relation`

        Args:
            word (str): the word to be looked up

        Returns:
            list: a list of synonyms of this word in all of its meanings in
            WordNet.

        """
        if not self.is_a_word(word):
            return None
        res = []
        for synsets in wn.synsets(word):
            res += synsets.lemma_names()

        return list(set(res))

    @functools.lru_cache(maxsize=None)
    def _get_antonyms(self, word):
        """A helper method for :func:`get_relation`

        Args:
            word (str): the word to be looked up

        Returns:
            list: a list of antonyms of this word in all of its meanings in
            WordNet.

        """
        if not self.is_a_word(word):
            return None

        res = []
        for synset in wn.synsets(word):
            if word in synset.name():
                for lemma in synset.lemmas():
                    string = str(lemma).split(".")
                    if word in string[-1]:
                        for candidate in lemma.antonyms():
                            res.append(candidate.name())
        res = list(set(res))
        return res

    @functools.lru_cache(maxsize=None)
    def _get_all_antonyms(self, word):
        """ A helper method for :func:`get_relation`

        WordNet antonyms are not particularly rich. LDT crudely expands them
        with also including the antonyms of all the synonyms of the target word.

        Args:
            word (str): the word to be looked up

        Returns:
            list: a list of antonyms of all the synonyms of this word,
            in all of its meanings in WordNet.

        """
        if not self.is_a_word(word):
            return None
        res = []
        syns = self._get_all_synonyms(word)
        for token in syns:
            res = res + self._get_antonyms(token)
        res = res + self._get_antonyms(word)
        res = list(set(res))
        return res

    @timeout_decorator.timeout(10, use_signals=False)
    @functools.lru_cache(maxsize=None)
    def _get_nyms(self, word, relation, synonyms=True, depth=1):
        """ Single interface to all WordNet relations computed with
        closure (i.e. except synonyms and antonyms).

        Args:
            word (str): the word to be looked up
            synonyms (bool): if *True*, the list is expanded by querying the
                relations for all the synonyms of the target word.
            depth(int): the depth of WordNet closure
            relation (str): the relation to be looked up. Possible values:

                * hyponyms,
                * hypernyms,
                * meronyms,
                * part_meronyms,
                * member_meronyms,
                * substance_meronyms

        Returns:
            list: a list of words related to the target word in the specified
            way, optionally expanded through synonyms of the queried word.

        """

        if not self.is_a_word(word):
            return None
        if relation == "hyponyms":
            nyms = lambda s: s.hyponyms()
        elif relation == "hypernyms":
            nyms = lambda s: s.hypernyms()
        elif relation == "part_meronyms":
            nyms = lambda s: s.part_meronyms()
        elif relation == "substance_meronyms":
            nyms = lambda s: s.substance_meronyms()
        elif relation == "member_meronyms":
            nyms = lambda s: s.member_meronyms()
        elif relation == "meronyms":
            nyms = lambda \
                s: s.substance_meronyms() + s.member_meronyms() + \
                   s.part_meronyms()

        result = []
        for synsets in wn.synsets(word):
            res = list(synsets.closure(nyms, depth))
            sublist = []
            for synset in res:
                if not synonyms:
                    sublist.append(synset.lemma_names()[0])
                else:
                    for lemma in synset.lemma_names():
                        sublist.append(lemma)
                result += sublist

        return result

    # pylint: disable=arguments-differ
    @functools.lru_cache(maxsize=None)
    def get_relation(self, word, relation, synonyms=True): #pylint:
        # disable=arguments-differ
        """ Single interface to all WordNet relations

        A method that provides a list of words related to the target word
        with the specified lexicographic relation in WordNet.

        It wraps :func:`_get_nyms` that relies on closure for all relations
        (except synonyms and antonyms), enabling its use with timeout
        decorator. This prevents problems with timing out on potentially long
        closures in WordNet.

        Args:
            word (str): the word to be looked up
            synonyms (bool): if *True*, the list is expanded by querying the
              relations for all the synonyms of the target word.
            relation (str): the relation look up. Possible values:

                * antonyms,
                * synonyms,
                * hyponyms,
                * hypernyms,
                * meronyms,
                * part_meronyms,
                * member_meronyms,
                * substance_meronyms

        Returns:
            list: a list of words related to the target word in the specified
            way.

        Todo:
            * test split_mwu

        """
        if not self.is_a_word(word):
            return None

        relation = self.check_relation(relation)

        if relation == "synonyms":
            res = self._get_all_synonyms(word)
        elif relation == "antonyms":
            if synonyms:
                res = self._get_all_antonyms(word)
            else:
                res = self._get_antonyms(word)
        else:
            try:
                res = self._get_nyms(word, relation=relation, synonyms=synonyms)
            except timeout_decorator.timeout_decorator.TimeoutError:
                print("WordNet query timed out: ", word, relation)
                res = []
            except: # wn.WordNetError:
                return []

        res = list(set(res))
        res = self.post_process(res)
        return sorted(res)

    # pylint: disable=arguments-differ
    def get_relations(self, word, relations="all", reduce=False,
                      synonyms=True):

        """ Aggregating all wWrdNet relations found for a word in a single
        dictionary.

        Args:
            word (str): the word to be looked up
            relations (str, tuple): the relations to look up. Possible values:

             * "main" for synonyms, antonyms, hypernyms, hyponyms and meronyms,
             * "all" for meronyms subsplit into 3 groups.
             * tuples with any combination of relations can also be passed.

            synonyms (bool): if *True*, the list is expanded by also querying the
            relations for all the synonyms of the target word.

        Returns:
            (dict): a dictionary with relation types as keys and lists of
            words as values.

        """

        relations = self.check_relations(relations, reduce)

        # if relations == "main":
        #     relations = ("synonyms", "antonyms", "hyponymns", "hypernyms",
        #                  "meronyms")
        # elif relations == "all":
        #     relations = ("synonyms", "antonyms", "hyponymns", "hypernyms",
        #                  "part_meronyms", "member_meronyms",
        #                  "substance_meronyms")
        # elif relations and isinstance(relations, tuple):
        #     pass
        # else:
        #     raise DictError("The value for 'relations' argument should be "
        #                     "'main' (for the main relations), 'all' (for all "
        #                     "relations with meronym subcategories), "
        #                     "or a tuple of relations to look up.")
        res = {}
        if relations:
            for rel in relations:
                res[rel] = self.get_relation(word, relation=rel, synonyms=synonyms)
        return res


    @functools.lru_cache(maxsize=None)
    def get_definitions(self, word, remove_notes=True):
        """A simple wrapper for NLTK's Princeton wordnet definitions.

        Args:
            word (str): a word to look up
            remove_notes (bool): if *True*, attempts to remove the
            lexicographic notes such as (obsolete) from the definition

        Returns:
            (dict): a dictionary with the numbered keys corresponding to a
            word senses. For example: ``{1: {"def": "definition A", "ex": [
            "example 1", "example 2"]}}``
        """
        if not self.is_a_word(word):
            return None

        res = {}
        counter = 1
        for i in wn.synsets(word):
            res[counter] = {}
            if i.definition():
                res[counter]["def"] = i.definition()
            if i.examples():
                res[counter]["ex"] = i.examples()
            counter += 1

        for counter in res:
            keys = res[counter].keys()
            for subkey in keys:
                if isinstance(res[counter][subkey], str):
                    if self.lowercasing:
                        res[counter][subkey] = res[counter][subkey].lower()
                    if remove_notes:
                        res[counter][subkey] = remove_text_inside_brackets(
                            res[counter][subkey])
                elif isinstance(res[counter][subkey], list):
                    pass
        return res
