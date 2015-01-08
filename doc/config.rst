Configuration
=============

This section explain all the configurations available for a project

Basic configuration
-------------------

The default configuration file look like this

.. code-block:: cfg

    [global]
    run_time = 30
    rampup = 0
    results_ts_interval = 10
    progress_bar = on
    console_logging = off
    base_url = http://localhost
    default_sleep_time = 2


    [user_group-1]
    threads = 3
    script = v_user.py

    [user_group-2]
    threads = 3
    script = v_user.py

Global section
--------------

Runtime
~~~~~~~

.. code-block:: cfg

    run_time = 30

The time in second for running the project when calling the multimech-run command

Rampup
~~~~~~

.. code-block:: cfg

    rampup = 0

This variable represent the time in second before reaching the specified number of virtual users requested

Results interval
~~~~~~~~~~~~~~~~

.. code-block:: cfg

    results_ts_interval = 10

The interval between results in seconds


Progress bar
~~~~~~~~~~~~

.. code-block:: cfg

    progress_bar = on

Set if the progress bar should be shown while running the tests


Logging
~~~~~~~

.. code-block:: cfg

    console_logging = off

Set the logging display inside the terminal while running the tests

Base url
~~~~~~~~

.. code-block:: cfg

    base_url = http://localhost

The base url for the tests. This url will be used by the `open_url` method

Sleep time
~~~~~~~~~~

.. code-block:: cfg

    default_sleep_time = 2

The default sleep time in second, used will calling the `user_sleep` method

User group sections
-------------------

This section defines the virtual groups for testing

Threads
~~~~~~~

.. code-block:: cfg

    threads = 3

Define the number of users simulated in this group

Custom configuration variables
------------------------------

In some projects, you may need to have some custom configuration, well that's possible, just add the needed section in the config.cfg file.

Since the `GenericTransaction` class loads the configuration file by default, you can access all the sections and variables you need inside your script.

Let's take a basic configuration file for example :

.. code-block:: cfg

    [global]
    run_time = 30
    rampup = 0
    results_ts_interval = 10
    progress_bar = on
    console_logging = off
    base_url = http://localhost
    default_sleep_time = 2

    [user_group-1]
    threads = 3
    script = v_user.py

    [custom_section]
    custom = spam

Ok so now inside our test script we want to get the custom value, we just need to do this inside our run method :

.. code-block:: python


    def run(self):
        spam = self.config.get('custom_section', 'custom')
        print(spam)


    if __name__ == '__main__':
        trans = Transaction()
        trans.run()

If you run the script, it will display `spam`, since the custom variable value is `spam`