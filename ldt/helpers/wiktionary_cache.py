# -*- coding: utf-8 -*-
"""Wiktionary cache of existing pages.

    It is possible to use Wiktionary API directly to find whether a word
    has an entry, e.g.
    # http://en.wiktionary.org/w/api.php?action=query&titles
    =my_word_of_interest
    However, that is slow and unkind on the wiktionary servers when running
    large-scale experiments. LDT caches a list of entries from the latest
    dump in the ldt_resources folder and uses that.

    Cache files are created in the LDT resources directory, which is set in the
    LDT config file in the user directory.

    The naming convention is YYYY-M-D_language_dictionary.vocab. For example:

     - 2018-7-1_en_wikisaurus.vocab
     - 2018-7-1_en_wiktionary.vocab

Todo:
    * refactor the tests
    * usage example in the module description
    * switch to lemma lists instead of page title lists
      (https://en.wiktionary.org/wiki/Category:English_lemmas)
    * make sure that the words are in the given language

"""

import os
import urllib.request
import datetime
import gzip

# import ldt.helpers

# import ldt.config as config
# from ldt.load_config import config
from ldt.load_config import config as config
from ldt.helpers.loading import load_resource as load_resource

def find_vocab_file(language, path_to_cache, wikisaurus=False):
    '''

    A helper function for finding the timestamped vocab file for the needed
    language in the resources folder.

    Args:
        language (str): a `2-letter language code <https://en.wiktionary.org/wiki/Wiktionary:List_of_languages#Two-letter_codes>`_
        path_to_cache (str): the path to the cache subfolder of ldt resources
            folder specified in config, where the wiktionary cache files are
            saved wikisaurus (bool): if False, Wiktionary entry namespace is
            cached, otherwise Wiktionary thesaurus entries are cached.

    Returns:
        (str): filename if one was present, or "none"

    '''
    if wikisaurus:
        template = "wikisaurus.vocab"
    else:
        template = "wiktionary.vocab"

    files = os.listdir(path_to_cache)
    filename = "none"
    for f in files:
        if language in f and template in f:
            filename = f
    return filename



def get_timestamped_vocab_filenames(filename, language=config[
    "default_language"], wikisaurus = False):
    '''

    A helper function for :func:`update_wiktionary_pages` that provides
    timestamped filenames.

    Args:
        filename (str): an earlier cache file, or "none" is there wasn't one.
        language (str): a `2-letter language code <https://en.wiktionary.org/wiki/Wiktionary:List_of_languages#Two-letter_codes>`_
        wikisaurus (bool): if False, Wiktionary entry namespace is cached,
            otherwise Wiktionary thesaurus entries are cached.

    Returns:
        (dict): a dictionary holding the old and new filenames

    '''

    if wikisaurus:
        template = "wikisaurus.vocab"
    else:
        template = "wiktionary.vocab"

    res = {}
    now = datetime.datetime.now()

    res["new_filename"] = str(now.year)+"-"+str(
        now.month)+"-"+str(
        now.day)+"_"+language+"_" + template

    if filename == "none":
        return res

    else:
        then = filename.split("_")[0]
        then_year = int(then.split("-")[0])
        then_month = int(then.split("-")[1])
        then_day = int(then.split("-")[2])

        if datetime.date(now.year, now.month, now.day) > datetime.date(
                then_year, then_month, then_day):
        #if now_year > then_year or now_month > then_month:
            res["old_filename"] = str(then_year)+"-"+str(
                then_month)+"-"+str(
                then_day)+"_"+language+"_wiktionary.vocab"
        return res

