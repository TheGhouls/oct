Your first project
==================

Once OCT is installed on your system you will have access to several command-line tools
to help you using it, write your test or run your project.

First we gonna use the ``oct-newproject`` command for creating our first project.

.. code-block:: sh

    oct-newproject my_project_name

This command will create a folder named ``my_project_name`` containing all the required
files for you to start an OCT project.

Let's take a look at the content of this new folder :

.. code-block:: sh

    |── config.json
    ├── templates
    │   ├── css
    │   │   └── style.css
    │   ├── img
    │   ├── report.html
    │   └── scripts
    └── test_scripts
        └── v_user.py

Those files are the minium required by an OCT project. We will see them in details in this documentation but let's take
it file by file.

Configuration
-------------

The main and more important file here is the `config.json` file, let's take a look at his default content :

.. code-block:: json

    {
        "run_time": 30,
        "results_ts_interval": 10,
        "progress_bar": true,
        "console_logging": false,
        "testing": false,
        "publish_port": 5000,
        "rc_port": 5001,
        "min_turrets": 1,
        "turrets": [
            {"name": "navigation", "canons": 2, "rampup": 0, "script": "test_scripts/v_user.py"},
            {"name": "random", "canons": 2, "rampup": 0, "script": "test_scripts/v_user.py"}
        ],
        "turrets_requirements": []
    }

Each key here is important, but some keys are not required to run a test. Let's take a look to the most importants ones :

* ``run_time``: This key simply set the time of a test in second. So in this case the test will run for 30 seconds.

* ``results_ts_interval``: Time interval between two sets of results in seconds. For exemple if we have a run time of 30 seconds and an interval of 10, we will have 3 results sets in the final report

* ``testing``: If this key is set to True, the `results.sqlite` file will be created in `/tmp` folder

* ``publish_port``: The port for the publishing socket of the HQ

* ``rc_port``: The port for the result collector (PULL socket) of the HQ

* ``min_turrets``: The minimum number of turrets to wait before sending start message

* ``turrets``: a list of turrets, this key will be use to package turrets with the `oct-pack-turrets` command

* ``turrets_requirements``: A list of string containing the required packages for turrets (Only for python turrets at this time)

This configuration if simple but will allow you to run simple test in local.


Now let's take a look at the per-turret configuration :

Each turret can be configured independently, and you can setup different options for each one :

* ``name``: the string representation for the turret

* ``canons``: The number of canons for this turret (aka virtual users)

* ``rampup``: The rampup for the turret. The rampup option will tell to the turret at how many seconds all canons must be spawned

* ``script``: The relative path to the associated test script

Writing tests
-------------

By default, the ``oct-new-project`` command will create an exemple test script under ``test_scripts/v_user.py``, let's take a look at it :

.. code-block:: python

    from oct_turrets.base import BaseTransaction
    import random
    import time


    class Transaction(BaseTransaction):
        def __init__(self):
            pass

        def run(self):
            r = random.uniform(1, 2)
            time.sleep(r)
            self.custom_timers['Example_Timer'] = r

.. note ::

    As you can see the default test is writen in python, but each turret can have its own implementation and its own way to write
    tests. Refer to turrets documentation for more explainations on how to write tests with the selected turret.

So this file represent a basic test that will simply wait between 1 or 2 seconds. Not really usefull but it give you an exemple on how to write tests and
we will keep this example for running our tests in the local setup. For advanced explanations on how to write tests, please see :doc:`writing_tests`


That's all you need
-------------------

And that's all you need ! Yup that's right, some configuration and basics tests and that's it.

Off course this will not test your infrastructure or website, but at this point you should better undersand how OCT work and what you need to run your tests !
In the next part we will talk about writing more complexe tests
