# -*- coding: utf-8 -*-
""" Extra resources classes

This module implements the base dictionary classes for looking up names,
numbers, stopwords and any other word categories that may be useful and can be
defined as lookup in a simple resource file. Each of these dictionaries only needs
to implement an `is_a_word` method.

Todo:
    * creation of default config file upon installation
    * the right error path in NLTK tokenizer
    * for files and urls, identify words after stripping the extensions
"""

import os
import functools

from abc import ABCMeta, abstractmethod

from ldt.dicts.dictionary import Dictionary as Dictionary
from ldt.helpers.exceptions import DictError as DictError
from ldt.helpers.resources import load_stopwords as load_stopwords
from ldt.helpers.resources import lookup_language as lookup_language
from ldt.helpers.loading import load_resource as load_resource
from ldt.helpers.formatting import get_spacing_variants as get_spacing_variants
from ldt.load_config import config as config

# class LexicographicDictionary(Dictionary, metaclass=ABCMeta):
class ResourceDict(Dictionary):
    """A class for simple resources like vocabulary lists, which only
    require simple lookup."""

    def __init__(self, path=None, resource="names",
                 language=config["default_language"],
                 lowercasing=config["lowercasing"],
                 split_mwu=config["split_mwu"]):
        """ Initializing the vocab lookup class.

        Args:
            lowercasing (bool): *True* if all data should be lowercased
            split_mwu (bool): *True* if in addition to underscored
                spellings of multi-word expressions their dashed and spaced
                versions should also be produced (e.g. 'good night',
                'good_night', "good-night")
            path (str): if str, interpreted as the full direct path to
                the resource to be used (one-column vocab text file expected).
                Otherwise LDT will look for the file in the
                language_resources subfolder of the ldt_resources folder,
                as specified in the deafult config file.
            resource (str): the resource to initialize (if path is a
                dictionary), as indicated in the config file. For example,
                "names", "numbers", "associations".
        """

        super(ResourceDict, self).__init__()
        if len(language) > 2:
            language = lookup_language(language, reverse=True)
        #: the language of the resource
        self.language = language

        if isinstance(path, str):
            self.path=path

        if not path:

            if resource in ["names", "numbers", "associations"]:
                resource_type = "language_resources"
            elif resource in ["freqdict", "vocabulary", "co-occurrence_data"]:
                resource_type = "corpus_resources"

            # if not self.language in path["resources"][resource_type]:
            #     raise DictError("No resources for this language were found, "
            #                     "check your configuration file.")
            path_to_dict = os.path.join(config["path_to_resources"],
                                        resource_type, self.language,
                                        config[resource_type][self.language][
                                            resource])

            #: the path from which the resource is loaded
            self.path = path_to_dict

        try:
            data = load_resource(self.path, format="infer",
                                 lowercasing=lowercasing)
            self.data = data
        except FileNotFoundError:
            print("No resource was found, please check the file path "
                  ""+self.path)



#todo lowercasing and splitting mwus for the whole resource
    @functools.lru_cache(maxsize=None)
    def is_a_word(self, word):
        if word in self.data:
            return True
        return False


class NameDictionary(ResourceDict):
    """A class for language-specific name resources."""

    def __init__(self, language=config["default_language"],
                 lowercasing=config["lowercasing"],
                 split_mwu=config["split_mwu"], path=None, resource="names"):
        """ Initializing the names lookup class.

        Args:
            lowercasing (bool): *True* if all data should be lowercased
            split_mwu (bool): *True* if in addition to underscored
                spellings of multi-word expressions their dashed and spaced
                versions should also be produced (e.g. 'good night',
                'good_night', "good-night")
            path (str, dict): if str, interpreted as the full direct path to
                the resource to be used (one-column vocab text file expected).
                Otherwise LDT will look for the file in the
                language_resources subfolder of the ldt_resources folder,
                as specified in the deafult config file.
        """
        super(NameDictionary, self).__init__(language=language,
                                             lowercasing=lowercasing,
                                             split_mwu=split_mwu, path=path,
                                             resource=resource)

class NumberDictionary(ResourceDict):
    """A class for language-specific name resources."""

    def __init__(self, language=config["default_language"],
                 lowercasing=config["lowercasing"],
                 split_mwu=config["split_mwu"], path=None,
                 resource="numbers"):
        """ Initializing the numbers lookup class.

        Args:
            lowercasing (bool): *True* if all data should be lowercased
            split_mwu (bool): *True* if in addition to underscored
                spellings of multi-word expressions their dashed and spaced
                versions should also be produced (e.g. 'good night',
                'good_night', "good-night")
            path (str, dict): if str, interpreted as the full direct path to
                the resource to be used (one-column vocab text file expected).
                Otherwise LDT will look for the file in the
                language_resources subfolder of the ldt_resources folder,
                as specified in the deafult config file.
        """
        super(NumberDictionary, self).__init__(language=language,
                                             lowercasing=lowercasing,
                                             split_mwu=split_mwu, path=None,
                                             resource=resource)

    @functools.lru_cache(maxsize=None)
    def is_a_word(self, word):
        """Returns True if the word is an ordinal or cardinal numeral,
        or if if contains an Arabic number.

        Args:
            word (str): a potential number

        Returns:
            (bool): True if the word is or contains a number.
        """
        word = word.lower()
        if word in self.data:
            return True
        else:
            # for char in word:
            #     if char.isnumeric():
            #         return True
            word = list(word)
            numbers = len([x for x in word if x.isnumeric()])
            # # letters = len([x for x in word if x.isalpha()])
            if numbers >= 2 or numbers/len(word) > 0.4:
                return True
        return False

