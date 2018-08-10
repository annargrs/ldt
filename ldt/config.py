# -*- coding: utf-8 -*-
""" Loading config file

LDT has a number of module-wide variables for default parameters. They can
also be overridden in most modules when instantiating resource objects. See
tutorial for explanation of parameters and a sample.

Todo:
    * create default config path on the first run

"""

import os
import warnings
import sys

import ruamel.yaml as yaml

# from ldt.helpers.exceptions import ResourceError as ResourceError

warnings.simplefilter('ignore', yaml.error.UnsafeLoaderWarning)

TESTFILE = os.path.dirname(os.path.realpath(__file__)).strip("ldt")
TESTFILE = os.path.join(TESTFILE, "test/sample_files/sample_config.yaml")


if "unittest" in sys.modules:
    CONFIGPATH = TESTFILE
else:
    CONFIGPATH = None

def load_config(path=None):
    """Loading config file from either the user home directory or the test
    directory"""
    if not path:
        path = os.path.expanduser('~/.ldt-config.yaml')
        print("Loading config from default location in", path)

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
        options["path_to_resources"] = TESTFILE.strip("sample_config.yaml")
    return options

#pylint: disable=invalid-name
config = load_config(CONFIGPATH)
