"""
https://www.neuraldump.net/2017/06/how-to-suppress-python-unittest-warnings/

Complaining about unclosed resources by WordNet and Urllib2. This seems to be
expected behavior by both libraries, as unclosed objects are supposed to be
simply garbage-collected.
"""

import warnings

def ignore_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return do_test