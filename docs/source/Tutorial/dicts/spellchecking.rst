=============
Spellchecking
=============

.. contents:: :local:

-------------
What LDT does
-------------

LDT provides an interface to the base ldt spellchecker class, currently based on `pyenchant <https://github.com/rfk/pyenchant>`_ library which in its turn relies
on `enchant <https://github.com/AbiWord/enchant>`_. Pyenchant enables the use of various engines, including hunspell and aspell. Check the
section :doc:`../installation`.

Note:

    Pyenchant developer announced that he's retiring from the project. It was last updated in February 2017. Moving to another spellchecker engine may be necessary in the future.

A part of spellchecking functionality is provided by the
:class:`~ldt.dicts.normalize.Normalization` class. See section :doc:`normalization`.

-----------------------------------------------------------
Detecting foreign words: language-independent functionality
-----------------------------------------------------------

Language-independent :class:`~ldt.dicts.spellcheck.custom.Spellchecker` class
initializes with a "main" language and a list of languages to be considered
"foreign". This is useful in case of corpora that may have a relatively high
 portion of words in those languages (e.g. Spanish in American English).
``is_a_word("word")`` method returns True if the queried word is found in
the spellechecker dictionary for the specified "main" language.

>>> spellchecker = ldt.dicts.spellcheck.Spellchecker(language="english", foreign_languages = ("german", "french"))
>>> spellchecker.is_a_word("cat")
True
>>> spellchecker.is_a_word("kat")
False

Foreign status of a word can be confirmed with
:meth:`~ldt.dicts.spellcheck.custom.Spellchecker.in_foreign_dicts()` method:

>>> spellchecker.in_foreign_dicts("casa")
True
>>> spellchecker.in_foreign_dicts("cat")
False

There is also :meth:`~ldt.dicts.spellcheck.custom.Spellchecker.filter_by_charset`,
which enables filtering foreign words by unicode charset (e.g. cyrillic,
arabic, korean, cjk, latin, etc.) See the method docstring for more details.

>>> spellchecker.filter_by_charset("cat", include=["latin"])
True
>>> spellchecker.filter_by_charset("猫", include=["latin"])
False


-----------------------------
English spellchecker settings
-----------------------------

The above methods should be inherited by the language-specific classes with
appropriate defaults for those languages. For English, the default LDT
"foreign languages" are Spanish and French.

>>> spellchecker = spellchecker_en = ldt.dicts.spellcheck.SpellcheckerEn()
>>> spellchecker_en.is_a_word("cat")
True
>>> spellchecker_en.is_a_word("Katze")
False
>>> spellchecker.in_foreign_dicts("Katze")
True

For English detection of foreign charsets is implemented not via
:meth:`~ldt.dicts.spellcheck.custom.Spellchecker.filter_by_charset`, but via
 encoding to ascii, as this is faster.

spellchecker_en.filter_by_charset("кошка")
>>> False

Note:

    If a foreign charset is detected, the word is also reported as foreign by
    :meth:`~ldt.dicts.spellcheck.custom.Spellchecker.in_foreign_dicts`:

    >>> spellchecker_en.in_foreign_dicts("猫")
    True

-------------------------------------------
Correcting frequent misspellings in English
-------------------------------------------

Web-crawled corpora and even Wikipedia have a lot of misspellings, but because of abundance of names, troponyms, specialized terms etc. simply trusting a spellchecker to correct everything automatically is clearly not an option.

LDT provides the following option: for words that were not found in dictionary resources, it is possible to check for 3 frequent misspelling patterns:

* misdoubled letters: *abberation* instead of *aberration* or *gramar* instead of *grammar*;
* letter_misplaced: *abritrary* instead of *arbitrary*;
* "extra_letters": in English, omission or insertion of letter "e" seems to be one of the most frequent misspelling patterns (e.g. *befor* instead of  *before*).

This functionality is provided by the
:meth:`~ldt.dicts.spellcheck.en.en.SpellcheckerEn.spelling_nazi` method of
``SpellcheckerEn`` class. By default, only words longer than 4 characters
are processed, as with longer words the likelihood of correct fix is higher.
 Only one correction is allowed.

>>> spellchecker_en.spelling_nazi("pot")
None
>>> spellchecker_en.spelling_nazi("aceptable")
"acceptable"
>>> spellchecker_en.spelling_nazi("abritrary")
'arbitrary'
>>> spellchecker_en.spelling_nazi("befor")
"before"

