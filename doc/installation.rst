Installation
============

OCT-Core
--------

OCT is avaible on pypi so you can install it with pip :

.. code-block:: bash

    pip install oct

Or directly from the source :

.. code-block:: bash

    python setup.py install

You will also need the python headers for installing some of the dependencies like
numpy, but you will also need ``build-essential`` and ``python-dev`` to compile them

On a debian based system you can install them using apt for example :

.. code-block:: bash

    apt-get install python-dev build-essential


.. note::
    The OCT core part have been developed and tested on linux based system only,
    at this point of the developement process we cannot guarantee you that the oct-core
    can be installed on a windows system

OCT-Turrets
-----------

You can actually choose any turret that you need, in any langage. By default the ``oct`` package require
the python turrets for installation and it will be automaticaly installed with the main ``oct`` package
