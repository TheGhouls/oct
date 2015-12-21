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



Selenium example
----------------
