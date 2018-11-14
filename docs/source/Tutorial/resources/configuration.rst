.. _configuration:

==================
Configuration file
==================

When LDT is imported, it looks for a ``.ldt-config.yaml`` file in the root of the user home directory. If this file is not
found, one is created with default settings. Modify them as needed.

Importing ldt in interactive session should indicate the location of the configuration file:

>>> import ldt
Loading configuration file: /home/user/.ldt-config.yaml

.. include:: .ldt-config.yaml
   :code: yaml

LDT expects to find the resources listed under the ``language_resources`` and ``corpus_resources`` in the specified ``path_to_resources``. See the corresponding pages for how to obtain the listed :doc:`language resources for English <./language_resources>` and :doc:`Wiki201308 corpus <corpus_resources>`.
You can download `the whole ldt_data folder <https://my.pcloud.com/publink/show?code=XZnkSn7ZUdfgWrtnfiyuXhjg9I0es0iPQRWy>`_,
complete with vocabulary samples. Unpack it to the location of your choosing and specify that location in the config file.
