====================================
Generating vector neighborhood files
====================================

LDT relies on `Vecto library <http://vecto.space>`_ for processing word
embeddings. It also follows Vecto approach in ensuring reproducibility of
experiments in automatically loading any available
`metadata <https://vecto.readthedocs.io/en/docs/tutorial/metadata.html>`_.

-----------------------
Vocabulary sample files
-----------------------

A core advantage of LDT is that you are not tied to a specific dataset. If your
goal is to find the embedding that works the best for a particular task, it
makes sense to explore the vocabulary that is likely to be important for that
task. For example, if you are doing sentiment analysis, it is possible that
the quality of representations of adjectives is at least as important as that
of nouns - although they are not represented well in traditional similarity/
relatedness or analogy datasets.

With LDT, you can create and use your own vocabulary dataset for profiling your
embeddings. The vocab samples are expected to be placed in
`experiments/vocab_samples` subfolder of your ldt resource folder (the location
specified in LDT :ref:`Configuration file`).

The format is one-word-per-line, the file should have ".vocab" extension.
Here is the included `test_sample.vocab` file example:

.. code-block::

    theft
    hurricane
    deployment
    advice
    activism
    premiership
    paradox
    kitchen


If you're creating your own sample, we recommend that you also create a metadata
file that documents this sample. LDT follows vecto-style metadata in json format.
Here is a sample `metadata.json`:

.. code-block:: json

    {
    "class": "dataset",
        "uuid": "f50ec0b7-f960-400d-91f0-c42a6d44e3d1",
        "task": "get_neighbors",
        "language": ["english"],
        "name": "test_sample",
        "description": "just a few random words for testing"
    }

This metadata will be automatically included in the metadata for any experiments
performed with LDT, so that you will never lose track of which files you used
for what an when.

The full `LDT base folder distribution <https://my.pcloud.com/publink/show?code=XZnkSn7ZUdfgWrtnfiyuXhjg9I0es0iPQRWy>`_
also includes `our balanced sample <https://my.pcloud.com/publink/show?code=XZ3Ghn7ZgCWsu7FHmP0X2eKmUR95VXmgbKIy>`_
of 909 verbs, adjectives, adverbs and nouns, selected for POS and frequency
as described in `the paper <http://aclweb.org/anthology/C18-1228>`_.

To specify what sample to use in an experiment, specify the name of the *folder*
containing the target dataset and metadata.json in the LDT
:ref:`Configuration file`. Once again, the folder must be located in
`experiments/vocab_samples` subfolder of your ldt resource folder.

.. code-block:: yaml

   experiments:
      vocab_sample: test_sample

------------------------------------
Generating vector neighborhood files
------------------------------------

You can generate neighborhood files for top *n* neighbors in the
vocabulary sample of your choice as follows:

>>> experiment = ldt.experiments.VectorNeighborhoods(experiment_name="just testing", overwrite=True, top_n=5)
>>> experiment.get_results()

The data will be saved in the `experiments\neighbors\just_testing` subfolder
in your ldt data location. For each embedding tab-separated files containing
neighbors, their rank and similarity scores will be generated. Example output:

+-------------+------+------------+--------------------+
| Target      | Rank | Neighbor   | Similarity         |
+-------------+------+------------+--------------------+
| premiership | 1    | semi-final | 0.962702751159668  |
+-------------+------+------------+--------------------+
| premiership | 2    | decider    | 0.9600796699523926 |
+-------------+------+------------+--------------------+
| premiership | 3    | play-offs  | 0.9560928344726562 |
+-------------+------+------------+--------------------+

If your embeddings are not normalized, retrieving neighbors will take more time.
By default LDT normalizes them on loading. If you need them not normalized,
use `normalize=False` option.

Alongside with the vector neighborhood files LDT generates a `metadata.json` file
to record the details of the current experiment: uuid, timestamps, library version,
embeddings metadata (if not found, LDT will generate embedding metadata stubs for you).
Note that the dataset metadata is also included automatically.

.. code-block:: json

    {
    "class": "experiment",
    "version": "ldt v. 0.3.0",
    "task": "get_neighbors",
    "uuid": "292594ae-287d-4c92-863e-747a1214d6d3",
    "top_n": 2,
    "embeddings": [
        {
            "class": "embeddings",
            "model": "sample_embeddings",
            "uuid": "f50ec0b7-f960-400d-91f0-c42a6d44e3d0",
            "window": 2,
            "dimensionality": 25,
            "context": "linear_unbound",
            "epochs": 2,
            "path": "/path/to/sample_files/sample_embeddings"
        }
    ],
    "timestamp": {
        "f50ec0b7-f960-400d-91f0-c42a6d44e3d0": {
            "start_time": "2018-10-08T21:56:59.884987",
            "end_time": "2018-10-08T21:57:02.562557"
        }
    },
    "dataset": {
        "class": "dataset",
        "uuid": "f50ec0b7-f960-400d-91f0-c42a6d44e3d1",
        "name": "test_sample",
        "description": "just a few words for testing",
        "task": "get_neighbors",
        "language": ["english"]
    }
    }


-----------------------------------
How many neighbors should I sample?
-----------------------------------

This depends on the kind of vocabulary you are interested in. A word like a *knob*
is not likely to have hundreds of closely related words, but we found *rather* as
a neighbor of *quite* in SG DEPS model at rank 920.

That being sad, the correlations with intrinsic and extrinsic tasks that we obtained
for data from *top 100* and *top 1000* neighbor pairs were similar
(`see for yourself <http://ldtoolkit.space/analysis/correlation/>`_).

------------------------------------
The neighbor extraction is too slow!
------------------------------------

The speed of this process depends on whether your numpy package has access
to the right linear algebra library - MKL, OpenBLAS or whatever is available
 for your system. With the OpenBLAS and Corei7 processor in Ubuntu we're
 processing 900 words for 300K 500-dimensional embeddings in under three minutes.

 If you do have the library, but the neighbor extraction is   still slow, check if it is actually used by numpy. This can be done as
  follows:

>>> import numpy as np
>>> np.show_config()
