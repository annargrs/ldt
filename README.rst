==============================
Linguistic Diagnostics Toolkit
==============================

**TLDR**: LDT is a shiny new Python library for doing two things:

------------

    * querying lots of dictionaries from a unified interface:
      spelling normalization, lemmatization, morphological analysis, WordNet,
      Wiktionary, BabelNet, and a lot more.
    * using the above to explore and profile word embeddings, i.e. the cool
      distributional representations of words as vectors. If you have never
      heard the word "word2vec" but are intrigued, here's `an introduction
      <https://www.shanelynn.ie/get-busy-with-word-embeddings-introduction/>`_.
      If you have, head over to the `project website <ldtoolkit.space>`_. If
      you don't care about word embeddings, you can just use LDT as a
      supplement to NLTK, SpaCy, and other great NLP tools.

------------

Current functionality:

* A unified interface for querying a vast array of resources for natural
  language processing, including Wiktionary, BabelNet, WordNet, and a lot of
  new custom routines:

     * misspellings (*cat : kat*);
     * inflected forms (*cat : cats*);
     * derivational relations (*cat : catness*);
     * lexicographic semantic relations:
       - synonymy (*cat : pussycat*);
       - antonymy (*black : white*);
       - hyperonymy (*cat : feline*);
       - hyponymy (*feline : cat*);
       - co-hyponymy (*cat : dog*);
       - meronymy (*cat : tail*)
     * psychological association norms (cat : mouse)
     * corpus-based statistics (e.g. for *cat : mouse* pair the frequency of
       *mouse* in the corpus in general and in the context of *cat* in
       particular);

* Using the above for large-scale analysis of potential relations between pairs
  of words

* Full setup for experimenting with your favorite word embeddings: loading
  them, drawing balanced vocab samples, and profiling them for the kinds of
  information that they encode.

That last step can help you predict how your model will do on a particular
task, and also give some ideas about how it can be improved. Check out the
`results of a large-scale experiment with 60 embeddings and 21 datasets.
<http://ldtoolkit.space/analysis/correlation/>`_

Quick links:

 * Installation
 * Tutorial
 * API reference
 * Published research results
 * Word embeddings leaderboard

If something doesn't work: open an issue on GitHub.

On multilinguality: for semantic analysis, LDT supports the largest
available multilingual resources (Wiktionary and BabelNet). Many of the
other modules are language-specific, and only English is fully supported at
the moment, but the infrastructure for going multilingual is already in
place. Get in touch if you'd like to get involved.
