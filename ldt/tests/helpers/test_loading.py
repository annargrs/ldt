import unittest
import os
from hurry.filesize import size
import ldt
from ldt.load_config import config as config


# path = os.path.abspath("./sample_files/file_formats")
path = config["path_to_cache"].replace("cache", "file_formats")

res_vocab = {"banana", "apple", "5", "123abc"}
res_vocab_upper = {"Banana", "apple", "5", "123abc"}

res_2cols_freqdict = {"falcon": 2, "mid": 20, "5": 14, "has_not": 3}
res_2cols = {"falcon": "bird", "mid": "way", "5": "cat", "has_not": "has"}
res_2cols_upper = {"falcon": "bird", "Mid": "way", "5": "cat", "has_not": "has"}


res_dict = {'falcon': {'bird', 'hawk', 'eagle'}, 'mid': {'way', 'middle',
            'between'}, '5': {'cat', '1', '2'}, 'has_not': {'been',
            'without',  'has'}}
res_dict_upper = {'falcon': {'bird', 'Hawk', 'eagle'}, 'Mid': {'way',
            'middle', 'between'}, '5': {'cat', '1', '2'}, 'has_not':
            {'been', 'without',  'has'}}

class Tests(unittest.TestCase):
    """The tests in this block inspect the file loaders for different
    formats."""

    def test_objectsize(self):
        res = ldt.helpers.loading.load_resource(format="tsv_dict",
                                                path=os.path.join(path,
                                                                  "2cols_list.tsv"))
        self.assertEqual(size(ldt.helpers.loading.get_object_size(res)), '1K')

# testing 1-col vocab files

    def test_load_vocab(self):
        res = ldt.helpers.loading.load_resource(format = "vocab", path =
        os.path.join(path, "1col.vocab"))
        self.assertEqual(res, res_vocab)

    def test_load_vocab_upper(self):
        res = ldt.helpers.loading.load_resource(format = "vocab", path =
        os.path.join(path, "1col.vocab"), lowercasing = False)
        self.assertEqual(res, res_vocab_upper)

# testing 2-col simple [word <tab> word] dicts

    def test_load_freqdict(self):
        res = ldt.helpers.loading.load_resource(format = "freqdict", path =
        os.path.join(path, "2cols.freqdict"), lowercasing = True)
        self.assertEqual(res, res_2cols_freqdict)

    def test_load_simple_dict(self):
        res = ldt.helpers.loading.load_resource(format = "tsv_dict", path =
        os.path.join(path, "2cols.txt"))
        self.assertEqual(res, res_2cols)

    def test_load_2coljson(self):
        res = ldt.helpers.loading.load_resource(format = "json", path =
        os.path.join(path, "2cols.json"))
        self.assertEqual(res, res_2cols)

    def test_load_2coljson_upper(self):
        res = ldt.helpers.loading.load_resource(format = "json", path =
        os.path.join(path, "2cols.json"), lowercasing = False)
        self.assertEqual(res, res_2cols_upper)

    def test_load_2colyaml(self):
        res = ldt.helpers.loading.load_resource(format = "yaml", path =
        os.path.join(path, "2cols.yaml"))
        self.assertEqual(res, res_2cols)

    def test_load_tsv_dict(self):
        res = ldt.helpers.loading.load_resource(format = "tsv_dict",
                                                path =
        os.path.join(path, "2cols_list.tsv"))
        self.assertEqual(res, res_dict)

    def test_load_tsv_dict_upper(self):
        res = ldt.helpers.loading.load_resource(format = "tsv_dict",
                                                path =
        os.path.join(path, "2cols_list.tsv"), lowercasing = False)
        self.assertEqual(res, res_dict_upper)

    def test_load_json(self):
        res = ldt.helpers.loading.load_resource(format = "json",
                                                path =
        os.path.join(path, "2cols_list.json"))
        self.assertEqual(res, res_dict)

    def test_load_json(self):
        res = ldt.helpers.loading.load_resource(format = "yaml",
                                                path =
        os.path.join(path, "2cols_list.yaml"))
        self.assertEqual(res, res_dict)



if __name__ == '__main__':
    unittest.main()