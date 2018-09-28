====================================
Linguistic Diagnostics Toolkit (LDT)
====================================

.. image:: https://travis-ci.com/annargrs/ldt.svg?branch=master
   :target: https://travis-ci.com/annargrs/ldt
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

**Note:** LDT is in active development; all the dictionary functionality is already available. Scripts for running experiments and integration with `vecto library <vecto.space>`_ are coming in the nearest weeks. Make sure you update your installation often!

----------------------
Current functionality
----------------------

LDT provides a unified Python interface for querying a large number of resources for natural language processing, including Wiktionary, BabelNet, WordNet, and a lot of new custom routines. A few quick highlights of the current functionality:

Retrieving related words from WordNet, Wiktionary, Wiktionary Thesaurus and BabelNet:

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

Derivational analysis:

>>> derivation_dict = ldt.dicts.derivation.DerivationAnalyzer()
>>> derivation_dict.analyze("kindness")
{'original_word': ['kindness'],
 'other': [],
  'prefixes': [],
  'related_words': ['kindhearted', 'kindly', 'in kind', 'kindliness', 'kinda', 'many-kinded', 'first-of-its-kind', 'kind of', 'kindful', 'kindless'],
  'roots': ['kind'],
  'suffixes': ['-ness']}

Reliable lemmatization with productive rules and Wiktionary/BabelNet, even for new words:

>>> morph_metadict = ldt.dicts.morphology.MorphMetaDict()
>>> morph_metadict.lemmatize("GPUs")
['GPU']

Correcting (at least some) text pre-processing noise and normalizing the input:

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

Trustworthy correction of frequent misspelling patterns, only for high-certainty cases:

>>> spellchecker_en = ldt.dicts.spellcheck.SpellcheckerEn()
>>> spellchecker_en.spelling_nazi("abritrary")
'arbitrary'

Collecting all the available info about a word with one click:

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

Finding possible relations between a pair of words in one click:

>>> relation_analyzer = ldt.relations.RelationsInPair()
>>> relation_analyzer.analyze("black", "white")
{'Hyponyms': True,
 'SharedMorphForm': True,
 'SharedPOS': True,
 'Synonyms': True,
 'Antonyms': True,
 'ShortestPath': 0.058823529411764705,
 'Associations': True}

The above functionality can be used in many NLP applications and for text pre-processing,
large-scale analysis of potential relations between pairs of words. See ldt.experiments.demo file for a toy example of such an analysis.

That last step can help you predict how your model will do on a particular
task, and also give some ideas about how it can be improved. Check out the
`results of a large-scale experiment with 60 embeddings and 21 datasets.
<http://ldtoolkit.space/analysis/correlation/>`_

.. inclusion-marker-end-do-not-remove

See the `Tutorial and API documentation <https://ldt.readthedocs.io/>`_ for more details on all of these resources.

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

