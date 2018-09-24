=================================================
Normalization and classification of input strings
=================================================

-------------
What LDT does
-------------

Generally speaking, for any input word the following four cases are possible:

1) "cat": a straightforward case where the word is either directly found in dictionaries, or can be lemmatized by productive rules and found in dictionaries;
2) "$%&cat": the input word is misspelled or garbled in pre-processing. The goal is to clean it up and perform step (1).
3) "chatte": the input word is not garbled, but it is not to be found in general dictionaries because it is a foreign word, a url, or some kind of code. Proper names also fall in this category, as detecting semantic relations between them would be different from the general vocabulary.
4) "AdaGram": the input word is not found in dictionaries and cannot be attributed to one of the broader categories in (3).

The overall algorithm for initial processing of input words is as follows:

.. figure:: /_static/ldt_normalize.png
   :align: center

---------
Base case
---------

``Normalizer`` class provides a wrapper for :ref:`MetaDictionary for morphological information`. If a word is not found in dictionaries on its own, but could be an inflected form, productive inflection patterns are used in conjunction with a larger resource (Wiktionary by default) to try to lemmatize. By default, the queries are kept to minimum, i.e. LDT stops at the first resource in which an entry for the queried word is found.

>>> analyzer = ldt.dicts.normalize.Normalization(language="English", order=("wordnet", "wiktionary"), custom_base="wiktionary")
>>> analyzer.normalize("cat")
{'word_categories': ['Lexicon'],
 'found_in': ['wordnet'],
 'lemmas': ['cat'],
 'pos': ['noun', 'verb']}
>>> analyzer.normalize("GPUs")
{'word_categories': ['Lexicon'],
 'found_in': ['wiktionary'],
 'lemmas': ['GPU'],
 'pos': ['noun', 'verb']}

-----------------------------------
Dealing with noise and misspellings
-----------------------------------

LDT attempts to detect and fix the following input problems:

1) Frequent misspelling patterns, as described in section :ref:`Correcting frequent misspellings in English`:

    >>> analyzer.normalize("gramar")
    {'word_categories': ['Misspellings'],
     'found_in': ['wordnet'],
     'lemmas': ['grammar'],
     'pos': ['noun']}

2) Non-alphabetical characters (except numbers) prepended or postpended to a detectable word:

    >>> analyzer.normalize("%grammar")
    {'lemmas': ['grammar'],
     'found_in': ['wordnet'],
     'word_categories': ['Misspellings'],
     'pos': ['noun']}

3) Hyphenation errors:

    >>> analyzer.normalize("gram-mar")
    {'found_in': ['wordnet'],
     'lemmas': ['grammar'],
     'word_categories': ['Misspellings'],
     'pos': ['noun']}

4) Tokenization errors:

    >>> analyzer.normalize("grammar.lexicon")
    {'found_in': ['wordnet'], 'lemmas': ['grammar', "lexicon],
    'word_categories': ['Misspellings'], 'pos': ['noun']}
    >>> analyzer.normalize("grammarlexicon")
    {'found_in': ['wordnet'], 'lemmas': ['grammar', "lexicon],
    'word_categories': ['Misspellings'], 'pos': ['noun']}

The latter relies on the compound splitting mechanism also used in analysis of derivational morphology (see section :ref:`Productive derivation patterns`).

--------------------------------------
Detecting lemmas or extra word classes
--------------------------------------

Some words will not be found in dictionaries, or, even if they are, analysis of semantic relations between them would be different from that for general vocabulary. LDT detects several such cases with resources described in section :ref: `Extra resources`. Names, URLs and filenames are all considered to be nouns.

>>> analyzer.normalize("alice")
{'lemmas': ['alice'], 'word_categories': ['Names'], 'pos': ['noun']}
>>> analyzer.normalize("grammar.com")
{'word_categories': ['URLs'], 'pos': ['noun']}
>>> analyzer.normalize("grammar.jpg")
{'word_categories': ['Filenames'], 'pos': ['noun']}
>>> analyzer.normalize("50")
{'word_categories': ['Numbers'], 'pos': ['numeral']}

Foreign words (detected as described in section :ref:`Detecting foreign words: language-independent functionality` and section :ref:`English spellchecker settings`) are simply attributed to a "Foreign" word category.

>>> analyzer.normalize("grammaire")
 {'word_categories': ['Foreign']}

------------------
"Missing" category
------------------

if everything else fails, the word is attributed to a "missing" word category:

>>> analyzer.normalize("grammarxyz")
{'word_categories': 'missing'}
