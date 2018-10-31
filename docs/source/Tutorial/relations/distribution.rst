==========================
Distributional information
==========================

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

>>> distribution_dict = ldt.relations.DistributionDict(frequencies=True)
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
  that at initialization of the resource.

Take into account that full distributional resources for Wikipedia are
large, and 2Gb file on disk takes even more memory when loaded into Python.
You can avoid this by providing a list of words that should be loaded: in
that case ldt will read the large files line-by-line and only load the data
you need. In LDT experiments this is done automatically, since at the
annotation stage it is already known what words have been extracted. If you

>>> distribution_dict = ldt.relations.DistributionDict(cooccurrence=True, wordlist=my_wordlist)
>>> distribution_dict.cooccur_in_corpus("cat", "dog")
True
>>> distribution_dict.cooccur_in_corpus("cat", "semantics")
False

------------------------
Google dependency ngrams
------------------------

LDT's google dependency ngrams file is a simple json dictionary that for any
 word lists all words that were found to cooccur with that word in google
 dependency ngrams (with frequency over 50).

You can use this resource by loading the DistributionDict with gdeps option
(off by default). Like for cooccurrence data, you can save gigabytes of RAM by
providing a list of words the data for which should be loaded.

>>> distribution_dict = ldt.relations.DistributionDict(gdeps=True, wordlist=mywordlist)
>>> distribution_dict.cooccur_in_gdeps("cat", "dog")
True
>>> distribution_dict.cooccur_in_gdeps("cat", "semantics")
False

----------------------------------------
Combining all distributional information
----------------------------------------

>>> distribution_dict = ldt.relations.DistributionDict(frequencies=True, gdeps=True, wordlist=["cat", "dog"])
>>> distribution_dict.analyze("cat", "dog")
{'GDeps': True, 'NonCooccurring': False, 'NeighborFrequency': 95131, 'TargetFrequency': 87783}