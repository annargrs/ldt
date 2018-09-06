# -*- coding: utf-8 -*-
""" This module provides the base interface for the BabelNet API (v5).

    BabelNet key is required. Register at https://babelnet.org/register

    There are daily usage limits for free users (up to 1000 queries per day
    by default, can be extended to 50,000 for academic users by request).
    Commercial version also available.

    The current functionality includes:

     - Basic retrieval of urllib queries, given a set of arguments;
     - Determining whether a word entry exists;
     - Automatically formatting the dictionary language argument as required.
     - counting the number of queries performed in this session
     - retrieving BabelNet nodes and edges;

    Todo:

     - cache saved between sessions;
     - authorization error for babelnet on invalid key;
     - querying offline dump of BabelNet.

"""

import urllib
import urllib.request
import json
import gzip
import functools
from ldt.dicts.dictionary import Dictionary as Dictionary
from ldt.helpers.resources import lookup_language_by_code as \
    lookup_language_by_code
# from ldt.config import lowercasing as config_lowercasing
# from ldt.config import language as config_language
# from ldt.config import split_mwu as config_split_mwu
from ldt.load_config import config as config
from ldt.helpers.exceptions import AuthorizationError as AuthorizationError
# from ldt.helpers.exceptions import DictError as DictError

class BaseBabelNet(Dictionary):
    """The class providing the base BabelNet interface.

    Note:
        The language argument used for BabelNet API is in 2-letter-code
        format, capitalized. LDT assumes the letter codes are the same as
        `2-letter codes used in Wiktionary
        <https://en.wiktionary.org/wiki/Wiktionary:List_of_languages>`_.
        LDT provides on-the-fly conversion as needed.

    Todo:
        * the exceptions on daily limit exceeded & invalid key

    """
    def __init__(self, babelnet_key=config["babelnet_key"], **kw): #pylint:
    # disable=unused-argument
        """ Initializing the BabelNet class.

        Unlike the basic Dictionary class, BabelNet checks the language
        argument upon initialization and converts it to the 2-letter code if
        necessary. Exception is raised if the BabelNet key is not supplied.

        Args:
            babelnet_key (str): the BabelNet user key (registration at
            `BabelNet <https://babelnet.org/register>`_)

        """
        super(BaseBabelNet, self).__init__()
        self.queries = 0
        if len(self.language) > 2:
            self.language = lookup_language_by_code(self.language, reverse=True)
        self._language = self.language.upper()
        if babelnet_key:
            if babelnet_key != "None":
                self.babelnet_key = babelnet_key
            else:
                raise AuthorizationError("Please provide a BabelNet key. If you "
                                         "don't have one, register at "
                                         "https://babelnet.org/register ")

    def _set_language(self, language):
        """This method ensures the language arg is a 2-letter code."""
        if len(language) > 2:
            language = lookup_language_by_code(language, reverse=True)
        self._language = language.upper()


    def is_a_word(self, word):
        """Determining whether an entry exists in the resource.

        While Wiktionary module can rely on an internal cache of page titles to
        determine whether an entry exists without performing the full query,
        that is not possible for BabelNet. So this method actually just
        wraps the :meth:`get_ids` method for consistency, and should not be
        used to first determine whether a word is worth querying. However,
        extra pings should be saved with the cache mechanism.

        Args:
            word (str): the word to look up

        Returns:
            (bool): True if the word entry was found.

        """

        if self.get_ids(word):
            return True
        return False

    @functools.lru_cache(maxsize=None)
    def query(self, url):
        """Helper method for querying BabelNet

        Args:
            url (str): the url from which data should be retrieved

        Returns:
            (dict): the data loaded from the retrieved json representation

        """

        request = urllib.request.Request(url)
        request.add_header('Accept-encoding', 'gzip')
        # print(request.get_full_url())
        try:
            response = urllib.request.urlopen(request)
            self.queries += 1
        except urllib.error.HTTPError:
            print("Cannot reach BabelNet")
            return None

        if response.info().get('Content-Encoding') == 'gzip':
            gz_data = gzip.decompress(response.read()).decode('utf-8')
            data = json.loads(gz_data)
            return data

    @functools.lru_cache(maxsize=None)
    def get_ids(self, word, full=False):
        """Returns the list of BabelNet IDS for a given word

        Args:
            word (str): the word to look up

        Returns:
            (list): a list of BabelNet ids of the 'bn:00516031n' format
        """

        service_url = 'https://babelnet.io/v5/getSynsetIds'
        res = []
        params = {'lemma': word, 'searchLang': self.language,
                  'key': self.babelnet_key}
        url = service_url + '?' + urllib.parse.urlencode(params)

        data = self.query(url)
        if full:
            return data
        for result in data:
            res.append(result["id"])
        return res

    @functools.lru_cache(maxsize=None)
    def get_lemmas(self, babelnet_id):
        """ Getting lemmas associated with a babelnet_id.

        Args:
            babelnet_id (str): the id to lookup (e.g. 'bn:00516031n')

        Returns:
            (list): the list of BabelNet's "simple lemmas" associated with
            the queried id

        """

        res = {}
        service_url = 'https://babelnet.io/v5/getSynset'
        params = {'id': babelnet_id, 'searchLang': self.language,
                  'key': self.babelnet_key}
        url = service_url + '?' + urllib.parse.urlencode(params)
        data = self.query(url)

        senses = data.get("senses")
        res = []
        for sense in senses:
            if sense["properties"]["language"] == self.language:
                res.append(sense["properties"]["simpleLemma"])
        # if self.lowercasing:
        #     res = [w.lower() for w in res]
        #     #todo mwu
        res = list(set(res))
        res = self.post_process(res)
        return res

    @functools.lru_cache(maxsize=None)
    def get_edges(self, babelnet_id):
        """ Getting babelnet_ids related to the given babelnet_id.

        Args:
            babelnet_id (str): the id to lookup (e.g. 'bn:00516031n')

        Returns:
            (dict): the dictionary of babelnet ids categorized by relation to
            the queried id ("other", "hypernyms", "hyponyms", "meronyms",
            "holonyms", "synonyms", "antonyms" are supported)

        """
        # returns a dict of ids: list of [types/relation_groups] of words the
        #  target bnet_id is related to
        res = {}
        service_url = 'https://babelnet.io/v5/getOutgoingEdges'
        params = {'id': babelnet_id, 'searchLang': self.language,
                  'key': self.babelnet_key}
        url = service_url + '?' + urllib.parse.urlencode(params)
        data = self.query(url)

        res = {"other": [], "hypernyms": [], "hyponyms": [], "meronyms": [],
               "holonyms": [], "synonyms": [], "antonyms": []}
        #do synonyms work that way?
        for result in data:
            if self.language == result["language"]:
                pointer = result['pointer']
                relation = pointer.get('name').lower()
                group = pointer.get('relationGroup').lower()
                target = result.get('target')
                for rel in res:
                    if group.startswith(rel[:-1]):
                        res[rel].append(target)
                        # retrieve lemma instead
                    if relation.startswith(rel[:-1]):
                        res[rel].append(target)
        return res
