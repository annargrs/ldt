========================
Bringing it all together
========================


    >>> test_dict = ldt.dicts.normalize.Normalization(language="English",
                                              order=("wordnet", "custom"),
                                              lowercasing=True)
    >>> test_dict.normalize("grammar")
    {'found_in': ['wordnet'], 'lemmas': ['grammar'], 'word_categories': [
    'Lexicon'], 'pos': ['noun']}
    >>> test_dict.normalize("grammars")
    {'found_in': ['wordnet'], 'lemmas': ['grammar'], 'word_categories': [
    'Lexicon'], 'pos': ['noun']}
    >>> test_dict.normalize("grammarxyz")
    None
    >>> test_dict.normalize("alice")
    {'lemmas': ['alice'], 'word_categories': ['Names'], 'pos': ['noun']}
    >>> test_dict.normalize("grammaire")
     {'word_categories': ['Foreign']}
    >>> test_dict.normalize("gramar")
    {'found_in': ['wordnet'], 'lemmas': ['grammar'], 'word_categories': [
    'Misspellings'], 'pos': ['noun']}
    >>> test_dict.normalize("%grammar")
    {'found_in': ['wordnet'], 'lemmas': ['grammar'], 'word_categories': [
    'Misspellings'], 'pos': ['noun']}
    >>> test_dict.normalize("grammar.com")
    {'word_categories': ['URLs'], 'pos': ['noun']}
    >>> test_dict.normalize("grammar.jpg")
    {'word_categories': ['Filenames'], 'pos': ['noun']}
    >>> test_dict.normalize("gram-mar")
    {'found_in': ['wordnet'], 'lemmas': ['grammar'], 'word_categories': [
    'Misspellings'], 'pos': ['noun']}
    >>> test_dict.normalize("grammar.lexicon")
    {'found_in': ['wordnet'], 'lemmas': ['grammar', "lexicon],
    'word_categories': ['Misspellings'], 'pos': ['noun']}
    >>> test_dict.normalize("grammarlexicon")
    {'found_in': ['wordnet'], 'lemmas': ['grammar', "lexicon],
    'word_categories': ['Misspellings'], 'pos': ['noun']}