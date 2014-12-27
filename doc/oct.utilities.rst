oct.utilities package
=====================

This module provide you basics shell commands to easily use the OCT module.

newproject module
-----------------

This module provide you a command to create a new project directory. Once the library is installed you can use :

.. code-block:: python

    oct-newproject <project-name>


It will create a new directory named `project-name` with basic stuff inside.

The project structure must look like this :

.. code-block:: python

    .
    ├── config.cfg
    ├── templates
    │   ├── css
    │   │   └── style.css
    │   ├── footer.html
    │   ├── head.html
    │   ├── img
    │   └── scripts
    └── test_scripts
        └── v_user.py


With this basic project structure you can start writing your scripts, customize your templates, etc...

This project can be run with the command

.. code-block:: python

    multimech-run <project>

But for testing your scripts you can simply run them by using your standard python interpreter

The file `config.cfg` contain all configuration variable for your project. By default it's look like this

.. code-block:: cfg

    [global]
    run_time = 30
    rampup = 0
    results_ts_interval = 10
    progress_bar = on
    console_logging = off
    xml_report = off
    base_url = http://localhost
    default_sleep_time = 2
    statics_enabled = 1


    [user_group-1]
    threads = 3
    script = v_user.py

    [user_group-2]
    threads = 3
    script = v_user.py

For explanations :

This file give you two virtual user groups, each group has 3 user, and the user script is the `v_user.py` file.

To see all configuration variables explained see the :doc:`config` section


Module doc
----------

.. automodule:: oct.utilities.newproject
    :members:
    :undoc-members:
    :show-inheritance:

run module
----------

TODO

WORK IN PROGRESS

This module give you access to the command :

.. code-block:: python

    oct-run <project>

This command will run your project using celery. For now the broker can only be configured in source code. It's bind on
a standard rabbitmq server.

The goal of this command is to run the same project in several rabbitmq instance.


Module doc
----------

.. automodule:: oct.utilities.run
    :members:
    :undoc-members:
    :show-inheritance:



celery module
-------------

The configuration for running celery

.. automodule:: oct.utilities.celery
    :members:
    :undoc-members:
    :show-inheritance:

Module contents
---------------

.. automodule:: oct.utilities
    :members:
    :undoc-members:
    :show-inheritance:
