
import os
import datetime
import abc

import json
import vecto

from ldt import __version__
from ldt.load_config import config



class Experiment(metaclass=abc.ABCMeta):
    """The top-level class for all experiments that provides the basic
    infrastructure. All specific experiment types must inherit from it."""
    def __init__(self, experiment_name=None, extra_metadata=None,
                 input_data=None, output_dir=None, overwrite=False):
        """ Initializing an Experiment.

        Args:
            experiment_name (str): the human-readable name of an experiment
                (e.g. "Profiling CBOW with window size 2-10")
            extra_metadata (dict): any extra fields to be added to the
                experiment metadata (overwriting any previously existing fields)
            input_data (list of str or str): either a list of paths to input
                data (each containing a metadata.json file), or a single
                path to a parent folder, the subfolders of which are to be
                processed.
            output_dir (str): the *existing* path for saving the *subfolder*
                named with the specified experiment_name, where the output data
                and metadata.json file will be saved.
            overwrite (bool): if True, any previous data for the same
                experiment will be overwritten, and the experiment will be
                re-started.
        """

        if not isinstance(experiment_name, str):
            raise ValueError("Please specify experiment_name argument: a short "
                             "description of the experiment you're conducting.")

        output_dir = check_output(output_dir, experiment_name)

        input_data = check_input(input_data)


        if overwrite:

            self._metadata = {}

            self._metadata["timestamp"] = []
            self._metadata["version"] = "ldt v. "+__version__
            self._metadata["class"] = "experiment"
            self._metadata["input_data"] = input_data

            self._metadata["timestamp"].append(("start_time",
                                                datetime.datetime.now().isoformat()))

        else:
            metadata_path = os.path.join(output_dir, "metadata.json")
            if os.path.isfile(metadata_path):
                with open(metadata_path, "r") as f:
                    self._metadata = json.load(metadata_path)

        if isinstance(extra_metadata, dict):
            self._metadata.update(extra_metadata)

    @abc.abstractmethod
    def _process(self, input_data, output_dir):
        # these functions should both process and save results for individual
        # files, and incorporating any existing metadata for those resources
        raise NotImplementedError

    def save_metadata(self, input_data, output_dir):
        with open(os.path.join(output_dir, "metadata.json"), "w") as f:
            json.dump(self._metadata, fp=f, ensure_ascii=False, indent=4,
                      sort_keys=False, allow_nan=True)

    def get_results(self, input_data, output_dir):
        for i in input_data:
            self._process(input_data=i, output_dir=output_dir)
            self._metadata["timestamp"].append\
                ((i, datetime.datetime.now().isoformat()))

    def resume(self, input_data, output_dir):
        raise NotImplementedError



def check_input(output_dir, input_data):

    if isinstance(input_data, list):
        # check that all input paths exist
        for i in input_data:
            if not os.path.exists(i):
                raise ValueError("Path", i, "does not exist.")

    elif isinstance(input_data, str):
        # if the input is a string, it must be an existing folder
        if not os.path.isdir(input_data):
            raise ValueError("Path", input_data, "does not exist.")
        # converting the folder to a list of constituent paths
        else:
            input_data = os.listdir(input_data)
            if "metadata.json" in filenames:
                filenames = filenames.remove("metadata.json")
            new_data = []
            for i in enumerate(filenames):
                new_data.append(os.path.join(input_data, i[1]))
            return new_data
    return input_data

def check_output(output_dir, experiment_name):

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

    return full_path


class ExperimentWithNeighborhoods(Experiment):
    pass




class ExperimentWithEmbeddings(Experiment):
    # the constant feature is the input list of dirs with embeddings,
    # process_embeddings function to be redefined in daughter experiment classes
    # experiment status
    # _get_neighbors is a hidden method
    pass

class ExperimentWithNeighborhoods():
    pass

class Metadata():

    def __init__(self, experiment_name=None, task="annotate_neighbors",
                 extra_metadata=None, input_data=None):

        # for vecto
        # supported_classes = ["experiment", "embeddings", "dataset", "corpus", "vocabulary"]
        # if metadata_class not in supported_classes:
        #     raise ValueError("The supported classes of metadata are: " +
        #                      ", ".join(supported_classes)+".")

        supported_tasks = ["get_neighbors", "annotate_neighbors"]
        if task not in supported_tasks:
            raise ValueError("The supported experiment tasks are: " +
                             ", ".join(supported_tasks)+".")

        self.required_fields = ["timestamp", "class", "version"]
        self._metadata={}
        self._metadata["timestamp"] = datetime.datetime.now().isoformat()
        self._metadata["version"] = "ldt v. "+__version__
        self._metadata["class"] = "experiment"
        self._metadata["progress"] = []

        if task == "get_neighbors":
            self.get_neighbors(experiment_name=experiment_name, task=task)

        if isinstance(extra_metadata, dict):
            self._metadata.update(extra_metadata)

    def get_neighbors(self, experiment_name, task):
        """Generating experiment metadata consistent with Vecto library format.
        See `Vecto docs <https://vecto.readthedocs.io/en/docs/tutorial/metadata
        .html>`_ for more detail.

        Args:
            experiment_name: the human-readable name of the experiment (e.g.
                "Profiling CBOW dims 25-500")
            task: the type of experiment being performed (in LDT - generating or
                annotating vector neighborhoods)

        Returns:
            (dict): dictionary with metadata fields

        """
        self._metadata["name"] = experiment_name
        self._metadata["task"] = task
        self._metadata["version"] = "ldt v. "+__version__+", vecto v. "+vecto.VERSION
        self._metadata["cite"] = \
            [{"contribution": "LDT library",
              "bibtex": {
                  "type": "inproceedings",
                  "id": "RogersAnanthakrishnaEtAl_2018",
                  "author": [{"name": "Anna Rogers"},
                             {"name": "Shashwath Hosur Ananthakrishna"},
                             {"name": "Anna Rumshisky"}],
                  "title": "What's in Your Embedding, And How It Predicts Task "
                           "Performance",
                  "url": "http://aclweb.org/anthology/C18-1228",
                  "address": "Santa Fe, New Mexico, USA, August 20-26, 2018",
                  "publisher": "ACL",
                  "booktitle": "Proceedings of the 27th International "
                               "Conference on Computational Linguistics",
                  "year": 2018,
                  "pages": "2690–2703"
                  }
             }
            ]


def generate_identifiable_filenames():
    pass
