Writing your own turret
=======================

You use OCT but the python turret doesn't fit your needs ? Or you need a library avaible only in one
language ? Or maybe you just want to create a turret with your favorite programing language ? No problem, this guide is here
for you !

.. note::
    You can base your turret on the python turret, source code avaible `here`_

.. _here: https://github.com/karec/oct-turrets

Global workflow
---------------

OCT uses zeromq for communication between the HQ and the turrets. That means that you can write a turret in any language
with a zeromq binding (`zeromq bindings`_)

.. _zeromq bindings: http://zeromq.org/bindings:_start

But before writing your code, you need to understand how turrets must communicate with the HQ. Here is a schema to explain it :

.. image:: images/oct-turrets.png

So as you can see this is pretty simple, the HQ send orders to the turrets using a PUB/SUB pattern, and the turrets will send
results to the master using a PUSH/PULL pattern.

.. note::
    The python turret also uses a push/pull pattern to enable communication between cannons and the turret itself. All cannons
    have an inproc socket connected to the turret process

Requirements
------------

Before going any further, you need to know what a turret must be able to do :

* Reading a turret configuration file (see below)
* Spawning N number of cannons (set in the configuration file)
* Managing rampup
* Importing test files and run it
* Sending well formated json messages to the HQ

The turret configuration
------------------------

As you can see in the python-turret example (in the GitHub repository), a turret must be able to read and understand this
type of configuration file :

.. code-block:: json

    {
        "name": "navigation",
        "cannons": 50,
        "rampup": 10,
        "script": "v_user.py",
        "hq_address": "127.0.0.1",
        "hq_publisher": 5000,
        "hq_rc": 5001
    }

The configuration is pretty simple - and yes this is the full configuration needed for a turret to run.

Let's explain all keys :

* ``name``: the display name of the turret for the report
* ``cannons``: the number of cannons to spawn (remember, cannons == virtual users)
* ``rampup``: the rampup value in seconds
* ``script``: the path/name of the test script to load
* ``hq_address``: the IP address of the HQ
* ``hq_publisher``: the port of the PUB socket of the HQ
* ``hq_rc``: the port of the PULL socket of the HQ

All keys are required.

Sockets configuration
---------------------

To communicate with the headquarters, you will need only two zmq sockets :

* A sub socket listening on the general, empty string '' channel and on '<turret_uniq_id>' channel (for direct orders)
* A push socket to send results to the master

For example, in the python turret the sockets are created this way :

.. code-block:: python

    self.context = zmq.Context()

    self.master_publisher = self.context.socket(zmq.SUB)
    self.master_publisher.connect("tcp://{}:{}".format(self.config['hq_address'], self.config['hq_publisher']))
    self.master_publisher.setsockopt_string(zmq.SUBSCRIBE, '')
    self.master_publisher.setsockopt_string(zmq.SUBSCRIBE, self.uuid)

    self.result_collector = self.context.socket(zmq.PUSH)
    self.result_collector.connect("tcp://{}:{}".format(self.config['hq_address'], self.config['hq_rc']))

You need to listen to the ``master_publisher`` socket to retrieve commands from the master. These commands can be :

* ``start``: tells the turret to start the tests
* ``status_request``: headquarters ask for the status of the turret (RUNNING, WAITING, etc.)
* ``kill``: tells the turret to shutdown
* ``stop``: tells the turret to stop tests and clean everything to be in ready status again

HQ commands format
------------------

The HQ will send commands in JSON format. All command messages will contain 2 keys : ``command`` and ``msg``.

For example :

.. code-block:: json

    {
        "command": "stop",
        "msg": "premature stop"
    }

Tell the HQ that your turret is ready to fire
---------------------------------------------

The master need to know if your turret is ready or not. Why ? Because the HQ can be set up to wait for ``n`` number
of turrets before starting the tests.

But don't worry, it's pretty simple to tell the master that your turret is ready, you only need to send a json message with the
``PUSH`` socket of your turret.

The status message SHOULD contain all of the following fields:

* ``turret``: the name of the turret (eg: navigation, connection, etc.)
* ``status``: the current status of the turret (ready, waiting, running, etc.)
* ``uuid``: the unique identifier of the turret
* ``rampup``: the rampup setting of the turret
* ``script``: the test script associated with the turret
* ``cannons``: the number of cannons on the turret

A complete json status message will look like this:

.. code-block:: json

    {
        "turret": "navigation",
        "status": "READY",
        "uuid": "d7b8a1cc-639a-405c-9b16-62ce5cd66f36",
        'rampup': "30",
        'script': "tests/navigation.py",
        'cannons': "250"
    }

.. note::

    The status messages are not fixed, since it will only be used in the final html report for displaying the latest known status of each turret. But it's important to update it, since a crashing turret will obviously impact final results


Results messages format
-----------------------

All results messages that will be sent to the HQ should have the same pattern. Note that if the HQ receive a badly formatted
message, it will fail silently and you will lose those data.

But don't worry, once again the pattern of the message is pretty simple :

.. code-block:: json

    {
        "turret_name": "my_turret"
        "elapsed": 12.48, // total elapsed time in seconds
        "epoch": 1453731738 // timestamp
        "scriptrun_time": 1.2, // the time it took to execute the current transaction (aka the response time)
        "error": "My custom error", // the error string. Empty if there are no errors
        "custom_timers": {
            "Example_timer": 0.6, // An example custom timer
            "Other timer": 0.8
        }
    }

See ? Pretty simple, isn't it ?

This message will be sent throught the ``push`` socket of the turret and will be received by the ``pull`` socket of the master.

.. warning::
    The master use the ``recv_json()`` method to retreive messages comming from the turret, so take care to sent message using the appropriate ``send_json()`` method


Error management
----------------

The way turrets must manage errors is pretty simple :

* If the error is inside the test scripts, the turret should keep running
* If the error happens at the turret level, the turret should send a notification to the master before dying

So, what happens when an error is thrown inside the test script ? Simple, your turret should log it and send it to the master
in the ``error`` key of the reponse message.
This way, the user could be informed if something went wrong, but the test will continue to run.

And now, if the error appears at the turret level, how to tell the HQ that your turret is dead ? Pretty simple again,
a simple status message with the new status of your turret :

.. code-block:: json

    {
        "turret": "navigation",
        "status": "Aborted",
        "uuid": "d7b8a1cc-639a-405c-9b16-62ce5cd66f36",
        'rampup': "30",
        'script': "tests/navigation.py",
        'cannons': "250"
    }

If you sent this message, in the final html report the user will be able to see that one turret is dead and at
what moment the turret as stopped

Writing your own packaging system
---------------------------------

For this you're pretty free to implement it the way you want / need it. But don't forget that the goal of the packaging system
is to provide simple way to distribute turret in one command line.

Don't forget to document the way your user can packages their turrets and how they can run it !

Plus, the packaging avaible in the core of OCT will be rewritten to be more generic as soon as possible.

Document your turret
--------------------

Simply put: please, document your turret !

We expect to create a list to reference all available turrets, and if your turrets doesn't have a documentation, we will refuse
to list it.

But keep in mind that for many case, a simple README is enough. At the very least, tell your users how to install and start your turret.
