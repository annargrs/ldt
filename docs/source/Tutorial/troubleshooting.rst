===============
Troubleshooting
===============

.. contents:: :local:

------------------------------------
Wrong location of configuration file
------------------------------------

If LDT loads sample configuration file instead of the configuration file in the user home folder, check if you have unittests or sphinx loaded in sys.modules. If you do, you can remove them with `del sys.modules["unittest"]`

----------------------
NLTK resources missing
----------------------

NLTK has many resources, of which three are used by LDT: ``wordnet``,
``stopwords``, ``lemmatizer``. Should they be missing, you can install them
individually from within Python shell:

.. code-block:: python

   import nltk
   nltk.download("wordnet")

or from command line:

.. code-block:: python

   python -m nltk.downloader wordnet