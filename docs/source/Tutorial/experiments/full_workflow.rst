======================================
Profiling word embeddings in one click
======================================

The above sections describe usage and setting up of the three steps of LDT analysis:
extracting vector neighborhoods, annotating and analyzing them. You can also performed
them all in one click using :func:`~ldt.experiments.default_workflow.default_workflow.default_workflow`,
which utilizes default settings for our linguistic resources. You can also make use of
that code as a template to write your own script, setting up
ldt resources your own way.

To use it interactively (recommended only for small experiments):

>>> ldt.experiments.default_workflow(experiment_name="just_testing", top_n=5)

This will start the analysis for the embeddings and vocab sample specified in the default
configuration file. The results and metadata for all three steps will be saved in 'experiments/just_testing'
folder of the specified ldt data folder.

To run the same procedure from command line use the following command:

::

   python3 -m ldt.experiments.default_workflow

