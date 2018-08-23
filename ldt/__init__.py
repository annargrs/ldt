# -*- coding: utf-8 -*-
""" Initializing the ldt package

Subpackages
===========

.. autosummary::
    :toctree: _autosummary

"""

from ._version import __version__
from .load_config import config

from ldt.helpers import resources
from ldt.helpers import loading
from ldt.helpers import ignore
from ldt.helpers import wiktionary_cache
from ldt.helpers import exceptions
from ldt.helpers import formatting

from ldt.dicts import dictionary
from ldt.dicts import metadictionary
from ldt.dicts import resources
from ldt.dicts import normalize

from ldt.dicts.base.custom import en
from ldt.dicts.base.wordnet import en
from ldt.dicts.base import babelnet
from ldt.dicts.base import wiktionary

from ldt.dicts.morphology.custom import en
from ldt.dicts.morphology.wordnet import en
from ldt.dicts.morphology import babelnet
from ldt.dicts.morphology import wiktionary
from ldt.dicts.morphology import morph_dictionary
from ldt.dicts.morphology import meta

from ldt.dicts.spellcheck.en import en
from ldt.dicts.spellcheck import custom

from ldt.dicts.semantics.wordnet import en
from ldt.dicts.semantics import babelnet
from ldt.dicts.semantics import wiktionary
from ldt.dicts.semantics import wikisaurus
from ldt.dicts.semantics import lex_dictionary

from ldt.dicts.derivation.custom import en
from ldt.dicts.derivation.wordnet import en
from ldt.dicts.derivation import wiktionary
from ldt.dicts.derivation import meta

from ldt.relations import word

# import ldt.helpers
# import ldt.dicts
# import ldt.dicts.semantics
# import ldt.dicts.spellcheck
# import ldt.dicts.morphology
# import ldt.dicts.derivation
# import ldt.dicts.base

