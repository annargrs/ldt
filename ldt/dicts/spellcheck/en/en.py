# -*- coding: utf-8 -*-
""" Class for 'safe-to-correct' frequent misspellings.

This module relies on the base spellchecker class that is shared
between all languages. Language-specific subclasses extend it with patterns
for frequent misspellings that should be safe to just fix.

The list of patterns for English was developed on the basis of `Wikipedia
lists of frequent misspellings
<https://en.wikipedia.org/wiki/Wikipedia:Lists_of_common_misspellings/>`_

Patterns:

    * misdoubled letters: *abberation* instead of *aberration* or *gramar*
        instead of *grammar*;
    * letter_misplaced: *abritrary* instead of *arbitrary*;
    * "common_pattern": frequently misspelling patterns, such as "k" for "c"
        in *magik* instead of *magic*
    * "extra_letters": in English, omission or insertion of letter "e" seems
        to be one of the most frequent misspelling patterns (e.g. *befor*
        instead of  *before*;

Todo:

    * load the patterns from an external language-specific yaml file, like in
        the derivation module

"""

# from difflib import SequenceMatcher
#
import operator

from ldt.dicts.spellcheck.custom import Spellchecker as Spellchecker


class SpellcheckerEn(Spellchecker):
    """The class providing the basic English WordNet interface.

    Since WordNets are language-specific, any further additions will have to
    implement similar classes for other languages.

    Todo:

        * Definitions and examples
        * throw and error if any other language is requested

    """

    def __init__(self, foreign_languages=("german", "french"),
                 engine_order="aspell,myspell"):
        """ Initializing the Misspellings class.

        Sets language to "en"

        """

        super(SpellcheckerEn, self).__init__(language="en",
                                             foreign_languages=foreign_languages,
                                             engine_order=engine_order)


    def filter_by_charset(self, word):
        """An English-specific wrapper for :meth:`filter_by_charset` that
        excludes words containing anything other than alphanumeric
        characters or hyphen.

        Exclusion of "with" enables avoiding Latin characters with diacritics.

        Args:
            word (str): the word to check.

        Returns:
            (bool): True if only allowed charsets are present
        """
        try:
            word.encode('ascii')
            return True
        except UnicodeEncodeError:
            return False

        # else:
        #     return self.filter_by_charset(word, include=["latin", "digit",
        #                                    "hyphen-minus", "apostrophe"],
        #                                    exclude=["with"])

    def is_foreign(self, word, dictionary=None):
        """Excluding foreign words with a combination of charset checking and
        select foreign dictionaries.

        Args:
            word (str): the word to check
            dictionary (LDT dictionary object): if specified, checking if a
                word entry is present for English will also be conducted in this
                language.

        Note:

            Wiktionary pagelists should *not* be used to detemine if a word
            has an entry in English, because it is Wiktionary's explicit aim
            that all Wiktionaries should contain entries for all words. For
            example, the lists of lemmas in the English Wiktionary also
            contains lemmas for other languages
            (https://en.wiktionary.org/wiki/Category:Lemmas_by_language).

        Returns:
            (bool): False if the word either contains foreign characters or is
            found in foreign dictionaries (excluding words present in the
            English spellchecker dictionary)

        """
        if not self.filter_by_charset(word):
            return True

        if self.is_a_word(word):
            return False
        if dictionary:
            if dictionary.is_a_word(word):
                return False
        elif self.in_foreign_dicts(word):
            return True

    #pylint: disable=too-many-locals
    #pylint: disable=too-many-branches
    def spelling_nazi(self, word, confidence=True, strict=True, min_length=4):
        """This function attempts to correct common misspellings according
        to a predefined set of patterns.

        Args:
            word (str): the word to spellcheck
            confidence (bool): if True, only the best candidate is returned.
                If False, a ranked list of candidates is returned.
            strict (bool): limit the search to the predefined patterns if True
            min_length (int): do not attempt to correct words shorter than
                that.

        Returns:
            (str or list): best ranking candidate or a ranked list of
                candidates

        Note:
            English has too many short frequent words different with only one
                letter, so dealing only with longer words is preferable.

        """

        if len(word) < min_length:
            return None

        if self.is_a_word(word):
            return None

        res = {}
        res_annotated = {}
        suggestions = self.target.suggest(word)

        for candidate_word in suggestions:

            # do not allow more than 1 letter difference in length
            if abs(len(candidate_word) - len(word)) < 2:

                res[candidate_word] = 0
                res_annotated[candidate_word] = []

                patterns = self.common_misspellings(word, candidate_word)

                scores = {"letter_misdoubled":20, "letter_misplaced":20,
                          "common_pattern":20, "extra_common_letter":10,
                          "missing_common_letter":10,
                          "double_letter_missed":20, "fishy": -20}

                # allowing only for 1 transformation
                if patterns:
                # if len(patterns) == 1:
                    res[candidate_word] += scores[patterns[0]]
                    res_annotated[candidate_word].append(patterns[0] + " " + \
                                            str(scores[patterns[0]]))

                # simple extra heuristic: reward starting and ending with
                # the same letter
                if candidate_word[0] == word[0]:
                    res[candidate_word] += 10
                    res_annotated[candidate_word].append("initial " + str(10))
                if candidate_word[-1] == word[-1]:
                    res[candidate_word] += 10
                    res_annotated[candidate_word].append("final " + str(10))

                # downgrade names and punctuated words
                if candidate_word[0].isupper():
                    res[candidate_word] -= 10
                    res_annotated[candidate_word].append("name " + str(-20))
                for punc in ["-", "'", " "]:
                    if punc in candidate_word and not punc in word:
                        res[candidate_word] -= 10
                        res_annotated[candidate_word].append("punc " + str(-20))

        if strict:
            cleaned = {}
            for candidate in res_annotated:
                for annotation in res_annotated[candidate]:
                    if annotation.split()[0] in scores and not \
                            annotation.split()[0] == "fishy":
                        cleaned[candidate] = res[candidate]
            res = cleaned
        ordered = sorted(res.items(), key=operator.itemgetter(1), reverse=True)
        res_list = [x for (x, y) in ordered]
        if res_list:
            if not confidence:
                return res_list
            else:
                if res[res_list[0]] > 30:
                        #to make sure that at least several heuristics applied
                    return res_list[0]

    #pylint: disable=too-many-branches
    def common_misspellings(self, misspelling, word):
        """Classifying the misspelling patterns, if any.

        Args:
            misspelling (str): the potentially misspelled word
            word (str): the correct word

        Returns:
            (list of str): the recognized types of misspellings that apply in
            this case
        """

        res = []
        aligned = self.get_opcode_alignment(misspelling, word)
        misspelling = aligned["misspelling"]
        word = aligned["word"]
        deletes = aligned["deletes"]
        inserts = aligned["inserts"]
        replaces = aligned["replaces"]

        # discard words that are just different in length
        if " " in inserts:
            return None

        # discard candidates where more than one letter was changed
        else:
            for string in deletes+inserts:
                if len(string) > 1:
                    return None
            for tupl in replaces:
                for i in tupl:
                    if len(i) > 1:
                        return None

        # discard candidates with too many transformations
        total_transforms = len(deletes)+len(inserts)+len(replaces)
        if total_transforms not in (2, 1):
            return None

        if total_transforms == 2:

        # up to 2 cases of deletions/insertions of the same letter was
        # deleted and replaced

            if len(inserts) == len(deletes) == 1:
                if inserts[0] == deletes[0]:
                    res = self._misplaced_letters(inserts, deletes, res)

        elif total_transforms == 1:

            # up to 1 replacement sanctioned by common patterns
            if not deletes and not inserts:
                if len(replaces) == 1:
                    res = self._common_replacements(replaces, res)

            # if one insertion or deletion - ok if it's e or if it's doubling
            elif not replaces:
                if not deletes and len(inserts) == 1:
                    res = self._extra_letters(misspelling, word, res)
                    if not res:
                        res = self._double_letters(misspelling, word, inserts, res)
                elif len(deletes) == 1 and not inserts:
                    res = self._misdoubled_letter(misspelling, word,
                                                  deletes, res)
        return res

    # pylint: disable=no-self-use
    def _misdoubled_letter(self, misspelling, word, deletes, res):
        if word.count("_") == 1:
            ind = word.index("_")
            if misspelling[ind].lower() in deletes and len(deletes) == 1:
                if misspelling[ind].lower() == word[ind-1].lower():
                    res.append("letter_misdoubled")
        return res

    #pylint: disable=no-self-use
    def _double_letters(self, misspelling, word, inserts, res):
        """Helper for :meth:`common_misspellings`: dealing with *gramar >
        grammar* patterns."""
        # if there is only one insert and the next letter is the same is insert
        # (aple - apple)
        if misspelling.count("_") == 1:
            ind = misspelling.index("_")
            if word[ind].lower() in inserts and len(inserts) == 1:
                if word[ind].lower() == word[ind-1].lower():
                    res.append("double_letter_missed")
                elif len(word) >= ind+1:
                    if word[ind].lower() == word[ind+1].lower():
                        res.append("double_letter_missed")
        return res

        # if there is only one delete and the next letter is the same is deleted
        #  (travell - travel)
        # elif word.count("_") == 1:
        #     ind = word.index("_")
        #     if misspelling[ind].lower() in deletes and len(deletes) == 1:
        #         if misspelling[ind].lower() == word[ind-1].lower():
        #             res.append("letter_misdoubled")
        # return res

    #pylint: disable=no-self-use
    def _extra_letters(self, misspelling, word, res):
        """Helper for :meth:`common_misspellings`: dealing with *befor >
        before* patterns."""
        #pylint: disable=consider-using-enumerate
        for i in range(len(misspelling)):
            if word[i] in ["E"] and misspelling[i] == "_":
                res.append("missing_common_letter")
            # if misspelling[i] in ["E"] and word[i] == "_":
            #     res.append("extra_common_letter")
        return res

    #pylint: disable=no-self-use
    def _common_replacements(self, replaces, res):
        """Helper for :meth:`common_misspellings`: dealing with *magik >
        magic* patterns."""
        common_patterns = [["i", "y"], ["c", "k"], ["g", "j"]]

        passed = False
        if replaces:
            if len(replaces) == 1:
                for pattern in common_patterns:
                    if pattern[0] in replaces[0] and pattern[1] in \
                            replaces[0]:
                        res.append("common_pattern")
                        passed = True
        if not passed:
            res.append("fishy")
        return res

    #pylint: disable=no-self-use
    def _misplaced_letters(self, inserts, deletes, res):
        """Helper for :meth:`common_misspellings`: dealing with *wrok >
        work* patterns."""
        if inserts:
            for i in inserts:
                if i in deletes:
                    res.append("letter_misplaced")
                else:
                    if not "letter_misdoubled" in res or \
                            "double_letter_missing" in res \
                            or "common pattern" in res in res:
                        res.append("fishy")

        return list(set(res))
