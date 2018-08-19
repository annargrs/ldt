# -*- coding: utf-8 -*-
""" This module brings together multiple resources for either:

 * confirming that a word is found in resources;
 * confirming that the word is of a category that excludes its being in
   resources (e.g. it is a proper noun, a foreign word or a number);
 * attempting to lemmatize by productive rules;
 * attempting to normalize the spelling.

Examples:
    >>> test_dict.normalize("#cat")
    {is_standard: False, "lemmas": ["cat"], "word_categories": ["hashtag"],
    "found_in": ["WordNet"]}
    >>> test_dict.normalize("cat")
    {"lemmas": ["cat"], "word_categories": ["hashtag"]}

Todo:
    * creation of default config file upon installation
    * the right error path in NLTK tokenizer
    * add .citation property, and print it out on initialization
        WordNet 1.5, NLTK implementation. Use .citation to get the full
        citation for this resource.
"""

# trying to clean up




@functools.lru_cache(maxsize=None)
def analyze(word):
    '''
    :param word: an ldt.word object
    :return: object with modified spellings, is_misspelled and is_lemmatized attributes
    '''
    wordform = str(word.original_spelling)
    spellings = []
    if not contains_a_letter(wordform):
        word.is_noise.append(True)
        return word
    #if contains trash, clean up
    if contains_fishy_punctuation(wordform):
        # TODO dots in filenames and extensions
        candidate = turn_to_word(wordform)
        candidates = turn_to_words(wordform)
        if candidate == None:
            word.has_extension = True
        else:
            word.has_extension = False
            if len(candidate) > 0:
                word.is_misspelled = True
#            print(1, candidate)
                spellings+=candidate
        if candidates != None:
#            print(2, candidates)
            if word.has_extension:
                candidates = candidates[:-1]
                word.is_misspelled = False
            for variant in candidates:
                if variant != None:
                    if len(variant) > 0:
                        if not variant in stopWords:
                            check = check_cleaned_up_variant(variant, word, l="derivation")
                            if check != None:
                                word = check
                            if not word.has_extension:
                                word.is_misspelled = True
    else:
        #TODO append british / american spellings
        spellings.append(wordform)
    #now proceed with a spellings list without punctuation trash
    for variant in spellings:
        if variant != None:
            if len(variant) > 0:
                #print("\nprocessing the variant: ", variant)

                check = check_cleaned_up_variant(variant, word, l = "spellings")
                if check != None:
                    word = check


                #try splitting a compound or misspelling:

                split = split_a_compound(variant)
                if split != False:
                    #print("splitted: ", split)
                    word.is_misspelled=True
                    for w in split:
                #         print(w)
                        check = check_cleaned_up_variant(w, word, l = "derivation")
                        if check != None:
                            word = check
                            #print("here", word.spellings)
                    try_hyphenating = "-".join(split)
                    check = check_cleaned_up_variant(try_hyphenating, word, l="spelling")
                    if check != None:
                        word = check
                        word.is_misspelled = True
                    try_underscore = "_".join(split)
                    check = check_cleaned_up_variant(try_underscore, word, l="spelling")
                    if check != None:
                        word = check
                        word.is_misspelled = True
            #
            # if all failed, try to spellcheck and check for foreign words
                if len(word.spellings) == 0 and len(word.stems) == 0:
                    for variant in spellings:
                        if len(spellings) == 1:
                            if not is_english(variant):
                                word.is_foreign = True
                            if ldt.dicts.cleanup.spellchecker.check_if_foreign(variant):
                                word.is_foreign = True
                            #else:
                                #word.is_foreign = False
                    #only do "safe" spellchecking when there's less chance to get it wrong:
                        if not word.is_foreign:
                            if abs(len(variant) - len(word.original_spelling)) < 2:
                                variant = ldt.dicts.cleanup.spellchecker.spellcheck(variant , confidence = True)
                                if variant:
                                    check = check_cleaned_up_variant(variant, word, l="spellings")
                                    if check != None:
                                        word = check
                                        word.is_misspelled = True
    #for now just make tags unique
    word.is_a_lemma = list(set(word.is_a_lemma))
    word.affixes = list(set(word.affixes))
#    print("\n\n")
    return word