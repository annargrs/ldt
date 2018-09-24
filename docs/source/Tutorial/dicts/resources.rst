===============
Extra resources
===============

.. contents:: :local:

-------------
What LDT does
-------------

A large part of vocabulary of word embeddings cannot be found in common dictionary resources because they are not even supposed to be there. Of these words, LDT attempts to detect names, numbers, filenames and URLs to at least be able to group them together. At least a portion of names may be found in named entity ontologies, and relations between them could theoretically be further processed in the future.

Generally all the extra resources provide a single ``is_a_word("word")`` method that returns True if the queried word is found to belong to the corresponding word class.

---------------
Detecting names
---------------

The LDT names dictionary file for English was created on the basis of English Wikipedia page titles (dump of November 2017). Only the words in the page title list that were predominantly capitalized in Wikipedia text are included.

>>> names_dict = ldt.dicts.resources.NameDictionary()
>>> names_dict.is_a_word("alice")
True
>>> names_dict.is_a_word("table")
False

-----------------
Detecting numbers
-----------------

For English, this file includes single-word cardinal and ordinal numerals.

>>> numbers_dict = ldt.dicts.resources.NumberDictionary()
>>> numbers_dict.is_a_word("twenty")
True
>>> numbers_dict.is_a_word("cat")
False

Digits also count

>>> numbers_dict.is_a_word("20")
True

As do words that contain a mixture of words and numbers:

>>> numbers_dict.is_a_word("abcde20")
True

--------------
Detecting URLs
--------------

LDT relies on a simple list of web domains, protocols, and/or "www" to determine URLs:

>>> web_dict = ldt.dicts.resources.WebDictionary("google.com")
>>> web_dict.is_a_word("google.com")
True
>>> web_dict.is_a_word("cat")
False
>>> web_dict.is_a_word("http://something.science")
True

-------------------
Detecting filenames
-------------------

In web-crawled corpora and even Wikipedia pre-processing artifacts are not uncommon, and filenames are among such most common artifacts. LDT tackles them with a simple list of common file extensions, and/or presence of over 2 forward or back slashes.

>>> file_dict = ldt.dicts.resources.FileDictionary()
>>> file_dict("cat.jpg")
True
>>> file_dict("cat")
False
>>> file_dict.is_a_word("/path/to/my/cat")
True

