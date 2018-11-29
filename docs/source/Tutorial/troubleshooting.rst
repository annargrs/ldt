===============
Troubleshooting
===============

.. contents:: :local:

------------------------------------
Wrong location of configuration file
------------------------------------

If LDT loads sample configuration file instead of the configuration file in
the user home folder, check if you have sphinx loaded in sys.modules. If you do,
you can remove them with `del sys.modules["sphinx"]`

The same will happen if "TRAVIS" or "TESTING_LDT" environment variables are
present.

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

------------------------------------
The neighbor extraction is too slow!
------------------------------------

The speed of this process depends on whether your numpy package has access
to the right linear algebra library - MKL, OpenBLAS or whatever is available
for your system. With the OpenBLAS and 4 Ghz Core i7-6700K processor in
Ubuntu we're
processing 900 words for 300K 500-dimensional embeddings in under three minutes.

If you do have the library, but the neighbor extraction is   still slow,
check if it is actually used by numpy. This can be done as follows:

>>> import numpy as np
>>> np.show_config()