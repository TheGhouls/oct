oct
===

[![Join the chat at https://gitter.im/karec/oct](https://badges.gitter.im/karec/oct.svg)](https://gitter.im/karec/oct?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![doc](https://readthedocs.org/projects/oct/badge/?version=latest)](http://oct.readthedocs.org/en/latest/)
[![Latest Version](https://img.shields.io/pypi/v/oct.svg?style=flat)](https://pypi.python.org/pypi/oct/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/oct.svg?style=flat)](https://pypi.python.org/pypi/oct/)
[![pypi](https://img.shields.io/pypi/status/oct.svg?style=flat)](https://pypi.python.org/pypi/oct/)
[![pypi](https://travis-ci.org/TheGhouls/oct.svg?branch=master)](https://travis-ci.org/TheGhouls/oct)
[![Coverage Status](https://coveralls.io/repos/github/TheGhouls/oct/badge.svg?branch=master)](https://coveralls.io/github/TheGhouls/oct?branch=master)


[Documentation](http://oct.readthedocs.org/en/latest/)

[OCT on pypi](https://pypi.python.org/pypi/oct)

follow us ! [@oct_py](https://twitter.com/oct_py)

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

```pip install oct```

Or using setuptools :

```python setup.py install```


Turrets
-------

[Python turret](https://github.com/karec/oct-turrets)

What's next ?
-------------

For documentation and examples, please visit the official documentation here : [doc](http://oct.readthedocs.org/en/latest/)

Contribution
------------

After cloning this repo you can install oct and dependencies with :

```
pip install -r requirements.txt && python setup.py install
```

After developping you can run the test suite with nose

```
nosetests -vdx tests/
```

Or with pytest

```
py.test -v tests/
```

Docker container for testing external publication
-------------------------------------------------

https://hub.docker.com/r/karec/oct/
