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

+-------------------+--------+--------+--------+
| LD score          | CBOW   | GloVe  | SG     |
+-------------------+--------+--------+--------+
| SharedMorphForm   | 51.819 | 52.061 | 52.9   |
+-------------------+--------+--------+--------+
| SharedPOS         | 30.061 | 35.507 | 31.706 |
+-------------------+--------+--------+--------+
| SharedDerivation  | 4.468  | 3.938  | 5.084  |
+-------------------+--------+--------+--------+
| Synonyms          | 0.413  | 0.443  | 0.447  |
+-------------------+--------+--------+--------+
| Antonyms          | 0.128  | 0.133  | 0.144  |
+-------------------+--------+--------+--------+
| Hyponyms          | 0.035  | 0.035  | 0.038  |
+-------------------+--------+--------+--------+
| OtherRelations    | 0.013  | 0.013  | 0.013  |
+-------------------+--------+--------+--------+
| Misspellings      | 13.546 | 9.914  | 12.809 |
+-------------------+--------+--------+--------+
| ProperNouns       | 30.442 | 27.278 | 27.864 |
+-------------------+--------+--------+--------+
| CloseNeighbors    | 3.102  | 0.16   | 2.278  |
+-------------------+--------+--------+--------+
| FarNeighbors      | 25.209 | 49.934 | 21.41  |
+-------------------+--------+--------+--------+

The numbers here indicate percentage of neighbor vectors that held the
indicated relation with each target word in the sample. Also, see the
`metadata.json` file in the same output folder for dictionary coverage,
timestamps, missed words and other useful information.

