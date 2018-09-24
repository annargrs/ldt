=====================================================
Collecting all available information for a given word
=====================================================

LDT's :meth:`ldt.relations.Word` class provides a convenient way to configure several resources and combine them for repeated queries. This class outputs a dictionary that records various properties of the queried word.

The first step of this analysis is input normalization described in section :ref:`Normalization and classification of input strings`.

Once a word entry has been detected in one of configured lexicographic resources, LDT collects the words that are related to the queried word with various lexicographic relations. Derivational analysis is also performed to detect both derived words and word stems/affixes.

