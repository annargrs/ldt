from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import ldt

here = os.path.abspath(os.path.dirname(__file__))

packages = find_packages(here, exclude=["*.tests", "*.tests.*", "tests.*", "tests"])

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.rst', 'CHANGES.txt')
requirements = read('requirements.txt')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='ldt',
    version=ldt.__version__,
    url='http://ldtoolkit.space/',
    license='Apache Software License',
    author='Anna Rogers',
    tests_require=['pytest'],
    install_requires=["ruamel.yaml", "wiktionaryparser==0.0.7",
                      "hurry.filesize", "timeout-decorator", "inflect",
                      "nltk", "vecto", "pandas", "pyenchant"],
    cmdclass={'test': PyTest},
    author_email='anna_rogers@uml.edu',
    description='Linguistic diagnostics for word embeddings',
    long_description=long_description,
    packages=packages,
    package_dir={"ldt":"ldt"},
    include_package_data=True,
    package_data={'ldt': ['test/sample_files/ldt-config.yaml']},
    entry_points={},
    zip_safe=False,
    platforms='any',
    test_suite='ldt.test.test_ldt',
    classifiers = [
        'Programming Language :: Python',
        'Natural Language :: English',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        "Topic :: Text Processing :: Linguistic"
        ],
    extras_require = {
        'testing': ['pytest'],
    }
)