class AssociationDictionary(ResourceDict):
    """A class for language-specific name resources."""

    def __init__(self, language=config["default_language"],
                 lowercasing=config["lowercasing"],
                 split_mwu=config["split_mwu"], path=None,
                 resource="associations"):
        """ Initializing the associations lookup class.

        Args:
            lowercasing (bool): *True* if all data should be lowercased
            split_mwu (bool): *True* if in addition to underscored
                spellings of multi-word expressions their dashed and spaced
                versions should also be produced (e.g. 'good night',
                'good_night', "good-night")
            path (str, dict): if str, interpreted as the full direct path to
                the resource to be used (one-column vocab text file expected).
                Otherwise LDT will look for the file in the
                language_resources subfolder of the ldt_resources folder,
                as specified in the deafult config file.
        """
        super(AssociationDictionary, self).__init__(language=language,
                                             lowercasing=lowercasing,
                                             split_mwu=split_mwu, path=path,
                                             resource=resource)


class WebDictionary(ResourceDict):


    """A class for language-specific name resources."""

    def __init__(self, language="en",
                 lowercasing=False,
                 split_mwu=False, path="helpers/generic_files/web_domains.vocab",
                 resource="domain"):
        """ Initializing the class for detecting URLs.

        Note:

            The domain list comes from `the official IANA list
            <https://www.iana.org/domains/root/db>`_, last updated on Aug.
            10th 2018.

        Args:
            lowercasing (bool): *True* if all data should be lowercased
            split_mwu (bool): *True* if in addition to underscored
                spellings of multi-word expressions their dashed and spaced
                versions should also be produced (e.g. 'good night',
                'good_night', "good-night")
            path (str, dict): if str, interpreted as the full direct path to
                the resource to be used (one-column vocab text file expected).
                Otherwise LDT will look for the file in the
                language_resources subfolder of the ldt_resources folder,
                as specified in the deafult config file.
        """
        dir_path = os.path.dirname(os.path.realpath(__file__)).strip("dicts")
        full_path=os.path.join(dir_path, path)
        super(WebDictionary, self).__init__(language=language,
                                            lowercasing=lowercasing,
                                            split_mwu=split_mwu,
                                            path=full_path,
                                            resource=resource)

    def is_a_word(self, word):
        for protocol in ["www.", "http:", "ftp:"]:
            if protocol in word:
                return True

        if not "." in word:
            return False
        else:
            for domain in self.data:
                if word.endswith(domain):
                    return True
                elif domain + "/" in word:
                    return True


class FileDictionary(ResourceDict):

    """A class for language-specific name resources."""

    def __init__(self, language="en",
                 lowercasing=False,
                 split_mwu=False,
                 path="helpers/generic_files/file_extensions.vocab",
                 resource="file"):
        """ Initializing the class for detecting URLs.

        Note:

            The file extension list currently has 182 entries,
            and comprises more popular formats rather than `everything
            <https://en.wikipedia.org/wiki/List_of_filename_extensions>`_.
            The reason for that is exostic file extensions like "bad" and
            "bar" that are unlikely to occur frequently, but likely to yield
            false positives.

        Args:
            lowercasing (bool): *True* if all data should be lowercased
            split_mwu (bool): *True* if in addition to underscored
                spellings of multi-word expressions their dashed and spaced
                versions should also be produced (e.g. 'good night',
                'good_night', "good-night")
            path (str, dict): if str, interpreted as the full direct path to
                the resource to be used (one-column vocab text file expected).
                Otherwise LDT will look for the file in the
                language_resources subfolder of the ldt_resources folder,
                as specified in the deafult config file.
        """
        dir_path = os.path.dirname(os.path.realpath(__file__)).strip("dicts")
        full_path=os.path.join(dir_path, path)
        super(FileDictionary, self).__init__(language=language,
                                            lowercasing=lowercasing,
                                            split_mwu=split_mwu,
                                            path=full_path,
                                            resource=resource)

    def is_a_word(self, word):
        if not "." in word:
            return False
        else:
            extension = word.split(".")[-1]
            if "."+extension in self.data:
                    return True
        return False

# if __name__=="__main__":
#     d={"A":["a"], "B":["B"], }
#     print(lowercase_resource(d))