"""This module combining all derivational analysis functionality from various
resources.

Examples:

    >>> test_dict = ldt.dicts.derivation.analyze.DerivationAnalyzer()
    >>> test_dict._get_constituents("kindness")
    {'original_word': ['kindness'], 'other': [], 'prefixes': [], 'roots': [
    'kind'], 'suffixes': ['-ness']}
    >>> test_dict._get_related_words("kindness")
    ['first-of-its-kind', 'kinda', 'kindness', 'kindless', 'many-kinded',
    'kindly', 'kindliness', 'in kind', 'kindhearted', 'kindful', 'kind of']
    >>> test_dict.analyze("kindness")
    {'original_word': ['kindness'], 'other': [], 'prefixes': [],
    'related_words': ['kindhearted', 'kindly', 'in kind', 'kindliness', 'kinda',
    'many-kinded', 'first-of-its-kind', 'kind of', 'kindful', 'kindless'],
     'roots': ['kind'], 'suffixes': ['-ness']}

Note:
    Only English is fully supported for analysis of productive
    morphological patterns at the moment.

"""

from ldt.dicts.dictionary import Dictionary as Dictionary
from ldt.load_config import config as config
from ldt.dicts.derivation.wiktionary import DerivationWiktionary as \
    DerivationWiktionary
from ldt.dicts.derivation.wordnet.en import DerivationWordNet as \
    DerivationWordNet
from ldt.dicts.derivation.custom.en.en import EnglishDerivation as \
    EnglishDerivation
from ldt.helpers.resources import update_dict as update_dict

class DerivationAnalyzer(Dictionary):
    """DerivationAnalyzer class combines to all derivation analysis
    functionality in ldt.
    """
    # pylint: disable=unused-argument

    def __init__(self, language=config["default_language"],
                 lowercasing=config["lowercasing"]):

        super(DerivationAnalyzer, self).__init__(language=language,
                                                 lowercasing=lowercasing)
        if language in ["en", "english", "English"]:
            self.wordnet = DerivationWordNet()
            self.custom = EnglishDerivation()
        else:
            self.wordnet = None
            self.custom = None

        self.wiktionary = DerivationWiktionary(language=language)
    def is_a_word(self, word):
        return self.wiktionary.is_a_word(word)

    def _get_constituents(self, word):
        """Bringing together analysis of productive affixes and compounds.
        If that fails, Wiktionary etymologies are also looked up.

        Args:
            word (str): the word to look up

        Returns:
            (dict of str): the derivational analysis data.
        """
        res = {'original_word': [word], 'other': [], 'prefixes': [],
               'roots': [], 'suffixes': []}
        if self.custom:
            res = self.custom.analyze_affixes(word)
            if not res["roots"]:
                compounds = self.custom.decompose_compound(word)
                res = update_dict(res, compounds)
        if not res["roots"]:
            etym = self.wiktionary.get_etymologies(word)

            if etym:
                res["roots"] = etym[0]
                for affix in etym[1]:
                    if affix.startswith("-"):
                        res["suffixes"].append(affix)
                    elif affix.endswith("-"):
                        res["prefixes"].append(affix)
        return res

    def _get_related_words(self, word):
        """Bringing together derivationally related word families
        from Wiktionary and WordNet, where available.

        Args:
            word (str): the word to look up

        Returns:
            (list of str): list of words derivationally related to the target word.
        """
        family = []
        if self.wordnet:
            try:
                family += self.wordnet.get_related_words(word)
            except TypeError:
                pass

        family += self.wiktionary.get_related_words(word)
        if family:
            family = list(set(family))
            return family
        return []

    def analyze(self, word):
        """Bringing together all derivational information for the query word.

        Args:
            word (str): the word to look up.

        Returns:
            (dict of str): the derivational analysis data.
        """
        res = self._get_constituents(word)
        res["related_words"] = []
        if res["roots"]:
            for root in res["roots"]:
                res["related_words"] += self._get_related_words(root)
        res["related_words"] = list(set(res["related_words"]))
        try:
            res["related_words"].remove(res["original_word"])
        except ValueError:
            pass
        return res

