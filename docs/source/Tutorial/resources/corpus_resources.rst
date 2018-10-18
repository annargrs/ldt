=========================
Corpus-specific resources
=========================

It is possible to use LDT for profiling any pre-trained word-level embeddings.
However, distributional information is obviously corpus-specific, and can
only be retrieved if the source corpus is known, and collocation data is
available. See `here <http://ldtoolkit
.space/analysis/examples/#use-case-1-explaining-performance-on-downstream-tasks>`_
for evidence of different behavior of word2vec and GloVe with regards to word
vector neighbors that are related, but were infrequent in the source corpus
or did not cooccur at all.

The next release of ldt (0.4.0) will include functionality for building
required distributional resources for any given tokenized corpus. For now, we
are sharing `the data that we used in our experiments on English Wikipedia
(August 2013) <https://my.pcloud.com/publink/show?code=XZzMFe7Z20t1QWsappQy7BlRdvrqcbrAM6HV>`_. This includes:

  - frequency dictionary,
  - cooccurrence data for linear unbound context window size 2 (more to come),
  - vocab file containing 269,864 words by which which all embeddings were filtered in the experiments described in the `LDT paper <http://aclweb.org/anthology/C18-1228>`_.

The corpus itself, pre-processed:

 * `One-sentence per line, cleaned from punctuation <https://my.pcloud.com/publink/show?code=XZKxYV7ZIl9KNR5oLa5K2OMQlVuW1XJ1IV0V>`_
 * `One-word-per-line, parser tokenization <https://my.pcloud.com/publink/show?code=XZYcQV7ZR67964yEkEJhgHaM273JjptIUEpX>`_
    (this is the version used in the non-dependency-parsed embeddings downloadable below, so use this one if you would
    like to have embeddings that are directly comparable).
 * `Dependency-parsed version (CoreNLP Stanford parser) <https://my.pcloud.com/publink/show?code=XZ1nbV7ZTdOs3qzO6p7X3lzX7Ychmbqc2unX>`_

The dump was originally presented in `this paper <http://www.aclweb.org/anthology/D17-1256>`_ by Li et al., who used it
to compare the effect of 4 types of syntactic context (symmetrical/positional linear and dependency-based). They also
generated 60 Skip-Gram, CBOW and GloVe embeddings with vector sizes 25, 50, 100, 250 and 500 in each of these conditions.
All the original embeddings are available in
`vecto library <http://vecto.readthedocs.io/en/docs/tutorial/getting_vectors
.html#pre-trained-vsms>`_, and you can download them to explore ldt capabilities.

`Get in touch <anna_rogers@uml.edu>`_ if you'd like to make your data available here in the same way.

If you would like to just experiment with ldt on some pre-trained embeddings
for which you don't have the distributional information, just comment out
the relevant lines in the :ref:`Configuration file`.