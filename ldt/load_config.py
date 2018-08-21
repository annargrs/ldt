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
# import nltk
import ruamel.yaml as yaml

from ldt.helpers.exceptions import ResourceError as ResourceError

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

# downloading NLTK resources

# nltk.download("wordnet")
# nltk.download("stopwords")

TESTFILE = os.path.dirname(os.path.realpath(__file__))
TESTFILE = os.path.join(TESTFILE, "tests/sample_files/.ldt-config.yaml")

if "unittest" in sys.modules or "sphinx" in sys.modules:
    CONFIGPATH = TESTFILE
else:
    CONFIGPATH = os.path.expanduser('~/.ldt-config.yaml')
    if not os.path.exists(CONFIGPATH):
        print("Creating a sample configuration file in", CONFIGPATH)
        shutil.copyfile(TESTFILE, CONFIGPATH)

def load_config(path=CONFIGPATH):
    """Loading config file from either the user home directory or the test
    directory"""

    if not os.path.isfile(path):
        raise ResourceError("Configuration yaml file was not found at "+path)

    with open(path) as stream:
        try:
            options = yaml.safe_load(stream)
        except yaml.YAMLError:
            raise ResourceError("Something is wrong with the configuration "
                                "yaml file.")

    if "unittest" in sys.modules:
        options["path_to_resources"] = TESTFILE.strip(".ldt-config.yaml")
    options["path_to_cache"] = os.path.join(options["path_to_resources"],
                                            "cache")
    options["wiktionary_cache"] = False
    return options

#pylint: disable=invalid-name
config = load_config()