def update_wiktionary_cache(language=config["default_language"],
                            path_to_cache=config["path_to_resources"],
                            wikisaurus=False):
    ''' The main wiktionary cache updating function.

    Args:
        language (str): a `2-letter language code <https://en.wiktionary.org/wiki/Wiktionary:List_of_languages#Two-letter_codes>`_
        path_to_resources (str): the path to ldt resources folder specified in
            config. The cache files are saved in "cache" subfolder of this folder.
        wikisaurus (bool): if False, Wiktionary entry namespace is cached,
            otherwise Wiktionary thesaurus entries are cached.

    Returns:
        (bool): True if the cache was updated, False otherwise

    '''

    # "0" is Wiktionary entries namespace, "110" is thesaurus entries namespace

    # if not path_to_cache.endswith("cache"):
    #     path_to_cache = os.path.join(path_to_cache, "cache")
    path_to_cache = get_cache_dir(path_to_cache)
    if wikisaurus:
        namespace = "110"
    else:
        namespace = "0"

    filename = find_vocab_file(language, path_to_cache, wikisaurus = wikisaurus)

    filenames = get_timestamped_vocab_filenames(filename, language, wikisaurus = wikisaurus)

    if filename == "none" or "old_filename" in filenames.keys():

        url = 'https://dumps.wikimedia.org/'+language+\
              'wiktionary/latest/'+language+'wiktionary-latest-all-titles.gz'

        gz = os.path.join(path_to_cache, filenames["new_filename"] + ".gz")
        if not os.path.exists(gz):
            try:
                urllib.request.urlretrieve(url, gz)
            except urllib.error.HTTPError:
                print("No such resource. Try one of the 2-letter Wiktionary "
                      "language codes, such as 'en' or 'de'. See "
                      "https://en.wiktionary.org/wiki/Wiktionary:List_of_languages#Two-letter_codes"
                      "for the full list.")
                return None


        with gzip.open(gz, 'rt') as f:
            file_content = f.read().split("\n")

            if not os.path.exists(gz.replace(".gz", "")):
                with open(gz.replace(".gz", ""), 'a') as out_file:

                    for l in file_content:
                        split_line = l.split("\t")

                        if split_line[0] == namespace:
                            out_file.write(split_line[1]+"\n")

        os.remove(gz)
        if "old_filename" in filenames.keys():
            os.remove(os.path.join(path_to_cache, filenames[
                "old_filename"]))

        print("Wiktionary vocab list successfully cached as "+ gz.strip(
            ".gz"))
        return gz.strip(".gz")

    else:
        print("Wiktionary vocab list already up-to-date as " + os.path.join(
            path_to_cache, filenames["new_filename"]))
        return False



def load_wiktionary_cache(language=config["default_language"],
                          lowercasing=config["lowercasing"],
                          path_to_cache=config["path_to_resources"],
                          wikisaurus =False):
    '''

    Args:
        language (str): a `2-letter language code <https://en.wiktionary.org/wiki/Wiktionary:List_of_languages#Two-letter_codes>`_
        lowercasing (bool): if not set, the global config variable is used.
            True (default) lowercases all vocab.
        path_to_cache (str): the path to ldt resources folder specified in
            config. The cache files are saved in "cache" subfolder.
        wikisaurus (bool): if False, Wiktionary entry namespace is cached,
            otherwise Wiktionary thesaurus entries are cached.

    Returns:
        (set): vocab list for the corresponding language, lowercased or not
            according to the global or local lowercasing option

    Todo:
        update the error message

    '''

    path_to_cache = get_cache_dir(path_to_cache)
    filename = find_vocab_file(language, path_to_cache, wikisaurus=wikisaurus)

    if filename != "none":
        date = filename.split("_")[0]
        print("The current cache file was updated on", date,
              "\nYou can run wiktionary.update_wiktionary_cache ("
              "language='') to update it")
    else:
        update_wiktionary_cache(language, path_to_cache, wikisaurus=wikisaurus)
        filename = find_vocab_file(language, path_to_cache, wikisaurus=wikisaurus)
#        print("Wiktionary cache file updated.")

    path = os.path.join(path_to_cache, filename)

    if not lowercasing:
        wiktionary_cache = load_resource(path=path, format="vocab",
                                         lowercasing=False)
    else:
        wiktionary_cache = load_resource(path=path, format="vocab")
    return wiktionary_cache

def get_cache_dir(path_to_cache=config["path_to_resources"]):
    """Helper function that formats the path to cache and creates it,
    if necessary.

    Args:
        path_to_cache (str): the path to resource directory. If "cache"
        subfolder does not exist. it will be created.

    Returns:
        (str): the path to the cache directory.

    """
    if not path_to_cache.endswith("/cache"):
        path_to_cache = os.path.join(path_to_cache, "cache")
    if not os.path.exists(path_to_cache):
        os.mkdir(path_to_cache)
    return path_to_cache

