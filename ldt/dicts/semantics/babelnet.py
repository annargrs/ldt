# -*- coding: utf-8 -*-
""" This module provides interface for the BabelNet API (v5).

    BabelNet key is required (register at https://babelnet.org/register).
    There are daily usage limits for free users (up to 1000 queries per day
    by default, can be extended to 50, 000 for academic users by request).
    Commercial version also available.

    The way BabelNet API works, only ids for nodes related to query word,
    and edges per one node can be obtained in one request. This makes
    retrieval of all words related to the target word an expensive operation,
    as lemmas for all related ids have to be queried individually. We recommend
    to use WordNet/Wiktionary for the entries that they do contain,
    and fall back on BabelNet as last resort.

    Also, while BabelNet is much larger than any other resource,
    its aggregated nature makes its internal organization less reliable; in
    particular, relation categories have been inconsistent in our experience.

    The current functionality includes aggregating all relations from all
    senses by type.

    Todo:

        mwu splitting functionality, ensure lowercasing

"""

from ldt.dicts.semantics.lex_dictionary import LexicographicDictionary
from ldt.dicts.base.babelnet import BaseBabelNet
from ldt.load_config import config

class BabelNet(BaseBabelNet, LexicographicDictionary):
    """The class providing BabelNet interface for semantic relations.

    Note:
        The language argument used for BabelNet API is in 2-letter-code
        format, capitalized. LDT assumes the letter codes are the same as
        `2-letter codes used in Wiktionary
        <https://en.wiktionary.org/wiki/Wiktionary:List_of_languages>`_.
        LDT provides on-the-fly conversion as needed.

    """

    # pylint: disable=unused-argument
    def __init__(self, language=config["default_language"],
                 lowercasing=config["lowercasing"],
                 babelnet_key=config["babelnet_key"]):
        """ Initializing the BabelNet class.

        Unlike the basic Dictionary class, BabelNet checks the language
        argument upon initialization and converts it to the 2-letter code if
        necessary. Exception is raised if the BabelNet key is not supplied.

        Args:
            language (str): the language of the dictionary (automatically
            formatted to uppercase 2-letter code)
            lowercasing (bool): *True* if all data should be lowercased
            queries (int): the number of queries to BabelNet performed in
            this session
            babelnet_key (str): the BabelNet user key (registration at
            `BabelNet <https://babelnet.org/register>`_)

        """
        super(BabelNet, self).__init__(language=language,
                                       lowercasing=lowercasing,
                                       babelnet_key=babelnet_key)
        # self.queries = 0
        # if len(language) > 2:
        #     language = lookup_language_by_code(language, reverse=True)
        # self._language = language.upper()
        # if config_babelnet_key:
        #     self.babelnet_key = config_babelnet_key
        # else:
        #     raise AuthorizationError("Please provide a BabelNet key. If you "
        #                              "don't have one, register at "
        #                              "https://babelnet.org/register ")
        self.supported_relations = ("hypernyms", "hyponyms", "meronyms",
                                    "holonyms", "synonyms", "antonyms", "other")

    # def _set_language(self, language):
    #     """This method ensures the language arg is a 2-letter code."""
    #     if len(language) > 2:
    #         language = lookup_language_by_code(language, reverse=True)
    #     self._language = language.upper()


    # def is_a_word(self, word):
    #     """Determining whether an entry exists in the resource.
    #
    #     While Wiktionary module can rely on an internal cache of page titles to
    #     determine whether an entry exists without performing the full query,
    #     that is not possible for BabelNet. So this method actually just
    #     wraps the :meth:`get_ids` method for consistency, and should not be
    #     used to first determine whether a word is worth querying. However,
    #     extra pings should be saved with the cache mechanism.
    #
    #     Args:
    #         word (str): the word to look up
    #
    #     Returns:
    #         (bool): True if the word entry was found.
    #
    #     """
    #
    #     if self.get_ids(word):
    #         return True
    #     return False

    # def query(self, url):
    #     """Helper method for querying BabelNet
    #
    #     Args:
    #         url (str): the url from which data should be retrieved
    #
    #     Returns:
    #         (dict): the data loaded from the retrieved json representation
    #
    #     """
    #
    #     request = urllib.request.Request(url)
    #     request.add_header('Accept-encoding', 'gzip')
    #     # print(request.get_full_url())
    #     try:
    #         response = urllib.request.urlopen(request)
    #         self.queries += 1
    #     except urllib.error.HTTPError:
    #         print("Cannot reach BabelNet")
    #         return None
    #
    #     if response.info().get('Content-Encoding') == 'gzip':
    #         gz_data = gzip.decompress(response.read()).decode('utf-8')
    #         data = json.loads(gz_data)
    #         return data

    #pylint: disable=arguments-differ
    def get_relations(self, word, relations, reduce=False):
        """Getting babelnet_id for the target word, and then retrieving lemmas
        for every related babelnet_id.

        Args:
            word (str): the word to look up
            reduce (bool): an optional parameter to be passed to
                :meth:`LexicographicDictionary.check_relations`, which would
                reduce the number of queried relations to only those
                requested. Highly recommended for users without high BabelNet
                usage quotas.
            relations (tuple): the list of relations to which the query should
                be limited. Supported values:

                 * "other",
                 * "hypernyms",
                 * "hyponyms",
                 * "meronyms",
                 * "holonyms",
                 * "synonyms",
                 * "antonyms" .

        Returns:
            (dict): a dictionary with relations as keys and lists of ids of
            concepts as values
        """

        relations = self.check_relations(relations, reduce)

        res = {}
#686
        ids = self.get_ids(word)
        # print(ids)
        for babel_id in ids:
            # print(babelnet_id)
            edges = self.get_edges(babel_id)
#            print(edges)
            if edges:
                for relation in edges:
                    if relation in relations and relation not in res.keys():
                        res[relation] = []
                for relation in res:
                    for babelnet_id in edges[relation]:
                        lemmas = self.get_lemmas(babelnet_id)
                        if lemmas:
                            res[relation] += lemmas

        for relation in relations:
            res[relation] = self.post_process(res[relation])
        return res

#todo babelnet synonyms - just lemmas for each id of a queried word?
