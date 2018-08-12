=========================================
Installing Linguistic Diagnostics Toolkit
=========================================

You need Python 3.5 or above.

.. code-block:: python

   pip install ldt

Package requirements:

* `nltk (with WordNet corpus) <http://www.nltk.org/install.html>`_
* `pyenchant <https://github.com/rfk/pyenchant>`_
* `wiktionaryparser <https://github.com/Suyash458/WiktionaryParser>`_
* `vecto <https://vecto.space>`_
* `pandas <https://pandas.pydata.org/>`_
* `TimeOut decorator <https://pypi.python.org/pypi/timeout-decorator>`_
* `ruamel.yaml <https://pypi.org/project/ruamel.yaml/>`_

For spellchecker engines, LDT currently relies on the `pyenchant <https://github.com/rfk/pyenchant>`_ library, which
provides an interface to the system spellcheckers such aspell, hunspell etc. Aspell worked the best in our tests,
although any other engine can also be used. To install them on your system,

Dictionaries for US and UK English, German, and French are included in
pyenchant distribution. If you need other languages, you will need to do the
following:

* Windows: just copy OpenOffice dictionary files to pyenchant folder (
  advice from here `this <https://faculty.math.illinois.edu/~gfrancis/illimath
  /windows/aszgard_mini/movpy-2.0.0-py2.4.4/manuals/PyEnchant/PyEnchant
  %20Tutorial.htm>`_, not tested by LDT developers).
* Mac: install enchant with brew (http://macappstore.org/enchant/)
* Linux: enchant should be available from your distribution repository.
  E.g. on Ubuntu you should be able to just `sudo apt-get install enchant`.
