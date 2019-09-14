# -*- coding: utf-8 -*-
""" Loading configuration file

LDT has a number of module-wide variables for default parameters. They can
also be overridden in most modules when instantiating resource objects. See
tutorial for explanation of parameters and a sample.

"""

import os
import warnings
import sys
import shutil
import ruamel.yaml as yaml
import nltk
import outdated

from ldt.helpers.exceptions import ResourceError
from ldt._version import __version__

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

try:
    is_outdated, latest_version = outdated.check_outdated('ldt', __version__)
    if is_outdated:
        print("You are using ldt v."+__version__+". Upgrade to v."+latest_version,
              "with \n   pip install --upgrade ldt\nSee what's new: "
              "https://github.com/annargrs/ldt/blob/master/CHANGES.txt")
except ValueError:
    print("This is LDT", __version__, "- an unpublished development version.")


def nltk_download():
    """Downloading the necessary NLTK resources if they are missing."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

nltk_download()

TESTFILE = os.path.dirname(os.path.realpath(__file__))
TESTFILE = os.path.join(TESTFILE, "tests/sample_files/.ldt-config.yaml")

if "TESTING_LDT" in os.environ or "TRAVIS" in os.environ or "sphinx" in sys.modules:
    CONFIGPATH = TESTFILE
else:
    CONFIGPATH = os.path.expanduser('~/.ldt-config.yaml')
    if not os.path.exists(CONFIGPATH):
        print("Creating a sample configuration file in", CONFIGPATH)
        shutil.copyfile(TESTFILE, CONFIGPATH)

def load_config(path=CONFIGPATH):
    """Loading config file from either the user home directory or the test
    directory"""
    print("Loading configuration file:", path)
    if not os.path.isfile(path):
        raise ResourceError("Configuration yaml file was not found at "+path)

    with open(path) as stream:
        try:
            options = yaml.safe_load(stream)
        except yaml.YAMLError:
            raise ResourceError("Something is wrong with the configuration "
                                "yaml file.")

    if "TRAVIS" in os.environ or "/tests/sample_files/" in path:
    # if TESTING:
        options["path_to_resources"] = path.strip(".ldt-config.yaml")
        options["experiments"]["embeddings"] = \
            [os.path.join(options["path_to_resources"], "sample_embeddings")]
        options["wiktionary_cache"] = False
        options["experiments"]["top_n"] = 2
        options["experiments"]["timeout"] = None
        options["experiments"]["multiprocessing"] = 1
        options["corpus"] = "Wiki201308"
        options["language_resources"]["hunspell"]["path"] = \
            os.path.join(options["path_to_resources"], "language_resources",
                         "hunspell_data")

    options["path_to_cache"] = \
        os.path.join(options["path_to_resources"], "cache")
    for i in options:
        if options[i] == "None":
            options[i] = None

    if "path/to/cache/and/resources" in options["path_to_resources"]:
        print("Please set up your resource directory before using LDT. "
              "See instructions at "
              "https://ldt.readthedocs.io/Tutorial/resources/configuration.html")

    return options

#pylint: disable=invalid-name
global config
config = load_config()
