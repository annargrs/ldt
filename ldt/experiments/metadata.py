# -*- coding: utf-8 -*-
"""General infrastructure for experiments with automatically logged metadata.

LDT uses the metadata framework developed in the vecto library: the data
for each resource (embeddings, datasets) and experiment are contained in a
unique folder that contains a metadata.json file. Its contents depend on the
type of the resource. See `Vecto documentation
<https://vecto.readthedocs.io/en/docs/tutorial/metadata.html#the-embeddings
-metadata>`_for more details.
Metadata for all resources used in the experiment are automatically included
with the metadata for that experiment, to simplify analysis and improve
reproducibility of experiments. Each resource/experiment also has a UUID.

Todo:

    * distinct filenames from varying parameters and model names
    * testing the resuming of an experiment and detecting unprocessed files

"""

import os
import datetime
import abc
import uuid

import json
from vecto.utils.data import load_json, save_json

from ldt import __version__
from ldt.load_config import config


class Experiment(metaclass=abc.ABCMeta):
    """The top-level class for all experiments that provides the basic
    infrastructure. All specific experiment types must inherit from it."""

    # pylint: disable = too-many-arguments
    def __init__(self, experiment_name=config["experiments"]["experiment_name"],
                 extra_metadata=None,
                 dataset=config["experiments"]["vocab_sample"],
                 embeddings=config["experiments"]["embeddings"],
                 output_dir=os.path.join(config["path_to_resources"],
                                         "experiments"),
                 overwrite=config["experiments"]["overwrite"],
                 experiment_subfolder=None):
        """ Initializing an Experiment.

        Args:
            experiment_name (str): the human-readable name of an experiment
                (e.g. "Profiling CBOW with window size 2-10")
            extra_metadata (dict): any extra fields to be added to the
                experiment metadata (overwriting any previously existing fields)
            embeddings (list of str or None): a list of paths to input
                data (each containing a metadata.json file). If set to None,
                the config parameters will be ignored (for experiments where
                embedding metadata has already been processed and can be just
                copied over from the previous step.)
            output_dir (str): the *existing* path for saving the *subfolder*
                named with the specified experiment_name, where the output data
                and metadata.json file will be saved.
            dataset (str): the location of the dataset to be used in the
                experiment.
            overwrite (bool): if True, any previous data for the same
                experiment will be overwritten, and the experiment will be
                re-started. If metadata from previous experiment is not
                found, this setting is disregarded.
            experiment_subfolder (str): if provided, the experiment results
                will be saved to this subfolder of the "experiments" folder
        """

        if not isinstance(experiment_name, str):
            raise ValueError("Please specify experiment_name argument: a short "
                             "description of the experiment you're conducting.")

        self.output_dir = check_output(output_dir, experiment_subfolder,
                                       experiment_name)
        self.message = None
        if embeddings:
            self.embeddings = check_input(input_data=embeddings)

        self._overwrite = overwrite
        if self._overwrite:
            self._init_metadata(embeddings)

        else:
            metadata_path = os.path.join(self.output_dir, "metadata.json")
            if os.path.isfile(metadata_path):
                self.metadata = load_json(metadata_path)
            else:
                self._init_metadata(embeddings)
                self._overwrite = True

        self._load_dataset(dataset=dataset)
        if isinstance(extra_metadata, dict):
            self.metadata.update(extra_metadata)

    def _init_metadata(self, embeddings):
        """Metadata Initialization helper"""
        self.metadata = {}

        self.metadata["timestamp"] = {}
        self.metadata["version"] = "ldt v. " + __version__
        self.metadata["class"] = "experiment"
        if hasattr(self, "embeddings"):
            self.metadata["embeddings"] = []
            shared_subpath = check_shared_subpath(embeddings, "")
            for embedding in embeddings:

                meta_path = os.path.join(embedding, "metadata.json")
                if os.path.isfile(meta_path):
                    embedding_metadata = load_json(meta_path)
                    embedding_metadata["path"] = embedding
                else:
                    embedding_metadata = create_metadata_stub(embedding, shared_subpath)

                    save_json(embedding_metadata, meta_path)
                self.metadata["embeddings"].append(embedding_metadata)


    @abc.abstractmethod
    def _load_dataset(self, dataset):
        """Abstract method for experiment-specific helper methods that load
        the input data"""
        pass

    @abc.abstractmethod
    def _process(self, embeddings_path):
        """Abstract method for experiment-specific main methods that specify
        the procedure to be performed on each embedding. These methods are
        responsible for both processing and saving results for individual
        files, and incorporating any existing metadata for those resources"""
        raise NotImplementedError

    def save_metadata(self):
        """Saving the metadata for the given experiment"""
        # print("dumping metadata")
        # print(self.metadata)
        with open(os.path.join(self.output_dir, "metadata.json"), "w") as path:
            json.dump(self.metadata, fp=path, ensure_ascii=False, indent=4,
                      sort_keys=False, allow_nan=True)

    def _check_uuid_in_metadata(self, field, path):
        """Helper method to determine if a given embedding does have
        associated metadata"""
        for i in self.metadata[field]:
            if i["path"] == path and "uuid" in i:
                return i["uuid"]
        return None

    def _start_experiment(self):
        input_data = self.find_unprocessed_files()
        self.embeddings = input_data
        if not self.embeddings:
            print("\n", self.metadata["task"].upper(), ": no new data to process.\n")
            return None
        else:
            print("\n", self.metadata["task"].upper(), ": the following will be processed:\n", self.embeddings)
            if self.message:
                print(self.message)

    def get_results(self):
        """The basic routine for processing embeddings one-by-one, and saving
        the timestamps of when each file was started and finished."""

        self._start_experiment()
        if not self.embeddings:
            return None

        for i in self.embeddings:

            emb_uuid = self._check_uuid_in_metadata(field="embeddings", path=i)
            if emb_uuid:
                self.metadata["timestamp"][emb_uuid] = {}
                self.metadata["timestamp"][emb_uuid]["start_time"] = \
                    datetime.datetime.now().isoformat()
            else:
                self.metadata["timestamp"][i] = {}
                self.metadata["timestamp"][i]["start_time"] = \
                    datetime.datetime.now().isoformat()

            self._process(embeddings_path=i)
            if emb_uuid:
                self.metadata["timestamp"][emb_uuid]["end_time"] = \
                    datetime.datetime.now().isoformat()
            else:
                self.metadata["timestamp"][i]["end_time"] = \
                    datetime.datetime.now().isoformat()
            self._postprocess_metadata()
            self.save_metadata()

    def find_unprocessed_files(self):
        """Helper method for determining which embeddings have already been
        processed."""
        if not hasattr(self, "embeddings"):
            return []
        if self._overwrite:
            return self.embeddings
        seen = []
        for path in self.embeddings:
            to_check = [path]
            emb_uuid = self._check_uuid_in_metadata(field="embeddings", path=path)
            to_check += [emb_uuid]
            for i in to_check:
                if i:
                    if i in self.metadata["timestamp"]:
                        if "end_time" in self.metadata["timestamp"][i]:
                            seen.append(path)
        unprocessed = [x for x in self.embeddings if not x in seen]
        return unprocessed

    def _postprocess_metadata(self):
        """Helper method for experiments that require extra operations on
        metadata once the processing has been complete"""
        pass

    def get_fname_for_embedding(self, embeddings_path):

        """At the moment, filenames are created from model names of the
        embedding models, assumed to be unique. If no model names are found
        in metadata, directory names for folders that
        contained the initial embeddings. In that case, they better be
        unique. """

        if "embeddings" in self.metadata:
            for embedding in self.metadata["embeddings"]:
                if embedding["path"] == embeddings_path:
                    return embedding["model"]
        filename = os.path.split(embeddings_path)[-1]+".tsv"
        if os.path.isfile(filename):
            return filename

