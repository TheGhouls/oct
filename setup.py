__author__ = 'manu'

import os
from setuptools import setup
from oct import __version__

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='oct',
    version=__version__,
    author='Emmanuel Valette',
    author_email='manu.valette@gmail.com',
    packages=['oct', 'oct.core', 'oct.multimechanize', 'oct.testing',
              'oct.multimechanize.utilities', 'oct.utilities', 'oct.tools'],
    package_data={'oct.utilities': ['templates/css/*']},
    description="A library based on multi-mechanize for performances testing, using custom browser for writing tests",
    long_description=long_description,
    url='https://github.com/karec/oct',
    download_url='https://github.com/karec/oct/archive/master.zip',
    keywords=['testing', 'multi-mechanize', 'perfs', 'webscrapper', 'browser', 'web', 'performances', 'lxml'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'
    ],
    install_requires=[
        'argparse',
        'requests',
        'lxml',
        'celery',
        'cssselect',
        'pygal',
        'cairosvg',
        'tinycss'
    ]
)
