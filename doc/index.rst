.. oct documentation master file, created by
   sphinx-quickstart on Thu Dec 18 15:29:32 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to oct's documentation!
===============================

Oct stand for Open Charge Tester, the goal of this project is to give you the basics tools for writing simple tests. The
tests are simple python scripts that make calls to web page or web service, submit data, login, etc...
OCT will give you the tools for easily write your test.

This documentation will provide you basics examples for write your tests, use oct-tools, lunch tests, get the results or even customize the results to fit your needs

Note that the OCT project is in early development and is not suitable for production.

If you want to contribute you're welcome ! Check the git, fork the project, and submit your pull requests !

The OCT module still needs many features at this point, here somme examples :

* Full python3 support (Experimental at the moment)
* Full celery integration for multi-processing
* More generic tests in core module
* More fancy templates
* etc...

Basics module information
=========================

OCT is based on multi-mechanize, a library for testing website. But this module is no longer under active development.

So instead of a fork, for building OCT module we include multi-mechanize as a module, and we update it as needed. For the moment
modifications are minors and the main job of OCT module is inside the core submodule, which contains a `GenericTransaction` class
 providing you useful methods for writing your tests scripts.

We already have done some update on the multi-mechanize modules like :

* update render of graphics
* update command for new projects
* more information in config file
* customisable templates
* replace matplotlib by pygal for graphics

But other improvements are on the way ! So stay tune on github !


How to
======

For each functionality, we have tried to write a how to. In that way you should be able to do everything you need with this library,
even customize it and add features !

See the :doc:`exemples`
project page

Installation
============

You'll need some linux packages for the installation, To install the required packages on Linux systems,
use your distribution specific installation tool, e.g. apt-get on Debian/Ubuntu:

.. code-block:: bash

   sudo apt-get install libxml2-dev libxslt-dev python-dev


You can install the OCT module with :

.. code-block:: python

   python setup.py install

Or with pip :

.. code-block:: python

   pip install oct


Contents
========

* :doc:`config`
* :doc:`scripts`
* :doc:`browser`
* :doc:`oct.core`
* :doc:`oct.multimechanize`
* :doc:`oct.testing`
* :doc:`oct.tools`
* :doc:`oct.utilities`

Indices and tables
==================

.. toctree::

   config
   scripts
   browser
   oct.core
   oct.multimechanize
   oct.testing
   oct.tools
   oct.utilities


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

