.. _configuration:

==================
Configuration file
==================

When LDT is imported, it looks for a ``.ldt-config.yaml`` file in the root of the user home directory. If this file is not
found, one is created with default settings. Modify them as needed.

Importing ldt in interactive session should indicate the location of the configuration file:

>>> import ldt
Loading configuration file: /home/user/.ldt-config.yaml

**Troubleshooting**: if LDT loads sample configuration file instead of the configuration file in the user home folder, check if you have unittests or sphinx loaded in sys.modules. If you do, you can remove them with ``del sys.modules["unittest"]``


.. include:: .ldt-config.yaml
   :code: yaml

LDT expects to find the resources listed under the ``language_resources`` and ``corpus_resources`` in the specified ``path_to_resources``. See the corresponding pages for how to obtain the listed :doc:`language resources for English <./language_resources>` and :doc:`Wiki201308 corpus <corpus_resources>`.