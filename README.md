oct
===

[![Join the chat at https://gitter.im/karec/oct](https://badges.gitter.im/karec/oct.svg)](https://gitter.im/karec/oct?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![doc](https://readthedocs.org/projects/oct/badge/?version=latest)](http://oct.readthedocs.org/en/latest/)
[![Latest Version](https://img.shields.io/pypi/v/oct.svg?style=flat)](https://pypi.python.org/pypi/oct/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/oct.svg?style=flat)](https://pypi.python.org/pypi/oct/)
[![pypi](https://img.shields.io/pypi/status/oct.svg?style=flat)](https://pypi.python.org/pypi/oct/)
[![pypi](https://travis-ci.org/TheGhouls/oct.svg?branch=master)](https://travis-ci.org/TheGhouls/oct)

[Documentation](http://oct.readthedocs.org/en/latest/)

[OCT on pypi](https://pypi.python.org/pypi/oct)

follow us ! [@oct_py](https://twitter.com/oct_py)

Python Version | OK ?   |
-------------- | -------|
Python >= 2.7.x|OK|
Python >= 3.4|OK|
Python == 3.5|OK|

Description
-----------

OCT stand for Open Charge Tester and his goal is simple : give you the tools to load test just anything !

In the first part of the OCT project we were based on the multi-mechanize project, but now most of the multi-mechanize
code has been replaced or removed. The OCT project is not for just testing web, it's for testing anything !

Yes simple as that, we give you the tools to create a test project, to distribute it, to run it and to get its performance
report. But when it come to the tests, you could just use anything ! Want to test a website ? you can use Selenium,
phantomjs, mechanize, etc. You want to use custom libraries for testing ? Not a problem, you are free to write just anything
in your test.

Plus : the client part has been removed from the oct package and it's now in a separate package, but that's not only
for a more explicit project or a lighter client. Thanks to zeromq you can write a turret (the client part) in any
avaible language for zeromq ! see [zeromq documentation](http://zeromq.org/bindings:_start) and then connect it to a
running instance of OCT !

We worked hard on OCT during the last few months but the project will stay in alpha version for a few release, because
yes the project work but we still need more unit tests and we realy need to update the doc, because actually
the documentation does not explain how to use OCT and how to run it.

Installation
------------
You can install OCT with pip :

`pip install oct`

Or using setuptools :

`python setup.py install`


Turrets
-------

[Python turret](https://github.com/karec/oct-turrets)

What's next ?
-------------

For documentation and examples, please visit the official documentation here : [doc](http://oct.readthedocs.org/en/latest/)

Roadmap
-------

For the 0.3.8 version :

* More unit test for cover the new functioning of the project
* A whole new documentation explaning how to create a project, how to package it and run it, how to write tests and how
to write custom turrets

For the 0.3.9 version :

* Performances optimisations
* Testing and debug

For the 0.4.0 version :

* Release of the beta version

Contribution
------------

Fork, pull requests, issues, we're open to any proposition !
