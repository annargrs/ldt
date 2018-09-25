============================================================
Extra resources for establishing relations in pairs of words
============================================================

-------------
What LDT does
-------------

LDT provides some additional resources that, unlike the resources described in section :ref:`Linguistic resources in LDT`, take two words as input, and output either a binary value or a score indicating the presence/strength of the relation between these two words. Most of them have a `are_related("word1", "word2")` method.

------------
Associations
------------

LDT's associations dictionary file is a combination of `University of South Florida Free Association norms <http://w3.usf.edu/FreeAssociation/>`_ and `Edinburgh Associative Thesaurus <http://rali.iro.umontreal.ca/rali/?q=en/Textual%20Resources/EAT>`_. You can use this dictionary as a standalone resource as follows:

>>> associations_dict = ldt.dicts.resources.AssociationDictionary()
>>> associations_dict.are_related("cat", "dog")
True

While association relation in psychology is directional, LDT ignores this crucial property, as in its use case (testing word embedding models) it is not clear what direction (from target to neighbor word or vice versa) should be preferred, if any.

>>> associations_dict.are_related("falcon", "eagle")
True
>>> associations_dict.are_related("eagle", "falcon")
True

-------------
Ontology path
-------------

Ontology is currently limited to wordnet's synsets relations, and the implementation relies on the NLTK's :meth:`~nltk.corpus.reader.wordnet.Synset.path_similarity` method. Crucially, it is a relation between synsets, i.e. you need to know which senses of two words you're dealing with. In LDT's use case of sense-insensitive word embeddings the idea is to assume the best. LDT takes the input strings, finds all the synsets for them and goes through the path similarities between all of them, outputting the lowest ranking value.

You can use this dictionary as a standalone resource as follows:

>>> wn_similarity = ldt.relations.OntoDict()
>>> wn_similarity.get_shortest_path("cat", "dog")
0.05

Note:

   NLTK's :meth:`~nltk.corpus.reader.wordnet.Synset.path_similarity` method is not particularly fast, and in our experiments it occasionally got stuck for hours on some very common words with numerous synsets. Thus LDT implementation provides an additional timeout check: if a wuery is not completed in 10 seconds, it is abandoned.

---------------------
Derivational antonymy
---------------------

LDT relies on lexicographic resources to detect antonymy relation, but in many cases they fail to list antonyms that are relatively easy to detect with productive derivational patterns, such as *feminist* and *anti-feminist*.

Since this obviously requires derivational analysis to have been performed, this resource takes ldt.Word objects as input. If input is a string, the Word objects are constructed.

You can use this dictionary as a standalone resource as follows:

>>> antonymy_by_derivation = ldt.relations.DerivationalAntonymy(language="en")
>>> antonymy_dict.are_related("regular", "irregular")
True

Only purely derivational relations are considered by this resource, so it will return False for lexical antonyms. Both sources of knowledge are combined in :meth:`~ldt.relations.RelationsInPair` class.

>>> antonymy_dict.are_related("black", "white")
False

Note that this resource takes a rather lax view of antonymy relation (e.g. "heartless" is not strictly speaking an antonym of "heart", but of "caring". However, a clause like "he has a good heart" could be viewed as opposite to "he is heartless", and a distributional meaning model should arguably be rewarded for capturing this relation. For now, you can fine-tune this resource by editing the list of language-specific prefixes and suffixes in :meth:`~ldt.relations.antonymy_by_derivation`.