def check_input(input_data):
    """Helper function that makes sure that all input paths are valid."""
    if isinstance(input_data, list):
        # check that all input paths exist
        for i in input_data:
            if not os.path.exists(i):
                raise ValueError("Path", i, "does not exist.")
    return input_data

def check_output(output_dir, experiment_subfolder, experiment_name):
    """Helper function that makes sure that all output paths are valid."""
    if not isinstance(output_dir, str) or not os.path.isdir(output_dir):
        raise ValueError("Please specify output_dir argument: the "
                         "existing path where the output data for "
                         "experiment '" + experiment_name + "' will be saved.")
    else:
        if " " in experiment_name:
            experiment_name = experiment_name.replace(" ", "_")

        full_path = os.path.join(output_dir, experiment_name)
        if not os.path.isdir(full_path):
            os.mkdir(full_path)
        if experiment_subfolder:
            full_path = os.path.join(full_path, experiment_subfolder)
            if not os.path.isdir(full_path):
                os.mkdir(full_path)
    return full_path

def check_shared_subpath(embeddings, head):
    """Find the maximum removeable subpath that would still leave the model
    subfolders intelligible"""
    head = head + os.path.dirname(embeddings[0])
    for i in embeddings:
        if not i.startswith(head):
            return os.path.split(head)[0]
    embeddings = [x.strip(head) for x in embeddings]
    return check_shared_subpath(embeddings, head)

def create_metadata_stub(embedding, shared_subpath):
    """Creating a Vecto-style metadata stub for input embeddings. We highly
    recommend filling these stubs out right now, while you still remember what
    your data is and where it is from."""
    for i in [shared_subpath, embedding]:
        i = i.strip("/")
        i = i.strip("\\")
    model_name = embedding.replace(shared_subpath, "")
    for i in ["/", "\\"]:
        model_name = model_name.strip(i)
        model_name = model_name.replace(i, "_")
    metadata_stub = {}
    metadata_stub["path"] = embedding
    metadata_stub["uuid"] = str(uuid.uuid4())
    metadata_stub["class"] = "embeddings"
    metadata_stub["model"] = model_name
    metadata_stub["dimensionality"] = ""
    metadata_stub["window"] = ""
    metadata_stub["context"] = ""
    metadata_stub["cite"] = {}
    metadata_stub["corpus"] = [{"name": "",
                                "size": "",
                                "description": "",
                                "source": "",
                                "domain": "",
                                "language": [""],
                                "pre-processing": {
                                    "cleanup": "",
                                    "lowercasing": "",
                                    "tokenization": "",
                                    "lemmatization": "",
                                    "stemming": "",
                                    "POS_tagging": "",
                                    "syntactic_parsing": ""
                                    }
                               }],
    metadata_stub["vocabulary"] = {"size": "",
                                   "min_frequency": "",
                                   "lowercasing": ""}
    return metadata_stub

