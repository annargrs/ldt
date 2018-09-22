# -*- coding: utf-8 -*-
""" Initializing the ldt package

Subpackages
===========

.. autosummary::
    :toctree: _autosummary

"""

from ._version import __version__
from ldt import load_config

from ldt import helpers
from ldt.helpers.loading import load_resource
from ldt import dicts
from ldt import relations
