__author__ = 'manu'

import os
from setuptools import setup, find_packages
from oct import __version__

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

setup(
    name='oct',
    version=__version__,
    author='Emmanuel Valette',
    author_email='manu.valette@gmail.com',
    packages=['oct', 'oct.core', 'oct.multimechanize', 'oct.testing',
              'oct.multimechanize.utilities', 'oct.utilities', 'oct.tools'],
    package_data={'oct.utilities': ['templates/css/*']},
    description="""
    A library based on multi-mechanize for performances testing, using custom browser for writing tests

    See the documentation at http://oct.readthedocs.org/en/latest/_

    Github repository : https://github.com/karec/oct_

    .. _http://oct.readthedocs.org/en/latest/: http://oct.readthedocs.org/en/latest/
    .. _https://github.com/karec/oct: https://github.com/karec/oct

    """,
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
        'tinycss',
        'six'
    ],
    entry_points={'console_scripts': [
        'multimech-run = oct.multimechanize.utilities.run:main',
        'multimech-newproject = oct.multimechanize.utilities.newproject:main',
        'multimech-gridgui = oct.multimechanize.utilities.gridgui:main',
        'oct-run = oct.utilities.run:oct_main',
        'oct-newproject = oct.utilities.newproject:main',
        'octtools-sitemap-to-csv = oct.tools.xmltocsv:sitemap_to_csv',
        'octtools-user-generator = oct.tools.email_generator:email_generator'
    ]},
)
