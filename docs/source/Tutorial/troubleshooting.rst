===============
Troubleshooting
===============

.. contents:: :local:

------------------------------------
Wrong location of configuration file
------------------------------------

If LDT loads sample configuration file instead of the configuration file in the user home folder, check if you have unittests or sphinx loaded in sys.modules. If you do, you can remove them with `del sys.modules["unittest"]`


--------------------------------------------
Wiktionary parser problems for derived terms
--------------------------------------------

The current version of wiktionaryparser does not support retrieval of derived terms, so the dependency is frozen at 0.0.4. However, that version may not work as expected with python older than 3.6. `Pull request has been created. <https://github.com/Suyash458/WiktionaryParser/pull/45>`_

In the meanwhile, if you're seeing this error:

>>> import wiktionaryparser
...
    from utils import WordData, Definition, RelatedWord
ImportError: cannot import name 'WordData'

A quick-and-dirty fix is to change the import statement at the beginning of your local WikiParse file as follows:

.. code-block:: python

   from .utils import WordData, Definition, RelatedWord

