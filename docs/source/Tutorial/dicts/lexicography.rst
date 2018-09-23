=======================
Lexicographic resources
=======================

LDT provides a unified interface to WordNet (via `NLTK <http://nltk.org>`_), Wiktionary (via `wiktionaryparser <https://github.com/Suyash458/WiktionaryParser>`_), Wikisaurus (via custom parser) and BabelNet (via BabelNet's API). Note that all of these resources except NLTK are currently queried online, so running large experiments may take time.

Wiktionary, Wikisaurus and BabelNet are multilingual resources. The default query language is read from the :doc:`configuration file <../resources/configuration>` or specified at dictionary initialization. For WordNets, only the English WordNet is currently integrated.

The general workflow for accessing these resources is as follows:

 1) create a dictionary object;
 2) query that dictionary with unified method names.

Each dictionary provides at least 3 common methods:

 1) `dictionaryobject.is_a_word("word")`: returns True is a word is found in a given resource;
 2) `dictionaryobject.get_relation("word", relation="synonyms")`: returns a lists of related words as values;
 3) `dictionaryobject.get_relations("word", relations=["synonyms", "antonyms"])`: returns a dictionary with relation types as keys and lists of related words as values. If no relations argument is specified, all available information is returned (proceed with caution in case of BabelNet).

--------------------------------------------------------
Lexicographic relations supported by different resources
--------------------------------------------------------

+--------------------+---------+------------+------------+----------+
| Relation           | WordNet | Wiktionary | Wikisaurus | BabelNet |
+====================+=========+============+============+==========+
| Synonyms           |    O    |    O       |    O       |    O     |
+--------------------+---------+------------+------------+----------+
| Antonyms           |    O    |    O       |    O       |    O     |
+--------------------+---------+------------+------------+----------+
| Hyponyms           |    O    |    O       |    O       |    O     |
+--------------------+---------+------------+------------+----------+
| Hypernyms          |    O    |    O       |    O       |    O     |
+--------------------+---------+------------+------------+----------+
| Meronyms           |    O    |    O       |    O       |    O     |
+--------------------+---------+------------+------------+----------+
| Part_meronyms      |    O    |            |            |          |
+--------------------+---------+------------+------------+----------+
| Substance_meronyms |    O    |            |            |          |
+--------------------+---------+------------+------------+----------+
| Member_meronyms    |    O    |            |            |          |
+--------------------+---------+------------+------------+----------+
| Holonyms           |         |    O       |    O       |    O     |
+--------------------+---------+------------+------------+----------+
| Troponyms          |         |    O       |    O       |          |
+--------------------+---------+------------+------------+----------+
| Coordinate terms   |         |    O       |    O       |          |
+--------------------+---------+------------+------------+----------+
| Other              |         |    O       |    O       |    O     |
+--------------------+---------+------------+------------+----------+

Synonyms, antonyms, meronyms, hyponyms, and hypernyms are supported by all resources, and can be be retrieved with the relations="main" argument of `get_relations` function.

-------
WordNet
-------

The LDT interface to Princeton WordNet relies on `NLTK library <http://www.nltk.org/howto/wordnet.html>`_, which provides much more fine-grained access to the resource. The goal of this module is only to provide a unified interface to the functions needed for LDT, making it easier to combine with other resources.

Initiate your dictionary:

>>> wordnet = ldt.dicts.semantics.WordNet()

Check if a word entry exists:

>>> wordnet.is_a_word("cat")
True

Retrieve lists of words related to the query word with a specified relation(s):

>>> wordnet.get_relation("cat", relation="hypernyms")
['excrete', 'feline', 'flog', 'gossip', 'man', 'stimulant', 'tracked_vehicle', 'whip', 'woman', 'x-raying']

Note that the resulting lists conflate hypernyms for every synset and ever part of speech of *cat*, so "feline", "woman", "x-raying", "whip", "gossip" etc. are all included. The lists are sorted alphabetically. LDT assumes standard sense-insensitive word embeddings, and takes the most generous scoring position: a model is rewarded for capturing any related word. Of course, this view may be overly generous, especially since not all WordNet senses are active in the popular web-crawled corpora and Wikipedia.

Note:

  LDT provides an option to further expand these lists by also retrieving words, related in the specified way to all the synonyms of the query word:

  >>> wordnet.get_relation("white", relation="antonyms")
  ['black', 'blacken']
  >>> wordnet.get_relation("white", relation="antonyms", synonyms=True)
  ['black', 'blacken', 'bloody', 'dirty', 'unclean']

  This option is off by default.

>>> wordnet.get_relation("cat", relations=["synonyms", "hypernyms"])
{'hypernyms': ['excrete', 'feline', 'flog', 'gossip', 'man', 'stimulant', 'tracked_vehicle', 'whip', 'woman', 'x-raying'],
 'synonyms': ['african_tea', 'arabian_tea', 'barf', 'be_sick', 'big_cat', 'bozo', 'cast', 'cat', "cat-o'-nine-tails", 'caterpillar', 'chuck', 'computed_axial_tomography', 'computed_tomography', 'computerized_axial_tomography', 'computerized_tomography', 'ct', 'disgorge', 'guy', 'hombre', 'honk', 'kat', 'khat', 'puke', 'purge', 'qat', 'quat', 'regorge', 'regurgitate', 'retch', 'sick', 'spew', 'spue', 'throw_up', 'true_cat', 'upchuck', 'vomit', 'vomit_up']}

----------
Wiktionary
----------

Wiktionary is the largest freely available dictionary resource, but also the least structured, which makes the parsing a challenge. LDT currently relies on `wiktionaryparser <https://github.com/Suyash458/WiktionaryParser>`_, and the output may be noisy.

To reduce the load on Wiktionary servers, and to speed up retrieval, LDT configuration file provides an option to cache the list of page titles, so that only words in that list will be queried from the server. If this option is set to True, upon initialization of a Wiktionary dictionary object LDT will automatically download the latest version of that list for the specified language from the servers. The timestamped cache files are saved in the cache subfolder of ldt resource folder, the path to which is specified in the :doc:`configuration file <../resources/configuration>`.

>>> wiki_fr = ldt.dicts.semantics.Wiktionary(language="fr", cache=True)
Loading wiktionary cache.
Updating wiktionary cache.
Wiktionary vocab list successfully cached as /your/ldt/folder/cache/2018-9-22_fr_wiktionary.vocab

It is these cache files that are at the moment used to confirm the existence of an entry for a given word:

>>> wiki_fr.is_a_word("chatte")
True

Note:

   The Wiktionary cache list should NOT be used by itself to determine whether a word exists in a given language, because Wiktionaries for all languages generally aim to include words from all other languages.

>>> wiki_en = ldt.dicts.semantics.Wiktionary(cache=False)
>>> wiki_en.get_relation("white", relation="synonyms"
['pale', 'fair']

If no relations argument is specified, LDT retrieves all possible lexicographic information for the word.

>>> wiki_en.get_relations("white")
{'antonyms': ['tanned', 'unwhite', 'nonwhite', 'black'],
 'synonyms': ['pale', 'fair']}

----------
Wikisaurus
----------

Wiktionary Thesaurus (previously known as Wikisaurus) is a relatively new addition to Wiktionary, and is not very large at the moment. As of now, the English version contains about 200 entries.

Wikisaurus module has all the same syntax and relations as Wiktionary. As the resource is not large, using cache to avoid querying non-existent pages is highly recommended.

>>> wikisaurus_en = ldt.dicts.semantics.Wikisaurus(language="en", cache=True)
Loading wiktionary cache.
Updating wiktionary cache.
Wiktionary vocab list successfully cached as /your/ldt/folder/cache/2018-9-22_en_wikisaurus.vocab
>>> wikisaurus.en.is_a_word("cat")
True
>>> wikisaurus.en.get_relations("cat", relations="all")
{'synonyms': ['tabby', 'puss', 'cat', 'kitty', 'moggy', 'housecat', 'malkin', 'kitten', 'tom', 'grimalkin', 'pussy-cat', 'mouser', 'pussy', 'queen', 'tomcat', 'mog'],
 'hyponyms': [],
 'hypernyms': ['mammal', 'carnivore', 'vertebrate', 'feline', 'animal', 'creature'],
 'antonyms': [],
 'meronyms': []}

--------
BabelNet
--------

To use BabelNet you will need to sign up for a user key (register at https://babelnet.org/register). There are daily usage limits for free users (up to 1000 queries ("babelcoins") per day by default, can be extended to 50, 000 for academic users by request). Commercial version also available.

The way BabelNet API works, only ids for nodes related to query word, and edges per one node can be obtained in one request. This makes retrieval of all words related to the target word an expensive operation, as lemmas for all related ids have to be queried individually. We recommend to use WordNet/Wiktionary for the entries that they do contain, and fall back on BabelNet as last resort.

Also, while BabelNet is much larger than any other resource, its aggregated nature makes its internal organization less reliable; in particular, relation categories have been inconsistent in our experience.

>>> babelnet = ldt.dicts.semantics.BabelNet(language="en")
>>> babelnet.is_a_word("cat")
True

The basic BabelNet methods are `get_edges`, `get_ids` and `get_lemmas`. Each of them counts as one BabelNet API query.

>>> babelnet.get_ids("cat")
['bn:00516031n', 'bn:09370384n', 'bn:14601862n', 'bn:00016608n', 'bn:02464463n', 'bn:00016606n', 'bn:00016624n', 'bn:01369919n', 'bn:00840476n', 'bn:03124841n', 'bn:00016644n', 'bn:02081887n', 'bn:12834386n', 'bn:03493520n', 'bn:01503037n', 'bn:17731028n', 'bn:02442292n', 'bn:21661726n', 'bn:03176292n', 'bn:03638482n', 'bn:13749367a', 'bn:04706109n', 'bn:07075325n', 'bn:03617868n', 'bn:01301887n', 'bn:00012592n', 'bn:00054399n', 'bn:00662304n', 'bn:00735860n', 'bn:15531094n', 'bn:01739170n', 'bn:03488992n', 'bn:19780789n', 'bn:00016609n', 'bn:00010309n', 'bn:00016607n', 'bn:00083115v', 'bn:04014406n', 'bn:00016625n', 'bn:00001844n', 'bn:00016610n', 'bn:00016741n', 'bn:00482617n', 'bn:00084643v', 'bn:03800650n', bn:17765459n', 'bn:17551416n', 'bn:15639460n']
>>> babelnet.get_lemmas("bn:00516031n")
['alternative_versions_of_kitty_pryde', 'alternate_versions_of_kitty_pryde', 'cat', 'ultimate_shadowcat']
>>> babelnet.get_edges("bn:00083115v")
{'other': ['bn:00090052v', 'bn:00008567n', 'bn:00027565n', 'bn:00030543n', 'bn:00043459n', 'bn:00071414n', 'bn:00073300n', 'bn:00022162n', 'bn:00012886n', 'bn:00056135n'],
 'hypernyms': ['bn:00087499v', 'bn:00087499v'],
 'hyponyms': [],
 'meronyms': [],
 'holonyms': [],
 'synonyms': [],
 'antonyms': ['bn:00090052v']}

Aggregating all lemmas per relation thus requires first retrieving ids for the query word, then edges for all of these ids, and then lemmas for all of them. That takes both time and your daily babelcoins. Proceed with caution.

>>> babelnet.get_relations("senator", relations=["hypernyms"])
# this call is equivalent to babelnet.get_relation("senator", relation="hypernyms")
{'hypernyms': ['legislative_assembly', 'metropolitan_see_of_milan', 'poltician', 'legislative_seat', 'senator_of_rome', 'band', 'the_upper_house', 'polictian', 'patres_conscripti', 'musical_ensemble', 'presbytery', 'politician', 'pol', 'solo_project', 'policymaker', 'political_figure', 'politican', 'policymakers', 'archbishop_emeritus_of_milan', 'deliberative_assemblies', 'ensemble', 'career_politics', 'soloproject', 'list_of_musical_ensembles', 'legislative', 'roman_senators', 'archbishopric_of_milan', 'politicain', 'rock_bands', 'section_leader', 'musical_organisation', 'music_band', 'four-piece', 'roman_catholic_archdiocese_of_milan', 'upper_house', 'archdiocese_of_milan', 'band_man', 'milanese_apostolic_catholic_church', 'legistrative_branch', 'group', 'solo-project', 'music_ensemble', 'law-makers', 'roman_senator', 'legislative_arm_of_government', 'solo_act', 'patronage', 'roman_catholic_archbishop_of_milan', 'bar_band', 'senate_of_rome', 'deliberative_body', 'see_of_milan', 'legislative_fiat', 'musical_group', 'ambrosian_catholic_church', 'legislature_of_orissa', 'legislative_branch_of_government', 'list_of_politicians', 'senatorial_lieutenant', 'roman_catholic_archdiocese_of_milano', 'legislature_of_odisha', 'bandmember', 'assembly', 'archdiocese_of_milano', 'bishop_of_milan', 'ensemble_music', 'solo_musician', 'musical_duo', 'legislative_branch_of_goverment', 'first_chamber', 'politicians', 'legislative_bodies', 'political_leaders', 'politico', 'music_group', 'legislative_body', 'career_politician', 'legislature', 'rock_group', 'legislative_power', 'diocese_of_milan', 'musical_ensembles', 'musical_organization', 'revising_chamber', 'archbishops_of_milan', 'political_leader', 'deliberative_assembly', 'conscript_fathers', 'five-piece', 'catholic_archdiocese_of_milan', 'pop_rock_band', 'senatrix', 'deliberative_organ', 'polit.', 'roman_senate', 'legislative_politics', 'bishopric_of_milan', 'legislative_branch', 'musical_band', 'archbishop_of_milan', 'legislatures', 'general_assembly', 'musical_groups', 'instrumental_ensemble', 'politition', 'patres', 'upper_chamber', 'solo-act', 'conscripti', 'legislator']}

Babelcoins cost of this query: 30.

--------------
MetaDictionary
--------------

LDT's ``MetaDictionary`` class provides a way to combine information from different dictionaries in different ways. Strictly speaking, both WordNet and Wiktionary are already included in BabelNet, so just that resource should be sufficient (and Wiktionary parsing in BabelNet may be better). However, it does come with query limits (up to 50,000 per day for non-profit research). MetaDictionary provides a way to use WordNet and Wiktionary whenever possible, and to fall back to BabelNet only when a word is missing in both of these resources.

MetaDictionary is initialized with a list of dictionaries (``order`` option) that specifies the order in which they should be queried.

>>> metadictionary = ldt.dicts.metadictionary.MetaDictionary(language="English", order=['wordnet', 'wiktionary', "babelnet"])

The methods of ``MetaDictionary`` have an additional boolean option ``minimal``. If set to True, the querying stops at the first resource in which an entry is found. WordNet is the least computationally expensive, with wiktionary and babelnet following suit, so this is the recommended order.

Unlike the methods for individual dictionary resources, ``is_a_word()`` method of ``MetaDictionary`` returns not a boolean, but a list of resources in which entries for the queried word were found.

>>> metadictictionary.is_a_word("cat", minimal=True)
# since the entry is found in WordNet, no queries to either Wiktionary or BabelNet are made
["wordnet"]
>>> metadictictionary.is_a_word("cat", minimal=False)
['wordnet', 'wiktionary', 'babelnet']

Likewise, with the ``minimal`` option querying for related words stops at the first resource in which an entry was found.

>>> metadictictionary.get_relation("senator", relation="hypernyms", minimal=True)
['legislator']
>>> metadictictionary.get_relation("senator", relation="hypernyms", minimal=False)
['ambrosian_catholic_church', 'archbishop_emeritus_of_milan', 'archbishop_of_milan', 'archbishopric_of_milan', 'archbishops_of_milan', 'archdiocese_of_milan', 'archdiocese_of_milano', 'assembly', 'band', 'band_man', 'bandmember', 'bar_band', 'bishop_of_milan', 'bishopric_of_milan', 'career_politician', 'career_politics', 'catholic_archdiocese_of_milan', 'conscript_fathers', 'conscripti', 'deliberative_assemblies', 'deliberative_assembly', 'deliberative_body', 'deliberative_organ', 'diocese_of_milan', 'ensemble', 'ensemble_music', 'first_chamber', 'five-piece', 'four-piece', 'general_assembly', 'group', 'instrumental_ensemble', 'law-makers', 'legislative', 'legislative_arm_of_government', 'legislative_assembly', 'legislative_bodies', 'legislative_body', 'legislative_branch', 'legislative_branch_of_goverment', 'legislative_branch_of_government', 'legislative_fiat', 'legislative_politics', 'legislative_power', 'legislative_seat', 'legislator', 'legislature', 'legislature_of_odisha', 'legislature_of_orissa', 'legislatures', 'legistrative_branch', 'list_of_musical_ensembles', 'list_of_politicians', 'metropolitan_see_of_milan', 'milanese_apostolic_catholic_church', 'music_band', 'music_ensemble', 'music_group', 'musical_band', 'musical_duo', 'musical_ensemble', 'musical_ensembles', 'musical_group', 'musical_groups', 'musical_organisation', 'musical_organization', 'patres', 'patres_conscripti', 'patronage', 'pol', 'polictian', 'policymaker', 'policymakers', 'polit.', 'politicain', 'political_figure', 'political_leader', 'political_leaders', 'politican', 'politician', 'politicians', 'politico', 'politition', 'poltician', 'pop_rock_band', 'presbytery', 'revising_chamber', 'rock_bands', 'rock_group', 'roman_catholic_archbishop_of_milan', 'roman_catholic_archdiocese_of_milan', 'roman_catholic_archdiocese_of_milano', 'roman_senate', 'roman_senator', 'roman_senators', 'section_leader', 'see_of_milan', 'senate_of_rome', 'senator_of_rome', 'senatorial_lieutenant', 'senatrix', 'solo-act', 'solo-project', 'solo_act', 'solo_musician', 'solo_project', 'soloproject', 'the_upper_house', 'upper_chamber', 'upper_house']

