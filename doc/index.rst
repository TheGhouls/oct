.. oct documentation master file, created by
   sphinx-quickstart on Thu Dec 18 15:29:32 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to oct's documentation!
===============================

Oct stand for Open Charge Tester, the goal of this project is to give you the basics tools for write simple tests. The
tests are simple python scripts that make calls to web page or web service, submit data, login, etc...
OCT will give you basics tools for easily writing your test.

This documentation will provide you basics examples for writing tests, use oct-tools, lunch tests, get results or even customize the results to fit your needs

Note that the OCT project is in early development and is not suitable for productions tests actually.

If you want to contribute you're welcome ! Check the git, fork the project, and submit your pull requests !

The OCT module steel need many features at this point, here somme examples :

* Full python3 support
* New lib for replace Mechanize (based on html5lib ?)
* Full celery integration for multi-processing
* More generic tests in core module
* More fancy templates
* etc...

Basics module information
=========================

OCT is based on multi-mechanize, a library for testing website. But this module is no longer under active development
and the last commit was 3 years ago.

So instead of a fork, for building OCT module we include multi-mechanize as a module, and we update it. For the moment
modifications are minors and the main job of OCT module is inside the core submodules, which contains a `GenericTransaction` class
 which provide you useful methods for writing your tests scripts.

We already have done some update on the multi-mechanize modules like :

* update render of graphics
* update command for new projects
* more information in config file
* customisable templates

But other improvements are on the way ! So stay tune on github !


How to
======

For each functionality, we have tried to write a how to. In that way you should be able to do everything you need with this library,
even customize it and add features to it !

See the :doc:`exemples`
project page

Installation
============

You'll need some linux packages for the installation, To install the required development packages of these dependencies on Linux systems,
use your distribution specific installation tool, e.g. apt-get on Debian/Ubuntu:

.. code-block:: bash

   sudo apt-get install libxml2-dev libxslt-dev python-dev


You can install the module with :

.. code-block:: python

   python setup.py install

Or using pip :

.. code-block:: python

   pip install oct


NB : You may encounter build error with pip or easy_install, you


Contents
========

* :doc:`oct.core`
* :doc:`oct.multimechanize`
* :doc:`oct.testing`
* :doc:`oct.tools`
* :doc:`oct.utilities`

Indices and tables
==================

.. toctree::

   exemples
   oct
   oct.core
   oct.multimechanize
   oct.testing
   oct.tools
   oct.utilities


* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

