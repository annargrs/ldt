# -*- coding: utf-8 -*-
"""Text formatting functions

This section includes a few helper functions for formatting different
spelling variants.

"""



def remove_text_inside_brackets(text, brackets="()[]"):
    '''
    A helper function for :func:`get_relations`, code from `here
    <https://stackoverflow.com/questions/14596884/remove-text-between-and-in-python>`_

    Args:
        text (str): the text to clean from brackets
        brackets: the list of symbols counting as brackets

    Returns:
        (str): cleaned-up text
    '''


    count = [0] * (len(brackets) // 2)  # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b:  # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1) ** is_close  # `+1`: open, `-1`: close
                if count[kind] < 0:  # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else:  # character is not a [balanced] bracket
            if not any(count):  # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars).strip()

def get_spacing_variants(word):

    '''
    A helper function for :func:`get_relations` that, given a
    string spaced input, produces a list of different spelling versions of
    this word (e.g. ["good night", "good-night", "good_night"])

    Args:
        word (str): input word

    Returns:
        (list): a list of variants: spaced, dashed and underscored
    '''

    res = []
    res.append(word)
    res.append(word.replace(" ", "_"))
    res.append(word.replace(" ", "-"))
    return res

def strip_non_alphabetical_characters(word, ignore=None):
    """Helper function for removing any non-alphabetical character with optional exclusion list.

    Wiktionary etymologies are a mess to parse. This function attempts to extra clean-up cases like *(-ness* or *"king+*. Optionally, it will return only strings that are known determined to be words by :func:`noise.is_a_word`.

    Args:
        word (str): a potential word string to process
        ignore (tuple): the characters to not strip (e.g. "-")

    Returns:
        str: cleaned up string (a potential word)

    """
    if not word:
        return None

    if word.isalpha():
        return word
    else:
        stripped = ""
        for i in range(len(word)):
            if i == 0 or i == len(word) - 1:
                try:
                    if word[i].isalpha() or word[i] in ignore:
                        stripped += word[i]
                except TypeError:
                    pass
            else:
                try:
                    if word:
                        if word[i] in ignore or word[i].isalpha():
                            stripped += word[i]
                except TypeError:
                    pass
        return "".join(stripped)

def dash_suffix(suffix):
    """A helper function for custom derivation dicts.

    Some suffixes are mostly spelled with a dash (e.g. *tree-like*), and some
    may be spelled with a dash for stylistic reasons (e.g. *work-able*).
    This function ensures that both ways are tracked.

    Args:
        suffix (str): suffix to be dashed or not

    Returns:
        suffix (str): a dashed suffix

    """
    if suffix.startswith("-"):
        return suffix
    else:
        return "-" + suffix

def rreplace(word, old_suffix, new_suffix):
    """Helper for right-replacing suffixes"""
    return new_suffix.join(word.rsplit(old_suffix, 1))

def _check_res(res):
    """Helper for avoiding empty dictionary as function argument in
    morphological dictionaries"""
    if not res:
        res = {
            "suffixes": [], "prefixes": [], "roots": [], "other": [],
            "original_word": []
            }
    return res