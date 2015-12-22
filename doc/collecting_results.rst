Collecting the results
======================

The tests has ended and the report has been created ? Let's take a look at it !

Results.html file
-----------------

This is the main and the more explicit part of the results, it will give you all major informations about the tests, plus
some graphs to help you for reading the results.

A default result page look like this :

.. image:: images/oct-results.png
    :scale: 50%

For each custom timer, a section will be created (like All transactions section) and the associated graphs will be created.

At the moment the graphs are in SVG format and use javascript for simpler interpretation and reading.

Regenerate results
------------------

Sometimes you may need to regenerate the html report with all graphs from an sqlite file. OCT got a tool to allow you to
do this.

You can simply use the ``oct-rebuild-results`` like this for example:

.. code-block:: bash

    oct-rebuild-results . results.sqlite config.json

.. note::

    The oct-rebuild-results command will only work on an already created results folder that contain only the sqlite results
    and optionnaly the configuration.
