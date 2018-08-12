# -*- coding: utf-8 -*-
""" Initializing the ldt package

Subpackages
===========

.. autosummary::
    :toctree: _autosummary

"""

import ldt.dicts.dictionary
import ldt.dicts.metadictionary

from .config import config
from ._version import __version__
from .helpers import loading, formatting, wiktionary_cache, resources

from .dicts.base import *
from .dicts.semantics import *
from .dicts.morphology import *
from .dicts.derivation import *
from .dicts.spellcheck import *
from .dicts.resources import *

