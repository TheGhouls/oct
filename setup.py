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
              'oct.multimechanize.utilities', 'oct.utilities', 'oct.tools', 'oct.results'],
    package_data={
        'oct.utilities': ['templates/css/*', 'templates/configuration/*', 'templates/html/*', 'templates/scripts/*']
    },
    description="A library for performances testing, give you the tools for load testing anything",
    long_description=long_description,
    url='https://github.com/karec/oct',
    download_url='https://github.com/karec/oct/archive/master.zip',
    keywords=['testing', 'perfs', 'performances', 'web', 'load', 'zeromq'],
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
        'pygal',
        'peewee',
        'oct-turrets',
        'six',
        'pyzmq',
        'numpy',
        'jinja2'
    ],
    entry_points={'console_scripts': [
        'multimech-run = oct.multimechanize.utilities.run:main',
        'multimech-newproject = oct.multimechanize.utilities.newproject:main',
        'multimech-gridgui = oct.multimechanize.utilities.gridgui:main',
        'oct-run = oct.utilities.run:main',
        'oct-newproject = oct.utilities.newproject:main',
        'octtools-sitemap-to-csv = oct.tools.xmltocsv:main',
        'octtools-user-generator = oct.tools.email_generator:email_generator',
        'oct-tocsv = oct.tools.results_to_csv:main',
        'oct-rebuild-results = oct.tools.rebuild_results:main',
        'oct-pack-turrets = oct.utilities.pack:main'
    ]},
)
