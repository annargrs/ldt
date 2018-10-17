====================================
Linguistic Diagnostics Toolkit (LDT)
====================================

.. image:: https://travis-ci.com/annargrs/ldt.svg?branch=master
   :target: https://travis-ci.com/annargrs/ldt
   :alt: Build Status

.. inclusion-marker-begin-do-not-remove

LDT is a shiny new Python library for doing two things:

* querying lots of dictionaries from a unified interface to perform **spelling normalization, lemmatization, morphological analysis, retrieving semantic relations from WordNet, Wiktionary, BabelNet**, and a lot more.

* using the above to **explore and profile word embeddings**, i.e. the cool distributional representations of words as vectors.

If you have never heard about word embeddings -- you're missing out, here's `an introduction <https://www.shanelynn.ie/get-busy-with-word-embeddings-introduction/>`_.  If you have, head  over to the `project website <ldtoolkit.space>`_ for some new research results. And if you don't care about word embeddings, you can still just use LDT as a supplement to NLTK, SpaCy, and other great NLP tools.

**Note:** LDT is in active development; all the dictionary functionality for English and scripts for running experiments are already available. Integration with `vecto library <vecto.space>`_ are coming in the nearest weeks. Make sure you update your installation often, and join the `discussion <https://groups.google.com/forum/#!forum/linguistic-diagnostics>`_ group to discuss your results and get notified about new releases!

---------------------------------
LDT for profiling word embeddings
---------------------------------

Simply `install and configure <https://ldt.readthedocs.io/Tutorial/installation.html>`_ ldt, and run this script:

::

   python3 -m ldt.experiments.default_workflow

The output will be something like this:

+-------------------+--------+--------+--------+
| LD score          | CBOW   | GloVe  | SG     |
+-------------------+--------+--------+--------+
| SharedMorphForm   | 51.819 | 52.061 | 52.9   |
+-------------------+--------+--------+--------+
| SharedPOS         | 30.061 | 35.507 | 31.706 |
+-------------------+--------+--------+--------+
| SharedDerivation  | 4.468  | 3.938  | 5.084  |
+-------------------+--------+--------+--------+
| Synonyms          | 0.413  | 0.443  | 0.447  |
+-------------------+--------+--------+--------+
| Antonyms          | 0.128  | 0.133  | 0.144  |
+-------------------+--------+--------+--------+
| Hyponyms          | 0.035  | 0.035  | 0.038  |
+-------------------+--------+--------+--------+
| OtherRelations    | 0.013  | 0.013  | 0.013  |
+-------------------+--------+--------+--------+
| Misspellings      | 13.546 | 9.914  | 12.809 |
+-------------------+--------+--------+--------+
| ProperNouns       | 30.442 | 27.278 | 27.864 |
+-------------------+--------+--------+--------+
| LowFreqNeighbors  | 94.778 | 66.51  | 96.109 |
+-------------------+--------+--------+--------+
| HighFreqNeighbors | 3.421  | 15.697 | 2.513  |
+-------------------+--------+--------+--------+
| NonCooccurring    | 88.97  | 67.904 | 90.252 |
+-------------------+--------+--------+--------+
| CloseNeighbors    | 3.102  | 0.16   | 2.278  |
+-------------------+--------+--------+--------+
| FarNeighbors      | 25.209 | 49.934 | 21.41  |
+-------------------+--------+--------+--------+

The numbers here indicate percentage of neighbor vectors that held the
indicated relation with each target word in the sample. The information is
coming from a ton of dictionaries (see below), and you can fine-tune which
ones you want to use.

LDT profile explains what kinds of information your embedding model
actually captures. That can help you predict how your model will do on
a  particular task, and also give some ideas about how it can be improved.
Check out the `results of a large-scale experiment with 60 embeddings and 21
datasets. <http://ldtoolkit.space/analysis/correlation/>`_

And yes, you heard it right, you can use your own vocabulary sample - the one
that actually makes sense for whatever  downstream task you're optimizing for!

Note:

   The current implementation queries online resources, so a large
   experiment will take time. Stay tuned, we're working on making it faster.
   The distribution analysis is currently provided for embeddings trained on
   our `pre-processed Wikipedia dump <http://ldtoolkit.space/task_data/>`_,
   which is also available in dependency-parsed version.

-----------------------------------------
LDT for detecting relations in word pairs
-----------------------------------------

The main function of LDT is automatic detection of linguistic relations
that *could* possibly hold in a pair of words. This can now be achieved as
follows:

>>> relation_analyzer = ldt.relations.RelationsInPair()
>>> relation_analyzer.analyze("black", "white")
{'Hyponyms': True,
 'SharedMorphForm': True,
 'SharedPOS': True,
 'Synonyms': True,
 'Antonyms': True,
 'ShortestPath': 0.058823529411764705,
 'Associations': True}

It goes without saying that *white* and *black* are not always antonyms.
Context dependence is something we're thinking about, but at the moment ldt
follows other context-independent evaluation methodologies such as human
judgements of word similarity/relatedness.

---------------------------------
LDT for working with dictionaries
---------------------------------

The above information comes from a ton of various dictionary resources. You
can access all combined information about any given word in one click:

>>> encapsulation = ldt.Word("encapsulation")
>>> encapsulation.pp_info()
======DERIVATIONAL INFO======
Stems :  capsulate, encapsulate, capsule
Suffixes :  -ion, -ate
Prefixes :  en-
OtherDerivation :
RelatedWords :  encapsulation, capsule review, glissonian capsule, capsular, capsulate
======SEMANTIC INFO======
Synonyms :  encapsulation
Antonyms :
Meronyms :
Hyponyms :
Hypernyms :  physical_process, status, condition, process
======EXTRA WORD CLASSES======
ProperNouns :  False
Noise :  False
Numbers :  False
URLs :  False
Hashtags :  False
Filenames :  False
ForeignWords :  False
Misspellings :  False
Missing :  False

To provide this, LDT queries various old and new resources. Accordingly,
they are all now accessible from a unified Python interface,
making LDT usable in other NLP research areas as a companions to NLTK.

A few quick highlights of ldt resources:

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Retrieving related words from WordNet, Wiktionary, Wiktionary Thesaurus and BabelNet:
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

>>> wiktionary = ldt.dicts.semantics.Wiktionary()
>>> wiktionary.get_relation("white", relation="synonyms")
['pale', 'fair']
>>> wikisaurus = ldt.dicts.semantics.Wikisaurus()
>>> wikisaurus.get_relations("cat", relations="all")
{'synonyms': ['tabby', 'puss', 'cat', 'kitty', 'moggy', 'housecat', 'malkin', 'kitten', 'tom', 'grimalkin', 'pussy-cat', 'mouser', 'pussy', 'queen', 'tomcat', 'mog'],
 'hyponyms': [],
 'hypernyms': ['mammal', 'carnivore', 'vertebrate', 'feline', 'animal', 'creature'],
 'antonyms': [],
 'meronyms': []}
>>> babelnet = ldt.dicts.semantics.BabelNet()
>>> babelnet.get_relations("senator", relations=("hypernyms"))
{'hypernyms': ['legislative_assembly', 'metropolitan_see_of_milan', 'poltician', 'legislative_seat', 'senator_of_rome', 'band', 'the_upper_house', 'polictian', 'patres_conscripti', 'musical_ensemble', 'presbytery', 'politician', 'pol', 'solo_project', 'policymaker', 'political_figure', 'politican', 'policymakers', 'archbishop_emeritus_of_milan', 'deliberative_assemblies', 'ensemble', 'career_politics', 'soloproject', 'list_of_musical_ensembles', 'legislative', 'roman_senators', 'archbishopric_of_milan', 'politicain', 'rock_bands', 'section_leader', 'musical_organisation', 'music_band', 'four-piece', 'roman_catholic_archdiocese_of_milan', 'upper_house', 'archdiocese_of_milan', 'band_man', 'milanese_apostolic_catholic_church', 'legistrative_branch', 'group', 'solo-project', 'music_ensemble', 'law-makers', 'roman_senator', 'legislative_arm_of_government', 'solo_act', 'patronage', 'roman_catholic_archbishop_of_milan', 'bar_band', 'senate_of_rome', 'deliberative_body', 'see_of_milan', 'legislative_fiat', 'musical_group', 'ambrosian_catholic_church', 'legislature_of_orissa', 'legislative_branch_of_government', 'list_of_politicians', 'senatorial_lieutenant', 'roman_catholic_archdiocese_of_milano', 'legislature_of_odisha', 'bandmember', 'assembly', 'archdiocese_of_milano', 'bishop_of_milan', 'ensemble_music', 'solo_musician', 'musical_duo', 'legislative_branch_of_goverment', 'first_chamber', 'politicians', 'legislative_bodies', 'political_leaders', 'politico', 'music_group', 'legislative_body', 'career_politician', 'legislature', 'rock_group', 'legislative_power', 'diocese_of_milan', 'musical_ensembles', 'musical_organization', 'revising_chamber', 'archbishops_of_milan', 'political_leader', 'deliberative_assembly', 'conscript_fathers', 'five-piece', 'catholic_archdiocese_of_milan', 'pop_rock_band', 'senatrix', 'deliberative_organ', 'polit.', 'roman_senate', 'legislative_politics', 'bishopric_of_milan', 'legislative_branch', 'musical_band', 'archbishop_of_milan', 'legislatures', 'general_assembly', 'musical_groups', 'instrumental_ensemble', 'politition', 'patres', 'upper_chamber', 'solo-act', 'conscripti', 'legislator']}

++++++++++++++++++++++
Derivational analysis:
++++++++++++++++++++++

>>> derivation_dict = ldt.dicts.derivation.DerivationAnalyzer()
>>> derivation_dict.analyze("kindness")
{'original_word': ['kindness'],
 'other': [],
  'prefixes': [],
  'related_words': ['kindhearted', 'kindly', 'in kind', 'kindliness', 'kinda', 'many-kinded', 'first-of-its-kind', 'kind of', 'kindful', 'kindless'],
  'roots': ['kind'],
  'suffixes': ['-ness']}

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Reliable lemmatization with productive rules and Wiktionary/BabelNet:
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

WordNet lemmatizer is limited by the size of its lexical base, even when
the morphological pattern is straightforward.

>>> morph_metadict = ldt.dicts.morphology.MorphMetaDict()
>>> morph_metadict.lemmatize("GPUs")
['GPU']

+++++++++++++++++++
Input normalization
+++++++++++++++++++

Vector neighborhoods are often full of pre-processing noise and misspellings. LDT does its best to clean up some straightforward cases:

>>> analyzer = ldt.dicts.normalize.Normalization()
>>> analyzer.normalize("%grammar")
{'lemmas': ['grammar'],
 'found_in': ['wordnet'],
 'word_categories': ['Misspellings'],
 'pos': ['noun']}
>>> analyzer.normalize("gram-mar")
{'found_in': ['wordnet'],
 'lemmas': ['grammar'],
 'word_categories': ['Misspellings'],
 'pos': ['noun']}
>>> analyzer.normalize("grammarlexicon")
{'found_in': ['wordnet'],
'lemmas': ['grammar', "lexicon],
'word_categories': ['Misspellings'],
'pos': ['noun']}

LDT also provides the option of correction of frequent misspelling patterns
(only for high-certainty cases):

>>> spellchecker_en = ldt.dicts.spellcheck.SpellcheckerEn()
>>> spellchecker_en.spelling_nazi("abritrary")
'arbitrary'

.. inclusion-marker-end-do-not-remove

-----------
Quick links
-----------

 * `Installation instructions <https://ldt.readthedocs.io/Tutorial/installation.html>`_
 * `Project website <ldtoolkit.space>`_
 * `Tutorial <https://ldt.readthedocs.io/Tutorial/index.html>`_
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
goes. LDT supports BabelNet, the largest multilingual dictionary resource available -
so everything they have is retrievable. Many of the other LDT modules (particularly morphology)
are language-specific, and only English is fully supported at
the moment. However, the infrastructure for adding other languages is already
in place, so if you can find or create e.g. lists of affixes for your
language, development would be easy. Get in touch if you'd like to get
involved.

Legal caveat: LDT is open-source free software. No hamsters were harmed in its production,
and no harm should come from its usage. However, no guarantees of any kind.

