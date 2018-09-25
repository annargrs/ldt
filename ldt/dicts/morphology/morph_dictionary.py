# -*- coding: utf-8 -*-
""" Morphological Dictionary class

This module implements the base Morphological dictionary class that is
inherited by classes for resources from which morphological information can be
obtained.

Basic functionality required in any subclass:

    * retrieving POS information of an entry;
    * lemmatization;
    * retrieving morphological form codes

Todo:
    * creation of default config file upon installation
    * the right error path in NLTK tokenizer
    * generating inflected forms with  https://github.com/jazzband/inflect
"""

from abc import ABCMeta, abstractmethod

from ldt.dicts.dictionary import Dictionary
from ldt.load_config import config

class MorphDictionary(Dictionary, metaclass=ABCMeta):
    """A super-class for resources with relations functionality

    """
    # pylint: disable=unused-argument
    def __init__(self, **kw):
        """ Initializing the base class.

        Args:
            lowercasing (bool): *True* if all data should be lowercased
            split_mwu (bool): *True* if in addition to underscored
                spellings of multi-word expressions their dashed and spaced
                versions should also be produced (e.g. 'good night',
                'good_night', "good-night")

        """

        super(MorphDictionary, self).__init__(**kw)

    @abstractmethod
    def get_pos(self, word, formatting):
        """Stub for the method of all subclasses of MorphDictionary that
        returns parts of speech for a given word.

        Args:
            word (str): the word to be looked up
            formatting (str): the format of output:

                *dict* for a dictionary of part-of-speech-tags, with number
                of senses with that POS as values
                *list*: a list of all available POS tags for the word

        Returns:
            (list, dict): part-of-speech tags for the given word

        Todo:
            * pos format
        """

        raise NotImplementedError()

    @abstractmethod
    def lemmatize(self, word):
        """Stub for the method of all subclasses of MorphDictionary that
        returns dictionary form for a given word.

        Args:
            word (str): the word to be looked up

        Returns:
            (list): lemma(s) of the given word

        Todo:
        """

        raise NotImplementedError()

    def get_form(self, word):
        """Stub for the method of all subclasses of MorphDictionary that
        returns morphological form(s) of a given word.

        Args:
            word (str): the word to be looked up

        Returns:
            (list): possible morphological forms for the given word

        Todo:
            * morph form format
        """

        raise NotImplementedError()
        # https://github.com/jazzband/inflect
