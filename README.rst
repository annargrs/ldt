====================================
Linguistic Diagnostics Toolkit (LDT)
====================================

.. image:: https://travis-ci.com/ookimi/ldt.svg?token=vNtsLg9GAp2WkcBr9HBr&branch=master
   :target: https://travis-ci.com/ookimi/ldt
   :alt: Build Status

----
TLDR
----

.. inclusion-marker-begin-do-not-remove

LDT is a shiny new Python library for doing two things:

* querying lots of dictionaries from a unified interface to perform
  **spelling normalization, lemmatization, morphological analysis,
  retrieving semantic relations from WordNet, Wiktionary, BabelNet**, and a lot more.

* using the above to **explore and profile word embeddings**, i.e. the cool
  distributional representations of words as vectors.

If you have never heard about word embeddings -- you're missing out, here's `an introduction <https://www.shanelynn.ie/get-busy-with-word-embeddings-introduction/>`_.  If you have, head  over to the `project website <ldtoolkit.space>`_ for some new research results. And if you don't care about word embeddings, you can still just use LDT as a supplement to NLTK, SpaCy, and other great NLP tools.

**Note:** LDT is undergoing refactoring, and not all the LD scores published** `in the paper <http://aclweb.org/anthology/C18-1228>`_ are in the public build yet. Check back for the rest of the code and detailed tutorial in the end of August.

.. inclusion-marker-end-do-not-remove

----------------------
Current functionality
----------------------

LDT provides a unified interface for querying a vast array of resources for natural
  language processing, including Wiktionary, BabelNet, WordNet, and a lot of
  new custom routines:

     * misspellings (*cat : kat*);
     * inflected forms (*cat : cats*);
     * derivational relations (*cat : cattish*);
     * lexicographic semantic relations:
       - synonymy (*cat : pussycat*);
       - antonymy (*black : white*);
       - hyperonymy (*cat : feline*);
       - hyponymy (*feline : cat*);
       - co-hyponymy (*cat : dog*);
       - meronymy (*cat : tail*)

All of the above can be used for large-scale analysis of potential relations between pairs
  of words. See ldt.experiments.demo file for a toy example of such an analysis.

That last step can help you predict how your model will do on a particular
task, and also give some ideas about how it can be improved. Check out the
`results of a large-scale experiment with 60 embeddings and 21 datasets.
<http://ldtoolkit.space/analysis/correlation/>`_

-----------
Quick links
-----------

 * `Project website <ldtoolkit.space>`_
 * `API reference <https://ldt.readthedocs.io/genindex.html>`_.
 * `Published research results <http://aclweb.org/anthology/C18-1228>`_.
 * `Word embeddings leaderboard <http://ldtoolkit.space/leaderboard/>`_.
 * `Correlation of LD scores with downstream task performance <http://ldtoolkit.space/analysis/correlation/>`_.

-------
Support
-------

If something doesn't work, open an issue on GitHub.

---------------
Multilinguality
---------------

Yes, LDT is multilingual! At least, as far as querying semantic relations
goes. LDT supports the largest free multilingual resources (Wiktionary
and BabelNet), so everything they have is retrievable. However, many of the
other LDT modules are language-specific, and only English is fully supported at
the moment. But the infrastructure for adding other languages is already
in place, so if you can find or create e.g. lists of affixes for your
language, development would be easy. Get in touch if you'd like to get
involved.
