===============================
Annotating vector neighborhoods
===============================

----------------
Input and output
----------------

Automatic annotation of vector neighborhoods is the core function of LDT.
The input to this step is pre-computed vector neighborhood files, generated
as described in :ref:`Generating vector neighborhood files`.

The basic usage is as follows:

>>> experiment = ldt.experiments.AnnotateVectorNeighborhoods(
    experiment_name="just testing", ld_scores=["Synonyms", "Antonyms"],
    overwrite=True)
>>> experiment.get_results()

LDT will add columns with data for the specified types of relations (`ld_scores`)
to the original vector neighborhood files. The data will be saved in the
`experiments\neighbors_annotated\just_testing` subfolder
in your ldt data location. Example output:

+-------------+------+---------------+--------------------+----------+----------+
| Target      | Rank | Neighbor      | Similarity         | Synonyms | Antonyms |
+-------------+------+---------------+--------------------+----------+----------+
| paradox     | 1    | theory        | 0.9357089996337892 | False    | False    |
+-------------+------+---------------+--------------------+----------+----------+
| paradox     | 2    | illusion      | 0.9308078289031982 | False    | False    |
+-------------+------+---------------+--------------------+----------+----------+
| premiership | 1    | semi-final    | 0.962702751159668  | False    | False    |
+-------------+------+---------------+--------------------+----------+----------+
| premiership | 2    | decider       | 0.9600796699523926 |          |          |
+-------------+------+---------------+--------------------+----------+----------+

Note that for missing vocabulary entries the table cells will be left empty.

Alongside with the annotated files, LDT will automatically save the metadata for
this experiment: uuid, timestamps for starting and ending annotation of each file,
metadata for input embeddings (from the neighborhood metadata) and all the settings
in the ldt config file.

Crucially, metadata for this experiment also includes **coverage**: how many
neighbor words were not found in any resources. The specific pairs that were
missed will also be logged. A separate entry is failed pairs: the entries on which
LDT failed internally for some reason. If you get any of these, please let us know.

.. code-block:: json

    {
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

---------------------
What you can annotate
---------------------

Currently the value of `ld_scores` parameter can include any combination of the following
values:

    - "SharedPOS",
    - "SharedMorphForm",
    - "SharedDerivation",
    - "NonCooccurring",
    - "GDeps",
    - "TargetFrequency",
    - "NeighborFrequency",
    - "Associations",
    - "ShortestPath",
    - "Synonyms",
    - "Antonyms",
    - "Meronyms",
    - "Hyponyms",
    - "Hypernyms",
    - "OtherRelations",
    - "Numbers",
    - "ProperNouns",
    - "Noise",
    - "URLs",
    - "Filenames",
    - "ForeignWords",
    - "Hashtags"
    - 'TargetFrequency',
    - 'NeighborFrequency'.

See `this page <http://ldtoolkit.space/ldscores/>`_ for more details on ld scores.

You can also use `ld_scores="all"` to use all available ld_scores.

Note:

    This class provides special treatment for *GDeps* and *NonCooccurring*:
    they require lookup in large files, and are off by default. Use
    `gdeps=True` and `cooccurrence=True` to turn them on, and make sure
    you have at least 32Gb RAM.

----------------------------
Setting up the LDT resources
----------------------------

LDT provides a lot of lexicographic, morphological and other resources
(see `ref`:Linguistic resources in LDT:). Choosing what resources you want to use
is done via the optional `ldt_analyzer` argument of
:class:`~ldt.experiments.annotate.AnnotateVectorNeighborhoods`. You can pass a
pre-initialized instance of :class:`~ldt.relations.pair.RelationsInPair`
(see section :ref:`Combining information from ldt word objects`).

The gist of default settings is to rely on WordNet and Wiktionary, and not use
BabelNet. Memory-intensive lookup of cooccurrence and GDeps data is also off
by default.

------------------
Why is it so slow?
------------------

Wiktionary and BabelNet are queried online, which slows down the analysis.
The NLTK WordNet library is also not particularly fast. Full analysis with WordNet
and Wiktionary only takes 4-7 seconds per word pair. We do plan to move this offline;
stay tuned for LDT updates.

The good news is that in large-scale experiments with embeddings trained on the same
corpus many target:neighbor pairs are the same, and LDT reuses previously computed
data whenever possible. So the annotation will be slow for the first files, but
faster for the rest.

