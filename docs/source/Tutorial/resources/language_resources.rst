===========================
Language-specific resources
===========================

As specified in the :ref:`Configuration`, LDT
expects to find a ``language_resources`` subfolder in the specified resources path. Language-specific resources are to be located in the subfolders of that folder, named with `2-letter name codes <https://en.wiktionary.org/wiki/Wiktionary:List_of_languages>`_.

The following resources can be `downloaded <https://my.pcloud.com/publink/show?code=XZ8MFe7ZTgD3AwGKcVhf4rgzAJCy3V578yKk>`_ for English:

 - names dictionary. This file was created on the basis of English Wikipedia page titles (dump of November 2017). Only the words in the page title list that were predominantly capitalized in Wikipedia text are included.
 - number dictionary. For English, this file includes single-word cardinal and ordinal numerals.
 - google dependency ngrams dictionary. This is a simple json dictionary that for any word lists all words that were found to cooccur with that word in google dependency ngrams (with frequency over 50).
 - associations dictionary. This file is a combination of `University of South Florida Free Association norms <http://w3.usf.edu/FreeAssociation/>`_ and `Edinburgh Associative Thesaurus <http://rali.iro.umontreal.ca/rali/?q=en/Textual%20Resources/EAT>`_. While association relation in psychology is directional, ldt ignores this crucial property, as in its use case (testing word embedding models) it is not clear what direction (from target to neighbor word or vice versa) should be preferred, if any.

