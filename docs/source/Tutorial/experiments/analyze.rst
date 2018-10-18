===================================
Analysing the results of annotation
===================================

----------------
Input and output
----------------

The input to this step of analysis is the annotated vector neighborhoods, generated
as described in section :ref:`Annotating vector neighborhoods`.

The basic usage is as follows:

>>> experiment = ldt.experiments.LDScoring(experiment_name="just testing", ld_scores=["Synonyms", "Antonyms"], overwrite=True)
>>> experiment.get_results()

This will produce two files in `experiments/just_testing` subfolder
of your ldt data folder: `ld_scores.tsv` file and `metadata.json`.

Sample scoring file format:

+----------+-------------------+--------------------+
| LDScores | sample_embeddings | sample_embeddings2 |
+----------+-------------------+--------------------+
| Synonyms | 0.0               | 41.4               |
+----------+-------------------+--------------------+
| Antonyms | 0.35              | 0.0                |
+----------+-------------------+--------------------+

Metadata file includes and partly copies the annotation metadata in the "annotation" key.
(see :ref:`Annotating vector neighborhoods`).
It also adds the output ld_scores (as some of them are derived from annotations
in a non-trivial way).

.. code-block:: json

    {
    "timestamp": "2018-10-08T22:17:13.911398",
    "version": "ldt v. 0.3.0",
    "class": "experiment",
    "task": "ld_scores_analysis",
    "ld_scores": ["Synonyms", "Antonyms"],
    "uuid": "85778a52-1848-4031-9040-d49c1d2ea7eb",
    "embeddings": [
        {
            "class": "embeddings",
            "model": "sample_embeddings",
            "uuid": "f50ec0b7-f960-400d-91f0-c42a6d44e3d0",
            "window": 2,
            "dimensionality": 25,
            "context": "linear_unbound",
            "epochs": 2,
            "path": "/home/anna/PycharmProjects/ldt/ldt/tests/sample_files/sample_embeddings"
        }
    ],
    "annotation": {
            "class": "experiment",
        "task": "annotate_neighbors",
        "uuid": "50fb8538-c092-4105-996d-c331f8801a26",
        "version": "ldt v. 0.3.0",
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
                "start_time": "2018-10-08T22:02:16.929949",
                "end_time": "2018-10-08T22:03:27.865392"
            }
        },
            "failed_pairs": [],
        "missed_pairs": [
            ["premiership","decider"]
        ],
        "total_pairs": 16,
        "annotated_information": ["Synonyms",
            "Antonyms"
        ],
        "coverage": 0.94,

        "ldt_config": {
            "path_to_resources": "/home/anna/PycharmProjects/ldt/ldt/tests/sample_files/", "default_language": "English",
            "lowercasing": true,
            "babelnet_key": "None",
            "wiktionary_cache": false,
            "cache_size": null,
            "language_resources": {
                "en": {
                    "names": "names.vocab",
                    "numbers": "numbers.vocab",
                    "associations": "associations.json",
                    "gdeps": "gdeps.json"
                }
            },
            "corpus": "Wiki201308",
            "corpus_resources": {
                "Wiki201308": {
                    "freqdict": "Wiki201308.freqdict",
                    "vocabulary": "Wiki201308.vocab",
                    "cooccurrence": "3grams.json"
                }
            },
            "experiments": {
                "vocab_sample": "test_sample",
                "embeddings": [
                    "/path/to/sample_files/sample_embeddings"
                ],
                "experiment_name": "just_testing",
                "top_n": 2,
                "overwrite": true
            },
            "path_to_cache": "/path/to/sample_files/cache"
        }
    }
    }


-------------------
Supported ld scores
-------------------

All ld scores described in the paper are supported, and the list is growing.
ld_scores argument of :class:`~ldt.experiments.analyze.LDScoring` takes a list of
any of the following scores (or `"all"` for all possible scores). Obviously, the
relevant information must have been annotated in the previous stage of the experiment.

- "SharedPOS",
- "SharedMorphForm",
- "SharedDerivation",
- "NonCooccurring",
- "CloseNeighbors",
- "FarNeighbors",
- "LowFreqNeighbors",
- 'HighFreqNeighbors',
- "GDeps",
- "TargetFrequency",
- "NeighborFrequency",
- "Associations",
- "ShortestPathMedian",
- "CloseInOntology",
- "Synonyms",
- "Antonyms",
- "Meronyms",
- "Hyponyms",
- "Hypernyms",
- "OtherRelations",
- "Numbers",
- "ProperNouns",
- "Misspellings",
- "URLs",
- "Filenames",
- "ForeignWords",
- "Hashtags",
- "Noise".

See `this page <http://ldtoolkit.space/ldscores/>`_ for more details on ld scores.

--------------------------
How LD scores are computed
--------------------------

Binary relations (e.g. synonymy is either detected or not) are quantified as a
simple count of all cases of that relation in all target:neighbor pairs for each
embedding. Directed lexicographic relations (hypernymy, hyponymy, meronymy) are
counted when the target word is e.g. a hypernym of the neighbor.

Continuous variables are broken down into bins, the size of which was chosen
empirically. The :meth:`~ldt.experiments.analyze.LDScoring._process` method
provides settings for:

- *lowfreq_threshold*: neighbors below this number will be considered low-frequency,
  and those above this number - high-frequency (default: 1000).
- *far_neighbors_threshold*: neighbors further than this number will be considered
  as "far neighbors" (default: 0.7).
- close_neighbors_threshold (float): neighbors closer than this number will be
  considered as "close neighbors" (default: 0.8).
- *ontology_threshold* (float): neighbors closer in ontology than this number will
  be considered "CloseInOntology".
