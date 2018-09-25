===============================
Distribution information in LDT
===============================

-------------
What LDT does
-------------

Evaluating a word embedding model is only fair if you know what information it had to begin with. At the moment LDT provides access to pre-computed frequency and cooccurrence dictionary as well as google dependency ngrams.

Location and filenames of corpus-specific resources are specified in the ldt configuration file as described in section :ref:`Corpus-specific resources`. The interface to all of them is provided by :meth:`~ldt.relations.distribution.DIstributionDict` class.

-----------------------------------
Word frequency in the source corpus
-----------------------------------

Get the frequency of a given word in the source corpus as follows:

>>> distribution_dict = ldt.relations.DistributionDict()
>>> distribution_dict.frequency_in_corpus("cat")
87783

---------------------------------
Cooccurrence in the source corpus
---------------------------------



------------------------
Google dependency ngrams
------------------------

LDT's google dependency ngrams file is a simple json dictionary that for any word lists all words that were found to cooccur with that word in google dependency ngrams (with frequency over 50).

You can use this dictionary as a standalone resource as follows:

