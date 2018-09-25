==============================
Parts of speech and word forms
==============================

-------------
What LDT does
-------------

LDT provides a unified way to access part-of-speech information in WordNet, Wiktionary and BabelNet. At the moment, only BabelNet information is reliably multilingual, but for English everything should work.

LDT also utilizes the above resources, `inflect module <https://pypi.org/project/inflect/>`_ and custom rules for lemmatization. Codes for different morphological word forms are not supported yet.

-----------------------------------------------------------
Lemmatization and retrieval of POS information with WordNet
-----------------------------------------------------------

A list of possible POSes for a given lemma, together with number of senses per POS can be accessed as follows:

>>> morph_wn = ldt.dicts.morphology.MorphWordNet()
>>> morph_wn.get_pos("cat")
{'noun': 8, 'verb': 2}

:meth:`~ldt.dicts.morphology.wordnet.en.MorphWordNet.lemmatize()` method
returns the lemma of the query word, or the word if it is already a lemma:

>>> morph_wn.lemmatize("cat")
['cat']
>>> morph_wn.lemmatize("cats")
['cat']
>>> morph_wn.lemmatize("cats")
['cat']

Since lemmatization has to be context-independent, all possible lemmas are looked up. For example, some verbs may have independent entries as gerunds, while others lack them.

>>> morph_wn.lemmatize("writing")
['write', 'writing']
>>> morph_wn.lemmatize("recognizing")
['recognize']

---------------------------------------------------------
Retrieval of POS information from Wiktionary and BabelNet
---------------------------------------------------------

POS information together of number of senses per POS can be retrieved in the same way as with WordNet:

Wiktionary:

>>> morph_wiki = ldt.dicts.morphology.MorphWiktionary(language="en")
>>> morph_wiki.get_pos("cat")
{'verb': 2, 'noun': 8, 'adjective': 1}

BabelNet:

>>> morph_bn = ldt.dicts.morphology.MorphBabelNet(language="en")
>>> morph_bn.get_pos("cat")
{'noun': 45, 'adjective': 1, 'verb': 2}

(this takes only 1 query, i.e. babelcoin)

Note: BabelNet and Wiktionary use different POS tagsets. BabelNet relies on `Universal POS tags <https://babelnet.org/4.0/javadoc/com/babelscape/util/UniversalPOS.html>`_, while Wiktionary categories are presumably those listed on `this page <https://en.wiktionary.org/wiki/Category:en:Parts_of_speech>`_. Pending further analysis, LDT brings all the basic POS tags for English to their traditional full names.

As for lemmatization, neither Wiktionary nor BabelNet support lookup in non-lemmatized forms. Theoretically, that could be used to check whether a word is a lemma:

>>> morph_wiki.lemmatize("recognizing")
None
>>> morph_wiki.lemmatize("recognize")
['recognize']

However, Wiktionary generally aims to have a separate page for each word form, and for many words this has been accomplished, which would throw the above crude filter off. BabelNet has even more of such entries.

>>> morph_wiki.lemmatize("cats")
['cats']

A better workflow would be as follows: use productive inflection patterns to try to un-inflect words and then confirm their existence in Wiktionary/BabelNet. See the following section for rule-based lemmatization for English.

------------------------------------
Custom LDT lemmatization for English
------------------------------------

LDT relies on `inflect module <https://pypi.org/project/inflect/>`_ to un-inflect potential non-lemmas. Only words with regular endings (*-ed*, *-s* etc.) are processed; any irregular forms should be already in WordNet. Since this is rule-based and therefore less reliable, it should only be applied for entries missing in when WordNet.

The general syntax is the same:

>>> morph_custom = ldt.dicts.morphology.MorphCustomDict()
>>> morph_custom.lemmatize("cats")
['cat']

:class:`~ldt.dicts.morphology.custom.en.MorphCustomDict` takes an optional
``dictionary`` argument that specifies the resource where the existence of
potential lemmas should be checked. This can be Wiktionary or BabelNet.

For example, WordNet does not have an entry for `GPU`, and therefore cannot
un-inflect the plural of this word:

>>> morph_wn.lemmatize("GPUs")
[]

However, this can be done falling back on Wiktionary:

>>> wiki = ldt.dicts.morphology.MorphWiktionary(language="en")
>>> morph_custom = ldt.dicts.morphology.MorphCustomDict(dictionary=wiki)
>>> morph_custom.lemmatize("GPUs")
['GPU']

--------------------------------------------
MetaDictionary for morphological information
--------------------------------------------

In case of retrieving POS information the basic idea for
:class:`ldt.dicts.morphology.meta.MorphMetaDict` is
the same as for the metadictionary class that combines lexicographic
information across resources. Depending on your needs and usage quotas, it
provides a way to stop at the first resource in which an entry is found, and
 to not query further. The hierarchy of dictionaries is set with the order parameter.

>>> morph_metadict = ldt.dicts.morphology.MorphMetaDict(language="English", order=("wordnet", "wiktionary", "babelnet"), custom_base="wiktionary")

By default the queries are "minimal":

>>> morph_metadict.is_a_word("cat")
['wordnet']
>>> morph_metadict.get_pos("cat")
['noun', 'verb']

Use `minimal=False` option to get combined information from all resources:

>>> morph_metadict.is_a_word("cat", minimal=False)
['wordnet', 'wiktionary', 'babelnet']
>>> morph_metadict.get_pos("cat", minimal=False)
['adjective', 'noun', 'verb']

In case of lemmatization the behavior is different. MorphMetaDict is initialized with additional `custom_base` option that specifies which resource should be used for lemmatizing potential inflected words that are not found in WordNet. This resource has to be included in the `order` list. By default it is Wiktionary. As described above, the resulting object combines the rule-based heuristics with larger lexical base of Wiktionary/BabelNet to successfully lemmatize new words not found in WordNet.

>>> morph_metadict = ldt.dicts.morphology.MorphMetaDict(language="English", order=("wordnet", "wiktionary", "babelnet"), custom_base="wiktionary")
>>> morph_metadict.lemmatize("GPUs")
['GPU']


