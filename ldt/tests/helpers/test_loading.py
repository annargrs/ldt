import unittest
import os
from hurry.filesize import size
import ldt
from ldt.load_config import config as config

class Tests(unittest.TestCase):
    """The tests in this block inspect the file loaders for different
    formats."""

    @classmethod
    def setUpClass(cls):
        """Setting up the test variables."""
        cls.path = config["path_to_cache"].replace("cache", "file_formats")
        cls.res_vocab = {"banana", "apple", "5", "123abc"}
        cls.res_vocab_upper = {"Banana", "apple", "5", "123abc"}
        cls.res_2cols_freqdict = {"falcon": 2, "mid": 20, "5": 14, "has_not": 3}
        cls.res_2cols = {"falcon": "bird", "mid": "way", "5": "cat",
                         "has_not": "has"}
        cls.res_2cols_upper = {"falcon": "bird", "Mid": "way", "5": "cat",
                               "has_not": "has"}
        cls.res_dict = {'falcon': {'bird', 'hawk', 'eagle'},
                        'mid': {'way', 'middle', 'between'},
                        '5': {'cat', '1', '2'},
                        'has_not': {'been', 'without', 'has'}}
        cls.res_dict_upper = {'falcon': {'bird', 'Hawk', 'eagle'}, 'Mid': {
            'way', 'middle', 'between'}, '5': {'cat', '1', '2'}, 'has_not': {
            'been', 'without', 'has'}}
        cls.res_json_freqdict = {"cat": {"dog":1, "cheese":5},
                                 "mouse": {"cat":5, "cheese":6}}

    @classmethod
    def tearDownClass(cls):
        """Clearning up the test variables."""
        cls.path = None
        cls.res_vocab = None
        cls.res_vocab_upper = None
        cls.res_2cols_freqdict = None
        cls.res_2cols = None
        cls.res_2cols_upper = None
        cls.res_dict = None
        cls.res_dict_upper = None
        cls.res_json_freqdict = None

    def test_objectsize(self):
        res = ldt.helpers.loading.load_resource(format="tsv_dict",
                                                path=os.path.join(self.path,
                                                                  "2cols_list.tsv"))
        self.assertEqual(size(ldt.helpers.loading.get_object_size(res)), '1K')

# testing 1-col vocab files

    def test_load_vocab(self):
        res = ldt.helpers.loading.load_resource(format="vocab", path=
        os.path.join(self.path, "1col.vocab"), silent=True)
        self.assertEqual(res, self.res_vocab)

    def test_load_vocab_upper(self):
        res = ldt.helpers.loading.load_resource(format="vocab", path=
        os.path.join(self.path, "1col.vocab"), lowercasing=False, silent=True)
        self.assertEqual(res, self.res_vocab_upper)

# testing 2-col simple [word <tab> word] dicts

    def test_load_freqdict(self):
        res = ldt.helpers.loading.load_resource(format="freqdict", path=
        os.path.join(self.path, "2cols.freqdict"), lowercasing=True,
                                                silent=True)
        self.assertEqual(res, self.res_2cols_freqdict)

    def test_load_simple_dict(self):
        res = ldt.helpers.loading.load_resource(format="tsv_dict", path=
        os.path.join(self.path, "2cols.txt"), silent=True)
        self.assertEqual(res, self.res_2cols)

    def test_load_2coljson(self):
        res = ldt.helpers.loading.load_resource(format="json", path=
        os.path.join(self.path, "2cols.json"), silent=True)
        self.assertEqual(res, self.res_2cols)

    def test_load_2coljson_upper(self):
        res = ldt.helpers.loading.load_resource(format="json", path=
        os.path.join(self.path, "2cols.json"), lowercasing=False, silent=True)
        self.assertEqual(res, self.res_2cols_upper)

    def test_load_2colyaml(self):
        res = ldt.helpers.loading.load_resource(format="yaml", path=
        os.path.join(self.path, "2cols.yaml"), silent=True)
        self.assertEqual(res, self.res_2cols)

    def test_load_tsv_dict(self):
        res = ldt.helpers.loading.load_resource(format="tsv_dict",
                                                path=
        os.path.join(self.path, "2cols_list.tsv"), silent=True)
        self.assertEqual(res, self.res_dict)

    def test_load_tsv_dict_upper(self):
        res = ldt.helpers.loading.load_resource(format="tsv_dict",
                                                path=
        os.path.join(self.path, "2cols_list.tsv"), lowercasing=False,
                                                silent=True)
        self.assertEqual(res, self.res_dict_upper)

    def test_load_json(self):
        res = ldt.helpers.loading.load_resource(format="json",
                                                path =
        os.path.join(self.path, "2cols_list.json"), silent=True)
        self.assertEqual(res, self.res_dict)

    def test_load_json_freqdict(self):
        res = ldt.helpers.loading.load_resource(format="json_freqdict",
                                                path =
        os.path.join(self.path, "json_freqdict.json"), silent=True)
        print(res)
        self.assertEqual(res, self.res_json_freqdict)

    def test_load_yaml(self):
        res = ldt.helpers.loading.load_resource(format="yaml",
                                                path=
        os.path.join(self.path, "2cols_list.yaml"), silent=True)
        self.assertEqual(res, self.res_dict)

if __name__ == '__main__':
    unittest.main()