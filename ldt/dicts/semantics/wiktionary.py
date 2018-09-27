# -*- coding: utf-8 -*-
""" This module provides interface for lexicographic data of Wiktionary.

    The current functionality includes:

     - Aggregating all relations from all senses by type;
     - Retrieving individual relations data

    Todo:
        * language-specific tokenizers in :meth:`get_relations`.
"""

import functools

from ldt.dicts.semantics.lex_dictionary import LexicographicDictionary
from ldt.dicts.base.wiktionary import BaseWiktionary
from ldt.helpers.formatting import remove_text_inside_brackets
from ldt.helpers.formatting import strip_non_alphabetical_characters
from ldt.load_config import config


class Wiktionary(BaseWiktionary, LexicographicDictionary):
    """The class providing Wiktionary interface for parsing lexicographic
    relations.

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
                 lowercasing=config["lowercasing"]):
        """ Initializing the Wiktionary class.

        Unlike the basic Dictionary class, Wiktionary checks the language
        argument upon initialization and converts it to the 2-letter code if
        necessary. A None cache is also initialized.

        Args:
            cache (bool): *True* if lists of entries for a given
            language should be cached to speed up queries
            language (str): the language of the dictionary
            lowercasing (bool): True if all data should be lowercased

        """

        super(Wiktionary, self).__init__(cache=cache, language=language,
                                         lowercasing=lowercasing)

        self.supported_relations = ("synonyms", "antonyms", "hyponyms",
                                    "hypernyms", "meronyms", "holonyms",
                                    "troponyms", "coordinate terms", "other",
                                    "derived terms")


    @functools.lru_cache(maxsize=config["cache_size"])
    def get_relations(self, word, relations="all",
                      reduce=False): #pylint: disable=arguments-differ

        """Parsing lexicographic relations in Wiktionary.

        Optionally adds partial matches as entries. For example, if a word
        list contains *hot dog*, both *hot* and *dog* will also be included.
        This could make sense for evaluating models that haven't done any MWU
        preprocessing.

        Args:
            word (str, list): the word to look up, or a WiktionaryParser object.

        Returns:
            (dict): a dictionary with relation types as keys and lists of
            words as values

        Todo:

            * The text and examples fields sometimes have unaccounted
            synonyms as "Synonym: " or "Synonyms: "
            * Preserve colons in translations

        """
        if not relations:
            relations = self.supported_relations
        else:
            relations = self.check_relations(relations, reduce)

        if isinstance(word, str):
            word = self.query(word)

        if word:
            dicts = _get_relations_full(word)
            for i in dicts:
                cleaned = []
                for wrd in dicts[i]:

                    if "(" in wrd:
                        wrd = remove_text_inside_brackets(wrd)
                    wrd = wrd.strip(":")
                    wrd = wrd.strip()
                    wrd = wrd.strip(",")
                    wrd = wrd.split(",")
                    for mwu in wrd:
                        mwu = strip_non_alphabetical_characters(mwu,
                                                                ignore=("-",
                                                                        " "))
                        # print(mwu)
                        mwu = mwu.strip()
                        for see in ["see", "see also", "See", "See also"]:
                            if mwu.startswith(see):
                                mwu = mwu.replace(see, "")
                        if not " " in mwu:
                            cleaned.append(mwu)

                        else:
                            mwu = mwu.strip()
                            cleaned.append(mwu)
                cleaned = list(set(cleaned))
                cleaned = sorted(cleaned)
                dicts[i] = []
                for wrd in cleaned:
                    if len(wrd) > 1 and not "thesaurus" in wrd:
                        dicts[i].append(wrd)
            for relation in dicts:
                dicts[relation] = self.post_process(dicts[relation])
            for i in ["{{ws beginlist}}", "{{ws endlist}}'"]:
                for rel in dicts:
                    if dicts[rel]:
                        if i in dicts[rel]:
                            dicts[rel].remove(i)

            new_res = {k: v for k, v in dicts.items() if k in relations}

            return new_res


# def dig_deeper(input, field, res):
#     """A helper function for :func:`get_wiktionary_field_strings`.
#     It recursively locates string-only fields.
#
#     Args:
#         word (str): the word to look up
#         field (str): the field to look up:
#             * "etymology"
#             * "partOfSpeech"
#
#     Returns:
#         (set): the string data for the corresponding field
#     """
#     if isinstance(input, dict):
#         for key, val in input.items():
#             if field == key:
#                 if input[key]:
#                     if isinstance(input[key], str):
#                         res.add(input[key].strip("\n"))
#                         return res
#
#             elif isinstance(val, list):
#                 for i in val:
#                     res = dig_deeper(val , field , res)
#
#     elif isinstance(input, list):
#         for i in input:
#             res = dig_deeper(i, field, res)
#     return res


def dig_deeper(entry, field, res, depth=10):
    """A helper function for :func:`get_wiktionary_field_strings`.
    It recursively locates the target field.

    Args:
        entry (dict or list): the entity to investigate
        field (str): the field to look up
        res (list): the list of found entities to update
        depth (integer): maximum recursion depth (otherwise this does blow up
            memory for some entries like "cat")

    Returns:
        (list): the updated list of found entities
    """
    if depth > 0:
        if isinstance(entry, dict):
            for key, val in entry.items():
                if field == key:
                    if entry[key]:
                        # if isinstance(entry[key], str):
                        res.append(entry[key])
                        return res

                elif isinstance(val, list):
                    for i in val:
                        depth -= 1
                        res = dig_deeper(val, field, res, depth)

        elif isinstance(entry, list):
            for i in entry:
                depth -= 1
                res = dig_deeper(i, field, res, depth)
        return res
    else:
        return res

def get_wiktionary_field_strings(word, field):
    """A helper function for locating string-only fields

    Args:
        word (str): the word to look up
        field (str): the field to look up. The possible values include:

             - "etymology"
             - "partOfSpeech"

    Todo:
        move to morphology or derivation sections

    Returns:
        (set): the string data for the corresponding field
    """
    res = set()
    test_dict = Wiktionary()
    word = test_dict.query(word)
    print(word)
    for sense in word:
        res = dig_deeper(sense, field, res)
    return res

def _get_relations_tuples(entry):
    """Helper for :func:`_get_relations_full`.

    Args:
        entry (dict): the dictionary to check for the relation types

    Returns:
        (tuple): (relationshipType, [list of words])

    """

    if isinstance(entry, dict):
        if 'relationshipType' in entry.keys() and 'words' in entry.keys():
            return (entry['relationshipType'], entry["words"])


def _get_relations_full(word):
    """Helper for :func:`get_relations`.

    Args:
        word (list): wikidata object

    Returns:
        (dict): a dictionary with all lists of words assembled per relation type
    """

    #flatten the crazy structure of the output
    res = dig_deeper(word, "relatedWords", res=[])
    flattened = []
    for i in res:
        if len(i) == 1:
            flattened.append(_get_relations_tuples(i[0]))
        else:
            for subdict in i:
                flattened.append(_get_relations_tuples(subdict))

    # assemble all relations
    rel_dict = {}
    for i in flattened:
        if not i[0] in rel_dict.keys():
            rel_dict[i[0]] = i[1]
        else:
            rel_dict[i[0]] += i[1]
    return rel_dict

# if __name__ == '__main__':
#     d = Wiktionary()
#     print(d.get_relations("cat"))
