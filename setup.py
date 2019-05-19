from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst')) as f:
    long_description = f.read()

setup(
    name='grammarize',
    version='0.0.1a1',
    description='tree grammar (partial) inferer',
    long_description=long_description,
    url='http://ponin.johan.free.fr/',
    author='Johan PONIN',
    author_email='johan.ponin.pro@gmail.com',
    license='GPLv2',
    package_dir={'grammarize': 'grammarize'},
    classifiers=[],
    keywords='tree grammar xml bnf',
    packages={'grammarize': 'grammarize'},
    test_suite=['tests.test_xml'],
    install_requires=[],
    extras_require={
        'dev': ['check-manifest'],
        'test': ['nosetest']
    },
    entry_points={
        'console_scripts': [
            'grammarize=grammarize:main'
        ]
    }
)
