Writing tests
=============

.. warning::

    This section will explain how to write tests, but only based on the **python** turret. But many turrets will
    have similar implementation

Basic example
-------------

Let's take the default ``v_user.py`` file :

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

This raw script will test nothing as it is, so let's work on this simple use case:

We need to test a basic API over the Internet and we want to use the ``requests`` python library.

So first let's adapt the script to our needs:

.. code-block:: python

    import time
    import requests
    from oct_turrets.base import BaseTransaction


    class Transaction(BaseTransaction):
        def __init__(self, config):
            super(Transaction, self).__init__(config)
            # each cannon will only instanciate Transaction once, so each property
            # in the Transaction __init__ method will be set only once so take care if you need to update it
            self.url = "http://my-api/1.0/"

        def run(self):
            # For more detailed results we will setup several custom timers
            with CustomTimer(self, 'Echo service'):
                requests.get(self.url + "echo")

            with CustomTimer(self, 'other-service'):
                requests.get(self.url + "other-service")

So what are we doing here ? We've just imported requests and used it in our script. For each service we've defined a custom
timer to see how much time each one will take to answer.

But how to install the dependencies needed by the turrets ? You can simply update your configuration with something like that :

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
            {"name": "random", "cannons": 2, "rampup": 0, "script": "test_scripts/v_user.py"}
        ],
        "turrets_requirements": [
            "requests"
        ]
    }

If you specify the dependecies in the "turrets_requirements" you will be able to install them for each turret by simply runing :

.. code-block:: bash

    pip install my_turret_package.tar

Setup and Tear down
-------------------

The previous example is still pretty simple, but you might need things like sessions or cookies. How to manage it knowing that the
transaction class will instantiate only once ?

Pretty simple too: we give you two methods in the ``BaseTransaction`` class to help you : ``setup`` and ``tear_down``

How does it works ? Take a look a this example:

.. code-block:: python

    import time
    import requests
    from oct_turrets.base import BaseTransaction


    class Transaction(BaseTransaction):
        def __init__(self, config):
            super(Transaction, self).__init__(config)
            # each cannon will only instanciate Transaction once, so each property
            # in the Transaction __init__ method will be set only once so take care if you need to update it
            self.url = "http://my-api/1.0/"
            self.session = None

        def setup(self):
            self.session = requests.Session()

        def run(self):
            # For more detailed results we will setup several custom timers
            with CustomTimer(self, 'Echo service'):
                self.session.get(self.url + "echo")

            with CustomTimer(self, 'other-service'):
                self.session.get(self.url + "other-service")

        def tear_down(self):
            self.session.close()

And that's it ! Before each ``run`` iteration, the ``setup`` method is called, and you've guessed it, ``tear_down`` is called after the iteration.

.. note::

    The setup and the tear_down method are not included in the stats sent to the HQ, so the actions will not be included
    in the ``scriptrun_time`` statistic
