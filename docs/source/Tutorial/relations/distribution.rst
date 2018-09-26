===============================
Distribution information in LDT
===============================

-------------
What LDT does
-------------

Evaluating a word embedding model is only fair if you know what information
it had to begin with. At the moment LDT provides access to pre-computed
frequency and cooccurrence dictionary as well as google dependency ngrams.

Location and filenames of corpus-specific resources are specified in the ldt
configuration file as described in section :ref:`Corpus-specific resources`.
The interface to all of them is provided by
:class:`~ldt.relations.distribution.DistributionDict` class.

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

Currently the cooccurrence data for Wiki201308 corpus is available for
linear symmetrical context of size 2. See `this paper <http://www.aclweb
.org/anthology/D17-1257>`_ for discussion of various context types.

Cooccurrence files are large, and for faster lookup they have to be loaded in
 RAM, but Python is not particularly efficient with this. With the
 current implementation it takes about 40 seconds to load ~1.5G file on a core
  i7 32Gb RAM machine (and it ends up taking ~4Gb of memory). By default, the
  DistributionDict is initialized without them. If you need them, specify
  that at initialization of the resource:

>>> distribution_dict = ldt.relations.DistributionDict(cooccurrence=True)
>>> distribution_dict.cooccur_in_corpus("cat", "dog")
True
>>> distribution_dict.cooccur_in_corpus("cat", "semantics")
False

If you need to know the exact cooccurrence rates, use the additional
``freq=True`` option. Note that the querying will be slower.

>>> distribution_dict = ldt.relations.DistributionDict(cooccurrence=True, cooccurrence_freq=True)
>>> distribution_dict.cooccur_in_corpus("cat", "semantics")
0

>>> distribution_dict.cooccur_in_corpus("cat", "dog")
686

------------------------
Google dependency ngrams
------------------------

LDT's google dependency ngrams file is a simple json dictionary that for any
 word lists all words that were found to cooccur with that word in google
 dependency ngrams (with frequency over 50). At the moment there is no
 option to retrieve cooccurrence frequencies.

You can use this resource by loading the DistributionDict with gdeps option
(off by default, as the loading of this resource takes both memory and time):

>>> distribution_dict = ldt.relations.DistributionDict(gdeps=True)
>>> distribution_dict.cooccur_in_gdeps("cat", "dog")
True
>>> distribution_dict.cooccur_in_gdeps("cat", "semantics")
False
