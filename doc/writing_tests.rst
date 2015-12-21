Writing tests
=============

.. warning::

    This section will explain to you how to write tests, but only based on the **python** turret. But many turrets will
    have similar implementation

Basic example
-------------

Let's take the default ``v_user.py`` file :

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

So this basic script will basicaly test nothing, so let's test this basic use case :

We need to test a basic api over the internet and we want to use the ``requests`` python library.

So first let's adapt the script for it :

.. code-block:: python

    import time
    import requests
    from oct_turrets.base import BaseTransaction


    class Transaction(BaseTransaction):
        def __init__(self):
            # each canon will only instanciate Transaction once, so each property
            # in the Transaction __init__ method will be set only once so take care if you need to update it
            self.url = "http://my-api/1.0/"

        def run(self):
            # For more detailed results we will setup several custom timers
            start = time.time()
            requests.get(self.url + "echo")
            self.custom_timers['Echo service'] = time.time() - start

            start = time.time()
            requests.get(self.url + "other-service")
            self.custom_timers['other-service'] = time.time() - start

So what are we doing here ? We've just imported requests and use it in our script. For each service we've defined a custom
timer to see how much time each one will take to answer.

But how to install dependencies needed by the turrets ? You can simply update your configuration with something like that :

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
        "turrets_requirements": [
            "requests"
        ]
    }

If you specify the dependecies in the "turrets_requirements" you will be able to install all of it for each turret by simply runing :

.. code-block:: bash

    pip install my_turret_package.tar

Setup and Tear down
-------------------

The previous example still pretty simple, but you can need for example sessions or cookies. But how to manage it knowing that the
transaction class will be instanciate only once ?

Pretty simple too, we give you two methods in the ``BaseTransaction`` class to help you : ``setup`` and ``tear_down``

How does it works ? Take a look a this example :

.. code-block:: python

    import time
    import requests
    from oct_turrets.base import BaseTransaction


    class Transaction(BaseTransaction):
        def __init__(self):
            # each canon will only instanciate Transaction once, so each property
            # in the Transaction __init__ method will be set only once so take care if you need to update it
            self.url = "http://my-api/1.0/"
            self.session = None

        def setup(self):
            self.session = requests.Session()

        def run(self):
            # For more detailed results we will setup several custom timers
            start = time.time()
            self.session.get(self.url + "echo")
            self.custom_timers['Echo service'] = time.time() - start

            start = time.time()
            self.session.get(self.url + "other-service")
            self.custom_timers['other-service'] = time.time() - start

        def tear_down(self):
            self.session.close()

And that's it ! Before each ``run`` iteration, the setup method will be call, and you guess it, after iteration the ``tear_down`` is call.

.. note::

    The setup and the tear_down method are not included in the stats sent to the HQ, so the actions will not be included
    in the ``scriptrun_time`` statistic
