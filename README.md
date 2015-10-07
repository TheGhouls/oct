oct
===
[![doc](https://readthedocs.org/projects/oct/badge/?version=latest)](http://oct.readthedocs.org/en/latest/)
[![Latest Version](https://img.shields.io/pypi/v/oct.svg?style=flat)](https://pypi.python.org/pypi/oct/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/oct.svg?style=flat)](https://pypi.python.org/pypi/oct/)
[![pypi](https://img.shields.io/pypi/status/oct.svg?style=flat)](https://pypi.python.org/pypi/oct/)
[![pypi](https://travis-ci.org/karec/oct.svg?branch=master)](https://travis-ci.org/karec/oct)

[Documentation](http://oct.readthedocs.org/en/latest/)

[OCT on pypi](https://pypi.python.org/pypi/oct)

Python Version | Tested |
-------------- | -------|
Python >= 2.7.x|Tested|
Python >= 3.4|Tested|

Description
-----------
OCT stand for Open Charge Tester and his goal is simple : make a library that give you the tools for writing performances tests on webiste.
Writing your script for browsing a web site is done with a custon minimal browser, based on lxml.

If you know multi-mechnanize as well, we've started using it for the core, but now we have removed many code from it and added many features
 like :
* update render of graphics
* update command for new projects
* more information in config file
* new config file format
* customisable jinja template
* customisable configuration files
* new commands

Installation
------------
You can install OCT with pip :

`pip install oct`

Or using setuptools :

`python setup.py install`

What's next ?
-------------


For documentation and examples, please visit the official documentation here : [doc](http://oct.readthedocs.org/en/latest/)

Roadmap
-------

Actually the project is in the alpha version, non-suitable for production, but will be under active developpement for some featurs like :
* Full zeromq integration for distribution of the tests (in progress)
* Packaging turrets commands
* More tools commands
* More simple deployement
* Light turrets management
* More fancy templates
* Generic use of any library for testing

Contribution
------------

Fork, pull requests, issues, we're open to any proposition !
