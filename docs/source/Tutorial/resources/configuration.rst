==================
Configuration file
==================

When LDT is imported, it looks for a ``.ldt-config.yaml`` file in the root of the user home directory. If this file is not
found, one is created with default settings. Modify them as needed.

The language-specific resources for English listed can be downloaded here.

The corpus-specific resources are relevant to the English Wikipedia dump (August 2013) that was used in our experiments.
You can download the resources, the cleaned corpus, and the dependency-parsed corpus, as well as 60 pre-trained
Skip-Gram, CBOW and GloVe embeddings of different sizes and types of syntactic context.

.. include:: .ldt-config.yaml
   :code: yaml
