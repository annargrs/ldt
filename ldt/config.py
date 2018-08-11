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

from ldt._version import __version__

# from ldt.helpers.exceptions import ResourceError as ResourceError

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

TESTFILE = os.path.dirname(os.path.realpath(__file__))
TESTFILE = os.path.join(TESTFILE, "test/sample_files/.ldt-config.yaml")
# TESTFILE = os.path.abspath(".test/sample_files/.ldt-config.yaml")

# if not os.path.exists(TESTFILE):
#     egg = "/ldt-"+__version__+"-py3.5/"
#     TESTFILE = TESTFILE.replace("/ldt/", egg)

if "unittest" in sys.modules:
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
        # raise ResourceError("User configuration file not found at path "+path)
        print("Something is wrong with the configuration yaml file.")

    with open(path) as stream:
        try:
            options = yaml.safe_load(stream)
        except yaml.YAMLError:
            print("Something is wrong with the configuration yaml file.")
            # raise ResourceError(
            #     "Something is wrong with the configuration yaml file.")

    if "unittest" in sys.modules:
        options["path_to_resources"] = TESTFILE.strip(".ldt-config.yaml")
    return options

#pylint: disable=invalid-name
config = load_config()
