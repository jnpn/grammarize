from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'DESCRIPTION.rst')) as f:
    long_description = f.read()

setup(
    name='grammarize',
    version='0.0.1a2',
    description='tree grammar (partial) inferer',
    long_description=long_description,
    url='http://ponin.johan.free.fr/',
    author='Johan PONIN',
    author_email='johan.ponin.pro@gmail.com',
    license='GPLv2',
    package_dir={'grammarize': 'grammarize'},
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: BNF',
    ],
    keywords='tree grammar xml bnf',
    packages={'grammarize': 'grammarize'},
    dependency_links=[
        'git+https://github.com/jnpn/sax.git',
    ],
    install_requires=[
        'click'
    ],
    extras_require={
        'dev': ['check-manifest', 'isort'],
        'test': ['nosetest']
    },
    entry_points={
        'console_scripts': [
            'grammarize=grammarize:main'
        ]
    }
)
