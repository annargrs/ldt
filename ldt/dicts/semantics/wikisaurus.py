# -*- coding: utf-8 -*-
""" This module provides interface for the Wiktionary thesaurus. It was
previously known as Wikisaurus; this is a cool name, so LDT kept it.

    The current functionality includes:

     - Retrieving Wiktionary Thesaurus Data with Wiktionary API;
     - Aggregating all relations types;
     - Determining whether a word entry exists;
     - Optionally caching the latest list of page titles for determining
       whether pages exist;
     - Automatically formatting the dictionary language argument as required.

    Todo:
        * language-specific tokenizers in :meth:`get_relations`.

"""

import urllib.request
import functools
import json


from ldt.helpers.resources import lookup_language_by_code as \
    lookup_language_by_code
from ldt.helpers.wiktionary_cache import load_wiktionary_cache as \
    load_wiktionary_cache
from ldt.dicts.semantics.lex_dictionary import LexicographicDictionary as \
    LexicographicDictionary
from ldt.dicts.base.wiktionary import BaseWiktionary as BaseWiktionary
# from ldt.helpers.formatting import remove_text_inside_brackets as \
#     remove_text_inside_brackets
# from ldt.helpers.formatting import strip_non_alphabetical_characters as \
#     strip_non_alphabetical_characters
# from ldt.config import lowercasing as config_lowercasing
# from ldt.config import language as config_language
# from ldt.config import split_mwu as config_split_mwu
# from ldt.config import wiktionary_cache as config_wiktionary_cache
from ldt.load_config import config as config


