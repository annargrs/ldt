=======================
Derivational morphology
=======================

.. contents:: :local:

-------------
What LDT does
-------------

There are surprisingly few comprehensive resources for derivational morphology. For the LDT primary use case (evaluation of word embeddings) this is a less-than-ideal situation for two reasons:

1) Many etymological (derivational) links are missing in dictionary resources, and therefore word embeddings do not get credit for correctly placing such words closer together in the vector space;
2) Most corpora on which word embeddings are trained are large and new (i.e. containing texts written relatively recently). This means that there is likely to be a large number of nonce-words that are simply not yet registered even in the largest dictionaries such as OED. Generally speaking, productive derivational patterns will always produce such nonce-words missing in the resources. Consequently, once again, word embeddings might not receive due credit.

LDT attempts to mitigate this situation in the following ways:

1) collecting "derivationally related words" from WordNet and Wiktionary;
2) trying to parse Wiktionary etymology sections;
3) providing simple rule-based heuristics for analysing potential derivatives.

--------------------------------------------------
Derivational word groups in WordNet and Wiktionary
--------------------------------------------------

Accessing derivational word groups from WordNet is performed as follows:

>>> derivation_wordnet = ldt.dicts.derivation.DerivationWordNet()
>>> derivation_wordnet.get_related_words("kind")
["kindness]

For Wiktionary, the mechanism is the same:

>>> derivation_wiki = ldt.dicts.derivation.DerivationWiktionary(language="en")
>>> derivation_wiki.get_related_words("kind")
['many-kinded',
 'in kind',
 'kind of',
 'kindliness',
 'kindly',
 'kindful',
 'kinda',
 'kindhearted',
 'kindless',
 'first-of-its-kind',
 'kindness']

Due to changes in wiktionaryparser the version is currently frozen at 0.0.7.

----------------------
Wiktionary etymologies
----------------------

WiktionaryParser detects etymology sections in Wiktionary, but they are written in free form, unstructured, and finding the actual roots of words is non-trivial. LDT does its best with a few regular expressions, but no guarantees.

>>> derivation_wiki = ldt.dicts.derivation.DerivationWiktionary(language="en")
>>> derivation_wiki.get_etymologies("lioness")
(['lion'], ['-ess'])

Note that the roots may be Latin, Saxon, Old French etc..
>>> derivation_wiki.get_etymologies("wizard")
(['wys'], ['-ard'])

------------------------------
Productive derivation patterns
------------------------------

``ldt.dicts.derivation.custom_dict.DerivationCustomDict()`` class provides a general language-independent interface for detecting compounds and words with prefixes and suffixes. Extending it to other languages could be as easy as providing the lists of affixes. See the API reference for more details.

For English LDT provides ``EnglishDerivation`` class that combines the above with a few custom methods.

>>> derivation_dict = ldt.dicts.derivation.EnglishDerivation()
>>> derivation_dict.analyze_affixes("antiestablishment")
{'suffixes': ['-ment'],
 'prefixes': ['anti-'],
 'roots': ['establishment', 'establish'],
 'other': [],
 'original_word': ['antiestablishment']}

Most patterns are productive. The list is based on `MorphoQuantics BNC data <http://morphoquantics.co.uk/>`_. In particular, 97 prefixes and 124 suffixes are included at the moment. See ``ldt.dicts.derivation.custom.en`` for an example of language data file.

A few historical patterns are also included:

>>> derivation_dict.analyze_affixes("bleed")
{'suffixes': [],
 'prefixes': [],
 'roots': ['blood', 'bleed'],
 'other': ['root_vowel_n/a>v'],
 'original_word': ['bleed']}

Decomposing compounds is based on search for possible conjoined constituents that are known to be separate words (with the possibility of insertions or replacement patterns in the compounded stems, such as "-s" between comppounded nouns in German). To avoid meaningless decompositions, by default LDT avoids this kind of analysis on short words and constrains the possible decomposition options by minimal stem length (3 by default).

>>> derivation_dict.decompose_compound("toothpaste")
{'suffixes': [],
 'prefixes': [],
 'roots': ['tooth', 'paste'],
 'other': [],
 'original_word': []}

-------------------------
Derivation MetaDictionary
-------------------------

All of the above resources are combined in ``DerivationAnalyzer`` class. It collects derivational families, etymologies and productive affix analysis, and outputs all the information.

>>> derivation_dict = ldt.dicts.derivation.DerivationAnalyzer(language="en")
>>> derivation_dict.analyze("kindness")
{'original_word': ['kindness'],
 'other': [],
  'prefixes': [],
  'related_words': ['kindhearted', 'kindly', 'in kind', 'kindliness', 'kinda', 'many-kinded', 'first-of-its-kind', 'kind of', 'kindful', 'kindless'],
  'roots': ['kind'],
  'suffixes': ['-ness']}

You can also access the decomposition and derivational family separately:

>>> derivation_dict._get_constituents("kindness")
{'suffixes': ['-ness'],
 'prefixes': [],
 'roots': ['kind'],
 'other': [],
 'original_word': ['kindness']}
>>> derivation_dict._get_related_words("kindness")
['first-of-its-kind', 'kinda', 'kindness', 'kindless', 'many-kinded', 'kindly', 'kindliness', 'in kind', 'kindhearted', 'kindful', 'kind of']
