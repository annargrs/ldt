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
import outdated

from ldt.helpers.exceptions import ResourceError
from ldt._version import __version__

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

try:
    is_outdated, latest_version = check_outdated('ldt', __version__)
    if is_outdated:
        print("You are using ldt v."+__version__+". Upgrade to v."+latest_version,
              "with \n   pip install --upgrade ldt\nSee what's new: "
              "https://github.com/annargrs/ldt/blob/master/CHANGES.txt")
except ValueError:
    print("This is LDT", __version__, "- an unpublished development version.")


def nltk_download():
    # downloading NLTK resources if they're missing
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

TESTFILE = os.path.dirname(os.path.realpath(__file__))
TESTFILE = os.path.join(TESTFILE, "tests/sample_files/.ldt-config.yaml")

if "TESTING_LDT" in os.environ or "sphinx" in sys.modules:
    TESTING=True
else:
    TESTING=False

if TESTING:
    nltk_download()

if TESTING:
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

#    if "unittest" in sys.modules:
    if TESTING:
        options["path_to_resources"] = TESTFILE.strip(".ldt-config.yaml")
        options["experiments"]["embeddings"] = \
            [os.path.join(options["path_to_resources"], "sample_embeddings")]
        options["wiktionary_cache"] = False
        options["experiments"]["top_n"] = 2
        options["experiments"]["batch_size"] = 2
        options["experiments"]["timeout"] = None
        options["experiments"]["multiprocessing"] = 1
        options["corpus"] = "Wiki201308"
    options["path_to_cache"] = \
        os.path.join(options["path_to_resources"], "cache")
    for i in options:
        if options[i] == "None":
            options[i] = None

    return options

#pylint: disable=invalid-name
global config
config = load_config()
