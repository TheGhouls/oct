Your first project
==================

OCT exposes several command-line tools to use it, write your tests or run your project.

First we're going to use the ``oct new-project`` command for creating our first project.

.. code-block:: sh

    oct new-project my_project_name

This command creates a folder named ``my_project_name`` containing all the required
files to start an OCT project.

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

Those files are the minimum required by an OCT project. We will analyze them in details in this documentation but let's take
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
            {"name": "navigation", "cannons": 2, "rampup": 0, "script": "test_scripts/v_user.py"},
            {"name": "random", "cannons": 2, "rampup": 0, "script": "test_scripts/v_user.py"},
            {
                "name": "advanced-turret",
                "cannons": 2,
                "rampup": 0,
                "script": "test_scripts/v_user.py",
                "specific_turret_config": "my_value", // this config value will be present only in this turret config
                "extra_files": [
                    "templates"
                    // allow you to pack files and folder in turrets
                ]
            }
        ],
        "turrets_requirements": [],
        "extra_turret_config": {
            // put global turrets config key / values here
        }
    }

Every key here is useful, but some keys are not required to run a test. Let's take a look at the main ones :

* ``run_time``: This key simply sets the time of a test in seconds. So in this case the test will run for 30 seconds.

* ``results_ts_interval``: Time interval between two sets of results in
  seconds. For exemple if we have a run time of 30 seconds and an interval of
  10, we will have 3 results sets in the final report

* ``testing``: If this key is set to True, the `results.sqlite` file will be created in `/tmp` folder

* ``publish_port``: The port for the publishing socket of the HQ

* ``rc_port``: The port for the result collector (PULL socket) of the HQ

* ``min_turrets``: The minimum number of turrets that must be deployed before the HQ sends the start message

* ``turrets``: a list of turrets, this key will be use to package turrets with the `oct pack-turrets` command

* ``turrets_requirements``: A list of string containing the required packages for turrets (only for python turrets at this time)

* ``extra_turret_config``: A nested object containing all extra turrets parameters. Each value in it will be set in each turret configuration

This configuration is simple but will allow you to run simple tests in a local environment.


Now let's take a look at the per-turret configuration :

Each turret can be configured independently, and you can setup different options for each one :

* ``name``: the string representation for the turret

* ``cannons``: The number of cannons for this turret (aka virtual users)

* ``rampup``: Turrets can spawn their cannon progressively, not each at the same time. Rampup gives a "step" for
  cannon initialization. The number of cannon spawned by second is equal to the total number of cannons of the
  turret by rampup - e.g., if you have 30 cannons and a rampup of 15 seconds, it will spawn 2 cannons by seconds.
  If you do not want to increase the number of cannons in time but start the tests with all cannons ready to fire,
  leave rampup at 0, as in the exemple.

* ``script``: The relative path to the associated test script

* ``extra_files``: put here every file or folder that you want to ship with the turret

Any additional configuration key will be set as is in turret own configuration

Writing tests
-------------

By default, the ``oct new-project`` command will create an exemple test script under ``test_scripts/v_user.py``, let's take a look at it :

.. code-block:: python

    from oct_turrets.base import BaseTransaction
    from oct_turrets.tools import CustomTimer
    import random
    import time


    class Transaction(BaseTransaction):
        def __init__(self, config):
            super(Transaction, self).__init__(config)

        def setup(self):
            """Setup data or objects here
            """
            pass

        def run(self):
            r = random.uniform(1, 2)
            time.sleep(r)
            with CustomTimer(self, 'a timer'):
                time.sleep(r)

        def tear_down(self):
            """Clear cache or reset objects, etc. Anything that must be done after
            the run method and before its next execution
            """
            pass


    if __name__ == '__main__':
        trans = Transaction(None)
        trans.run()
        print(trans.custom_timers)

.. note ::

    As you can see the default test is writen in python, but each turret can have its own implementation and its own way to write
    tests. Refer to turrets documentation for more explanations on how to write tests with the selected turret.

So this file represent a basic test that will simply wait between 1 or 2 seconds. Not really useful but it give you an exemple on how to write tests and
we will keep this example when running our tests in the local setup. For advanced explanations on how to write tests, please see :doc:`writing_tests`


That's all you need
-------------------

And that's all you need ! Some configuration and basics tests and that's it.

Of course this will not be enough to test your infrastructure or website, but
at this point you should better undersand how OCT work and what you need to run
your tests !  In the next part we will talk about writing more complexe tests.
