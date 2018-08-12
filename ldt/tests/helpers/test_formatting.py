import unittest

import ldt


class Tests(unittest.TestCase):
    '''
    The tests in this block inspect the Wiktionary functionality:
    updating the vocab list cache and retrieving entry data.
    '''

    def test_remove_bracketed_text(self):
        res = ldt.helpers.formatting.remove_text_inside_brackets("(See also) "
                                                                 "cat")
        self.assertEqual(res, 'cat')

    def test_spacing(self):
        res = ldt.helpers.formatting.get_spacing_variants("good night")
        self.assertEqual(res, ["good night", "good_night", "good-night"])

    def test_stripping_trash(self):
        res = ldt.helpers.formatting.strip_non_alphabetical_characters(
            "%^&_cat&*(", ignore = ("_"))
        self.assertEqual(res, "_cat")

if __name__ == '__main__':
    unittest.main()