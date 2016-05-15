import os
from setuptools import setup
from oct import __version__

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='oct',
    version=__version__,
    author='TheGhouls',
    author_email='manu.valette@gmail.com',
    packages=['oct', 'oct.core', 'oct.utilities', 'oct.tools', 'oct.results'],
    package_data={
        'oct.utilities': [
            'templates/css/*',
            'templates/configuration/*',
            'templates/html/*',
            'templates/scripts/*',
            'templates/javascript/*',
            'templates/fonts/*'
        ]
    },
    description="A library for performances testing, give you the tools for load testing anything with any language",
    long_description=long_description,
    url='https://github.com/TheGhouls/oct',
    download_url='https://github.com/TheGhouls/oct/archive/master.zip',
    keywords=['testing', 'perfs', 'performances', 'web', 'load', 'zeromq'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    install_requires=[
        'pygal',
        'peewee',
        'oct-turrets>=0.2.4',
        'six',
        'pyzmq',
        'numpy',
        'jinja2',
        'pandas',
        'ujson'
    ],
    entry_points={'console_scripts': [
        'oct = oct.utilities.commands:main'
    ]},
)
