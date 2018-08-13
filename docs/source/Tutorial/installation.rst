.. _installation:

=========================================
Installing Linguistic Diagnostics Toolkit
=========================================

You need Python 3.5 or above.

.. code-block:: python

   pip install ldt

Package requirements:

* `nltk <http://www.nltk.org/install.html>`_
* `pyenchant <https://github.com/rfk/pyenchant>`_
* `wiktionaryparser <https://github.com/Suyash458/WiktionaryParser>`_
* `vecto <https://vecto.space>`_
* `pandas <https://pandas.pydata.org/>`_
* `TimeOut decorator <https://pypi.python.org/pypi/timeout-decorator>`_
* `ruamel.yaml <https://pypi.org/project/ruamel.yaml/>`_
* `timeout-decorator <https://pypi.org/project/timeout-decorator/>`_
* `inflect <https://pypi.org/project/inflect/>`_

NLTK has many resources, of which three are used by LDT: wordnet, stopwords, lemmatizer.
You can install them individually from within Python shell:

```python
import nltk
nltk.download("wordnet")
```

or from command line:

```
>>> python -m nltk.downloader wordnet
```

For spellchecker engines, LDT currently relies on the `pyenchant <https://github.com/rfk/pyenchant>`_ library, which
provides an interface to the system spellcheckers such aspell, hunspell etc. Aspell worked the best in our tests,
although any other engine can also be used. Enchant needs to be installed for this to work.

* Mac: install enchant with brew (http://macappstore.org/enchant/)
* Linux: enchant should be available from your distribution repository.
  E.g. on Ubuntu you should be able to just `sudo apt-get install enchant`.
* Windows: we did not test this, but a binary package should be available from PyPi upon installation of pyenchant, and
  it should be possible to copy any required OpenOffice spellchecker dictionaries into pyenchant folder (advice from
  `here <https://faculty.math.illinois.edu/~gfrancis/illimath/windows/aszgard_mini/movpy-2.0.0-py2.4.4/manuals/PyEnchant/PyEnchant%20Tutorial.htm>`_).