class Wikisaurus(BaseWiktionary, LexicographicDictionary):
    """The class providing Wikisaurus interface with a custom API parser.

    It optionally uses a cached list of Wiktionary pages to reduce server
    load and speed  up analysis by only querying pages that actually exist
    for a given language (see :mod:`ldt.helpers.wiktionary_cache`). Since
    Wikisaurus is currently not a large resource (only 2000 synsets in
    English, as of writing), caching is highly recommended.

    Note:
        The language argument used for Wiktionary cache files and in Wiktionary
        API is in 2-letter-code format, while WiktinaryParser requires a
        `canonical language name
        <https://en.wiktionary.org/wiki/Wiktionary:List_of_languages>`_.
        LDT provides on-the-fly conversion as needed.

    Todo:

        * Definitions and examples

    """
    def __init__(self, cache=config["wiktionary_cache"],
                 language=config["default_language"],
                 lowercasing=config["lowercasing"],
                 split_mwu=config["split_mwu"]):
        """ Initializing the Wikisaurus class.

        Unlike the basic Dictionary class, Wikisaurus checks the language
        argument upon initialization and converts it to the 2-letter code if
        necessary. A None cache is also initialized.

        Args:
            language (str): the language of the dictionary
            lowercasing (bool): True if all data should be lowercased
            split_mwu (bool): True if in addition to underscored spellings of
            multi-word expressions their dashed and spaced versions should also
            be produced (e.g. 'good night', 'good_night', "good-night")

        """
        super(Wikisaurus, self).__init__(cache=cache, language=language,
                                         split_mwu=split_mwu)
    #     super(Wikisaurus, self).__init__()
    #     if len(language) > 2:
    #         language = lookup_language_by_code(language, reverse=True)
    #     self._language = language
    #     if not wiktionary_cache:
    #         self.cache = None
    #     else:
    #         self.load_cache()
    #     self.supported_relations = ("synonyms", "antonyms", "hyponyms",
    #                                 "hypernyms", "meronyms", "holonyms",
    #                                 "troponyms", "coordinate terms", "other")
    #
    #
    # def _set_language(self, language):
    #     """This method ensures the language arg is a 2-letter code."""
    #     if len(language) > 2:
    #         language = lookup_language_by_code(language, reverse=True)
    #     self._language = language
    #
    def load_cache(self):
        """Loading the cached list of titles of existing Wikisaurus pages.
        If it doesn't exist, this list is created in the ldt resources directory
        specified in the config file."""

        self.cache = load_wiktionary_cache(language=self._language,
                                           lowercasing=self.lowercasing,
                                           path_to_cache=config[
                                               "path_to_resources"],
                                           wikisaurus=True)

    def is_a_word(self, word):
        """ Determines whether a Wikisaurus entry exists for this word.

        If cache has been loaded, it is used to determine whether a word exists.
        Otherwise, Wikisaurus API is queried.

        Args:
            word (str): the input word to look up.

        Returns:
            (bool): True if the word entry was found.

        """
        if self.cache:
            if word in self.cache:
                return True
            return False
        else:
            if self.query(word):
                return True
            return False

    @functools.lru_cache(maxsize=None)
    def query(self, word):
        """Retrieving data from Wikisaurus API.

        Args:
            word (str): word to be queried.

        Returns (list):
            a list of Wikisaurus "revisions" data points

        Todo:
            Find the specific error that is thrown when too many
            requests are made in parallel.
        """

        wikisaurus_url = "https://" + self.language + \
                         '.wiktionary.org//w/api.php?format=json&action=query' \
                         '&prop=revisions&rvprop=content&titles=Thesaurus:'
        url = wikisaurus_url + word
        request = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(request).read()
        except urllib.error.URLError:
            return None
        if response:
            data = json.loads(response)
            data = data["query"]["pages"]
            rels = []

            for i in data.keys():
                try:
                    revisions = data[i]["revisions"]
                    for revision in revisions:
                        rels.append(revision["*"])
                    # rels += data[i]["revisions"]['*']  # , "\n\n")
                except KeyError:
                    pass
        return rels

    def _parse_wikisaurus_relations(self, wikidata):
        """Helper method for :meth:`get_relations`, returning wiki data
        per relation type

        Args:
            wikidata (list): list of wiktionary revisions datapoints,
            as returned by :meth:`query` method

        Returns:
            (dict): a dictionary of wiki data per relation type (unformatted)

        """

        res = {"Synonyms":[], "Hyponyms":[], "Hypernyms":[], "Holonyms":[],
               "Antonyms":[], "Meronyms":[], "Coordinate terms":[],
               "Various":[], "Related terns":[], "Derived terms":[],
               "See also":[]}

        wikisaurus_language = lookup_language_by_code(
            self.language).capitalize()

        for rel in wikidata:
            if wikisaurus_language in rel:
                rel = rel.split("==")
                # for i in range(len(rel)):
                for i in enumerate(rel):
                    i = i[0]
                    if rel[i]:
                        title = rel[i].strip("=")
                        if title in res:
                            for counter in range(len(rel)):
                                try:
                                    if "{{ws beginlist}}" in rel[i + counter]:
                                        res[title] = rel[i + counter]
                                        break
                                except IndexError:
                                    break
        for k in res:
            res[k.lower()] = res.pop(k)
        return res

    def _cleanup_wikisaurus(self, wikidata):

        for relation in wikidata.keys():
            if wikidata[relation] != []:
                splitted = wikidata[relation].split("\n")
                cleaned = []
                for i in splitted:
                    i = cleanup_wiki_string(i)
                    if i:
                        cleaned += [i]
                wikidata[relation] = cleaned
        for relation in wikidata:
            wikidata[relation] = self.post_process(wikidata[relation])
            # if not wikidata[relation]:
            #     wikidata[relation] = []
        return wikidata

    def get_relations(self, word, relations="all", reduce=False):
        """Retrieving relations from Wikisaurus entries

        Args:
            word (str): the word to be looked up
            relations (tuple, string): the relations to look up

        Returns:
            (dict): dictionary with relations as keys and lists of words as
            values
        """

        relations = self.check_relations(relations, reduce)

        word = self.query(word)
        res = self._parse_wikisaurus_relations(word)
        res = self._cleanup_wikisaurus(res)

        # for i in ["{{ws beginlist}}", "{{ws endlist}}'"]:
        #     for rel in res:
        #         if isinstance(res[rel], list):
        #             if i in res[rel]:
        #                 res[rel] = res[rel].remove(i)
        new_res = {k:v for k, v in res.items() if k in relations}
        for rel in new_res:
            if isinstance(new_res[rel], list):
                for i in ["{{ws beginlist}}", "{{ws endlist}}'"]:
                    if i in new_res[rel]:
                        new_res[rel].remove(i)
        return new_res


def cleanup_wiki_string(line):
    """Helper for :meth:`_cleanup_wikisaurus`

    Args:
        line (str): line to be cleaned up from wiki markup

    Returns:
        (str): cleaned up string

    """

    line = line.strip("=")
    line = line.lower()
    if line:
        if not "beginlist" in line and not "endlist" in line:
            line = line.replace("ws|", "")
            # {{ws|pedestrianize}} {{qualifier|dated}} cases
            if line.count("{{") > 1:
                line = line.split("{{")[1]
                line = line.strip()
            if "|" in line:
                line = line.split("|")[0]
            line = line.replace("}", "")
            line = line.replace("{", "")
            # still sometimes get things like ws ----
            if line.startswith("ws"):
                # will give False if there aren't any letters
                if line[2:].isupper() or line[2:].islower():
                    pass
    return line
