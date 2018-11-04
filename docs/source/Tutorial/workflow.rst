=============================
The overall idea and workflow
=============================

---------------------------------------------
I want to use LDT to evaluate word embeddings
---------------------------------------------

The core of LD methodology is large-scale automatic annotation of relations in word vector neighborhoods. You get your embeddings, you get the vocabulary sample that you want to investigate (or take ours for comparison), and you retrieve *n* neighbor pairs for those words. Then LDT can be used to annotate the files, and the resulting statistics will hopefully tell you what your embedding model is actually doing.

The overall algorithm for initial processing of input words is as follows:

.. figure:: /_static/ldt-scheme_resized.png
   :width: 400px
   :align: center

Section :ref:`Collecting all linguistic information about a word` and section :ref:`Detecting relations in pairs of words` describe how LDT aggregates information from various linguistic resources to achieve automatic annotation of all possible relations in word pairs. Section :ref:`Linguistic resources in LDT` of the tutorial describes the various linguistic resources that you can use and configure in this process.

The next step is :ref:`Running reproducible experiments with LDT`.
Once you install and configure LDT, a starter script with default settings
for English can be run simply as follows:

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

---------------------------------------------------------------------
I don't care about word embeddings, just show me the new dictionaries
---------------------------------------------------------------------

Head over to section :ref:`Linguistic resources in LDT`. A few quick highlights of what LDT can do for you:

Querying WordNet, Wiktionary, Wiktionary Thesaurus and BabelNet:

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
