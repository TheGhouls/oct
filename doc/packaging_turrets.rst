Packaging your turrets
======================

.. warning::

    This section will explain to you how to package turrets, but only based on the **python** turret. But many turrets will
    have similar implementation

So that's it ? You've written all your tests and you're ready to start to fire at your target ? Well let's prepare your turrets
for deployement !

Auto packaging
--------------

.. warning::

    This example only work for python based turrets. Please refer to your turret documentation if you use anything else

Oct provide a simple way to package your turrets and set them ready to fire, the ``oct-pack-turrets`` command.
It generate tar files based on your configuration file. Those tar files are the turrets, ready to fire at your command.

You can use it like this :

.. code-block:: bash

    oct-pack-turrets /path/to/oct/project

A sucessful packing should return the following output :

    Added config.json
    Added setup.py
    Added test_scripts/v_user.py
    Archive ./navigation.tar created
    =========================================
    Added config.json
    Added setup.py
    Added test_scripts/v_user.py
    Archive ./random.tar created
    =========================================

In addition if some optionnal keys of the configuration are not set, you could see something like that :

.. code-block:: bash

    WARNING: hq_address configuration key not present, the value will be set to default value

You will see a WARNING line per missing key.
Also if a required key is not set the command will throw an exception like that :

.. code-block:: bash

    oct.core.exceptions.OctConfigurationError: Error: the required configuration key <key> is not define

Where ``<key>`` is the missing key

Installing and starting the turrets
-----------------------------------

Now that your turrets are packaged, you call install them using pip for example :

.. code-block:: bash

    pip install navigation.tar

This command will install all required packages listed under the ``turrets_requirements`` configuration key, plus the
oct-turrets package itself.

Once the installation is done you can start your turret using the ``oct-turrets-start`` like that :

.. code-block:: bash

    oct-turrets-start --tar navigation.tar

And if everything is fine you should see this message :

.. code-block:: bash

    [2015-12-21 18:02:09,295: INFO | oct_turrets.turret] starting turret

You are now ready to fire the target !
