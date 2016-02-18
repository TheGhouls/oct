Running Tests
=============

So that's it ? Your turrets are running and ready to fire at the target ? Si let's do it ! Leeeeeeroooooy....

Configuration
-------------

Before running the tests, don't forget to update your configuration if your turrets are running on a different IP address from
the master.

Starting the test
-----------------

Just type:

.. code-block:: bash

    oct-run /path/to/oct/project

And that's it, your test will start and your turrets will now fire at the target. If everything is going ok you should see
an output like:

.. code-block:: bash

    Warmup
    waiting for 1 turrets to connect
    waiting for 0 turrets to connect
    turrets: 1, elapsed: 20.0   transactions: 4906  timers: 4906  errors: 0

So... That's it ?
And yes that's it ! You've successfuly run your first OCT test !

Once the test have ended you should see the following output :

.. code-block:: bash

    Processing all remaining messages...


    analyzing results...

    transactions: 4906
    errors: 0

    test start: 2015-12-21 18:23:06
    test finish: 2015-12-21 18:23:26

    Report generated in 2.75798082352 seconds
    created: ././results/results_2015.12.21_18.23.05_162132/results.html

    done.
