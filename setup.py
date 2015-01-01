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
    description='A library based on multi-mechanize for performances testing',
    url='https://github.com/karec/oct',
    download_url='https://github.com/karec/oct/archive/master.zip',
    keywords=['testing', 'mechanize', 'perfs'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=[
        'argparse',
        'mechanize',
        'requests',
        'matplotlib',
        'beautifulsoup4',
        'requests-cache',
        'celery'
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
