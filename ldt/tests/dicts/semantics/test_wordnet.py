import unittest
import os

os.environ["TESTING_LDT"] = "TRUE"

import ldt
from ldt.helpers.ignore import ignore_warnings

class Tests(unittest.TestCase):
    """
    The tests in this block inspect the WordNet functions: the pre-computed
    output is expected to be contained, but the module is not punished for
    new words not in the pre-computed lists - in case the dictionaries get
    updated.
    """

    @ignore_warnings
    def test_wiktionary_initialization(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        self.assertEqual(test.language, "en")

    @ignore_warnings
    def test_word_in_wordnet(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        self.assertFalse(test.is_a_word("cattttt"))

    @ignore_warnings
    def test_antonyms(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        res = test.get_relation("white", relation="antonyms", synonyms=False)
        ok = ['black', 'blacken']
        for w in ok:
            self.assertIn(w, ok)

    @ignore_warnings
    def test_all_antonyms(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        res = test.get_relation("white", relation="antonyms", synonyms=True)
        ok = ['unclean', 'black', 'blacken', 'bloody', 'dirty']
        for w in ok:
            self.assertIn(w, res)

    @ignore_warnings
    def test_synonyms(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        res = test.get_relation("car", relation="synonyms", synonyms=True)
        ok = ['machine', 'cable_car', 'motorcar', 'car', 'auto',
              'railroad_car', 'railcar', 'railway_car', 'gondola',
              'elevator_car', 'automobile']
        for w in ok:
            self.assertIn(w, res)

    @ignore_warnings
    def test_hyponyms(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        test.lowercasing = False
        res = test.get_relation("weekday", relation="hyponyms", synonyms=False)
        ok = ['Friday', 'Tuesday', 'feria', 'workday', 'Monday',
              'Saturday', 'Wednesday', 'Thursday']
        for w in ok:
            self.assertIn(w, res)

    @ignore_warnings
    def test_all_hyponyms(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        test.lowercasing = False
        res = test.get_relation("weekday", relation="hyponyms", synonyms=True)
        ok = ['Friday', 'Sat', 'Tuesday', 'Wednesday', 'feria', 'Tues',
              'Midweek', 'work_day', 'working_day', 'workday', 'Monday',
              'Saturday', 'Mon', 'Th', 'Sabbatum', 'Fri', 'Thursday', 'Wed']
        for w in ok:
            self.assertIn(w, res)

    @ignore_warnings
    def test_hypernyms(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        res = test.get_relation("girl", relation="hypernyms", synonyms=False)
        ok = ['female', 'female_offspring', 'lover', 'woman']
        for w in ok:
            self.assertIn(w, res)

    @ignore_warnings
    def test_all_hypernyms(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        res = test.get_relation("girl", relation="hypernyms", synonyms=True)
        ok = ['adult_female', 'female', 'female_offspring', 'female_person',
              'lover', 'woman']
        for w in ok:
            self.assertIn(w, res)

    @ignore_warnings
    def test_meronyms(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        test.lowercasing = False
        res = test.get_relation("church", relation="meronyms", synonyms=False)
        ok = ['Christian', 'amen_corner', 'apse', 'chancel', 'church_tower',
              'lady_chapel', 'narthex', 'nave', 'presbytery', 'rood_screen',
              'side_chapel', 'transept', 'vestry']
        for w in ok:
            self.assertIn(w, res)

    @ignore_warnings
    def test_all_meronyms(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        test.lowercasing = False
        res = test.get_relation("church", relation="meronyms", synonyms=True)
        ok = ['Christian', 'amen_corner', 'apse',  'apsis', 'bema',
              'chancel', 'church_tower', 'lady_chapel', 'narthex', 'nave',
              'presbytery', 'rood_screen', 'sacristy', 'sanctuary',
              'side_chapel', 'transept', 'vestry']
        for w in ok:
            self.assertIn(w, res)

    @ignore_warnings
    def test_part_meronyms(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        res = test.get_relation("church", relation="part_meronyms",
                                synonyms=False)
        ok = ['amen_corner', 'apse', 'chancel', 'church_tower',
              'lady_chapel', 'narthex', 'nave', 'presbytery', 'rood_screen',
              'side_chapel', 'transept', 'vestry']
        for w in ok:
            self.assertIn(w, res)

    @ignore_warnings
    def test_member_meronyms(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        test.lowercasing = False
        res = test.get_relation("church", relation="member_meronyms",
                            synonyms=False)
        ok = ['Christian']
        for w in ok:
            self.assertIn(w, res)

    @ignore_warnings
    def test_substance_meronyms(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        res = test.get_relation("paper" , relation="substance_meronyms",
                            synonyms=False)
        ok = ['cellulose']
        for w in ok:
            self.assertIn(w, res)

    @ignore_warnings
    def test_all_hypernyms(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        res = test.get_relation("girl", relation="hypernyms", synonyms=True)
        ok = ['adult_female', 'female', 'female_offspring', 'female_person',
              'lover', 'woman']
        for w in ok:
            self.assertIn(w, res)

    @ignore_warnings
    def test_get_relations(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        res = test.get_relations("girl", relations=("hypernyms", "synonyms"),
        synonyms=False)
        checks = len(res)==2 and "female" in res["hypernyms"]
        self.assertTrue(checks)

    @ignore_warnings
    def test_get_relations_reduce(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        res = test.get_relations("girl", relations=("hypernyms", "synonyms",
                                "holonyms"), synonyms=False, reduce=True)
        checks = len(res)==2 and "female" in res["hypernyms"]
        self.assertTrue(checks)

    @ignore_warnings
    def test_get_relations_none(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        res = test.get_relations("girl", relations=("holonyms"),
                                 synonyms=False, reduce=True)
        self.assertEqual(res, {})

    @ignore_warnings
    def test_definitions(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        res = test.get_definitions("cat")
        self.assertIn("roar", res[1]["def"])

    @ignore_warnings
    def test_words_in_definitions(self):
        test = ldt.dicts.semantics.wordnet.en.WordNet()
        res = test.get_words_in_definitions("cat")
        self.assertIn("roar", res)

if __name__ == '__main__':
    unittest.main()