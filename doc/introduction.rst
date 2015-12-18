Introduction
============

Terminology
-----------

* HQ for Headquarter. It's the "server" part of OCT and it will be in charge of sending start signal,
stop signal, collecting results and create reports
* Turret. A turret is the "client" part of OCT. It can be writen in any language and it communicate with the HQ using a
zeromq PUSH socket. Each turret own one or many canons.
* Canons represent the virtual users, wich means that each canon of the turret will run a test in parallel

.. note::
    Why do we use this terminology ? For the image. Think about it like that : Eeach turret own X canons who will shoot
    to the target. The turret will send report about the shoots to the HQ

What is OCT
-----------

OCT is an agnostic load testing tool. What do we mean by agnostic ? Simple : OCT provides only the needed tools
to distribute and simply run your tests and compile the results. But the tools and programming languages for writing tests are up to you.

At this stage of developpment we only offer a python turret, but if you want to create your own turret implementation
in any language, please do it ! We're realy open to any suggestions and help.

How it works ?
--------------

OCT use the power of ``zeromq`` to distribute test on any number of physical machines you need. When running a test
the principle is very simple :

* OCT start the HQ wich is in charge of collecting results and send a start message to the turrets
* The turrets catch the message, start the tests and send results to the HQ
* When the test end, the HQ will send a stop message to the turrets and process the remaining messages in queue
* OCT will next compile the results and create a html report of them

Want a graph ? Here you go :
