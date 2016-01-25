Writing your own turret
=======================

So that's it, you use OCT but the python turret doesn't fit your needs ? Or you need a library avaible only on one
language ? Or maybe you just want to create a turret with your favorite programing language ? No problem, this guide is here
for you !

.. note::
    You can base your turret on the python turret, source code avaible `here`_

.. _here: https://github.com/karec/oct-turrets

Global workflow
---------------

OCT use zeromq for communicate between the HQ and the turrets. That's mean that you can write a turret in any language
who have a zeromq binding (`zeromq bindings`_)

.. _zeromq bindings: http://zeromq.org/bindings:_start

But before starting to code, you need to understand how the turrets must communicate with the HQ. Here is a schema to explain it :

.. image:: images/oct-turrets.png

So as you can this is pretty simple, the HQ send orders to the turrets using a PUB/SUB pattern, and the turrets will send
results to the master using a PUSH/PULL pattern.

.. note::
    The python turret also use a push/pull pattern to enable communication between canons and the turret itself. All canons
    have an inproc socket connected to the turret process

Requirements
------------

Before going any further, you need to know what a turret must be able to do :

* Reading a turret configuration file (see below)
* Spawning N number of canons (set in the configuration file)
* Managing rampup
* Importing test files and run it
* Sending well formated json message to the HQ

The turret configuration
------------------------

Has you can see in the python-turret example (in the github repository), a turret must be able to read and understand this
type of configuration file :

.. code-block:: json

    {
        "name": "navigation",
        "canons": 50,
        "rampup": 10,
        "script": "v_user.py",
        "hq_address": "127.0.0.1",
        "hq_publisher": 5000,
        "hq_rc": 5001
    }

Has you can see the configuration is pretty simple and yes this is the full configuration need for a turret to run.

Let's explain all keys :

* ``name``: the display name of the turret for the report
* ``canons``: the number of canons to spawn(remember, canons == virtual users)
* ``rampup``: the rampup value in seconds
* ``script``: the path/name of the test script to load
* ``hq_address``: the ip address of the HQ
* ``hq_publisher``: the port of the PUB socket of the HQ
* ``hq_rc``: the port of the PULL socket of the HQ

Obviously you will need all this informations

Sockets configuration
---------------------

For communicate with the master, you will need only two zmq sockets :

* A sub socket listening on '' channel and on '<turret_uniq_id>' channel (for direct order)
* A push socket to send results to the master

For exemple, in the python turret the sockets are create this way :

.. code-block:: python

    self.context = zmq.Context()

    self.master_publisher = self.context.socket(zmq.SUB)
    self.master_publisher.connect("tcp://{}:{}".format(self.config['hq_address'], self.config['hq_publisher']))
    self.master_publisher.setsockopt_string(zmq.SUBSCRIBE, '')
    self.master_publisher.setsockopt_string(zmq.SUBSCRIBE, self.uuid)

    self.result_collector = self.context.socket(zmq.PUSH)
    self.result_collector.connect("tcp://{}:{}".format(self.config['hq_address'], self.config['hq_rc']))

You need to listen to the ``master_publisher`` socket to retreive commands from the master. This commands can be :

* ``start`` this command tell the turret to start the tests
* ``status_request`` the master ask for the status of the turret (RUNING, WAITING, etc.)
* ``kill`` tell the turret to shutdown
* ``stop`` tell the turret to stop tests and clean everything to be in ready stat again

HQ commands format
------------------

The HQ will send command in json format. All command message will contains 2 keys : ``command`` and ``msg``.

For example :

.. code-block:: json

    {
        "command": "stop",
        "msg": "premature stop"
    }

Tell the HQ that your turret is ready to fire
---------------------------------------------

The master need to know if your turret is ready or not. Why ? Because the HQ can be configured for waiting to ``n`` number
of turrets before starting tests.

But don't worry, it's pretty simple to tell the master that your turret is ready, you only need to send a json message with the
``PUSH`` socket of your turret.

The status message SHOULD contain all of the following fields :

* ``turret`` the name of the turret (eg: navigation, connection, etc.)
* ``status`` the current status of the turret (ready, waiting, running, etc.)
* ``uuid`` the unid id of the turret
* ``rampup`` the rampup setting of the turret
* ``script`` the test script associated with the turret
* ``canons`` the number of canons on the turret

A complete json status message will look like this :

.. code-block:: json

    {
        "turret": "navigation",
        "status": "READY",
        "uuid": "d7b8a1cc-639a-405c-9b16-62ce5cd66f36",
        'rampup': "30",
        'script': "tests/navigation.py",
        'canons': "250"
    }

.. note::

    The status messages are not fixed, since it will only be used in the final html report for displaying the latest known status of each turret. But it's important to update it, since if a turret crash it will obviously impact the results


Messages format
---------------



Error management
----------------

In case of turret destruction
-----------------------------

Writing your own packaging system
---------------------------------

Document your turret
--------------------
