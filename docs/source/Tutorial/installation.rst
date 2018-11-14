.. _installation:

=========================================
Installing Linguistic Diagnostics Toolkit
=========================================

You need Python 3.5 or above. The latest stable version of LDT is now available in PyPi:

>>> pip install ldt

The latest development version can be installed with:

>>> pip install git+https://github.com/annargrs/ldt.git

Package requirements (will be installed automatically by pip):

* `nltk <http://www.nltk.org/install.html>`_
* `pyenchant <https://github.com/rfk/pyenchant>`_
* `wiktionaryparser <https://github.com/Suyash458/WiktionaryParser>`_
* `vecto <https://vecto.space>`_
* `pandas <https://pandas.pydata.org/>`_
* `TimeOut decorator <https://pypi.python.org/pypi/timeout-decorator>`_
* `ruamel.yaml <https://pypi.org/project/ruamel.yaml/>`_
* `timeout-decorator <https://pypi.org/project/timeout-decorator/>`_
* `inflect <https://pypi.org/project/inflect/>`_
* `p_tqdm <https://github.com/swansonk14/p_tqdm>`_ and the underlying `pathos.multiprocessing <https://pypi.org/project/pathos/>`_

To run LDT will expect to find an ``.ldt-config.yaml`` configuration file in the user home folder, as described in the section :ref:`Configuration file`.

------------
Spellchecker
------------

For spellchecker engines, LDT currently relies on the `pyenchant <https://github.com/rfk/pyenchant>`_ library, which
provides an interface to the system spellcheckers such aspell, hunspell etc. Aspell worked the best in our tests,
although any other engine can also be used. Enchant needs to be installed for this to work.

* Mac: install enchant with brew (http://macappstore.org/enchant/)
* Linux: enchant should be available from your distribution repository.
  E.g. on Ubuntu you should be able to just `sudo apt-get install enchant`.
* Windows: we did not test this, but a binary package should be available from PyPi upon installation of pyenchant, and
  it should be possible to copy any required OpenOffice spellchecker dictionaries into pyenchant folder (advice from
  `here <https://faculty.math.illinois.edu/~gfrancis/illimath/windows/aszgard_mini/movpy-2.0.0-py2.4.4/manuals/PyEnchant/PyEnchant%20Tutorial.htm>`_).

Next you will need to configure LDT and download some additional resources.
See sections :ref:`Configuration file`, :ref:`Corpus-specific resources` and
:ref:`Language-specific resources`.

