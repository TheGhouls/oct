oct.tools package
=================

oct.tools contain two functions. One who can be called directly in the shell

.. code-block:: python

    octtools-user-generator

.. code-block:: python

    email_generator_func

HOW TO:
=======

octtools-user-generator
-----------------------

is the command line to generate either user or email WITH their password

occtools-user-generator must have a CSV file provided and have multiple optional arguments

.. code-block:: python

    MUST HAVE THIS ONE
        -h [CSV File]
    [[OPTIONAL]]
        -n [nb_item] Number of items generated
        -s [size] Size of each user/email/password generated
        -w [type u = user, e = email] What you want to generate

Default value of each options

.. code-block:: python

    -n => 250 items
    -s => item with lenght of 6
    -w => e (generate email by default)

Exemple
-------

.. code-block:: python

    octtools-user-generator userfile.csv -n 25000 -s 6 -w u

This command line will generate 25000 email/password with a lenght of 6 in "userfile.csv"

email_generator_func()
----------------------

Is a function with multiple agruments some have a default value


.. code-block:: python

    csvfile
    what = Define what you want to generate u = user, e = email.
    number = Define how many items you want to generate
    size = Define the size of each items
    chars = Define with 'what' you want to generate you item

Default value of each options


.. code-block:: python

    number = 15
    size = 6
    char = string.ascii_lowercase

Exemple
-------
.. code-block:: python

    email_generator_func("csvfile.csv", "u", 15000, 7):

This command line will generate 15000 user/password with a lenght of 7 in "csvfile.csv"


oct.tools.email_generator module
--------------------------------

.. automodule:: oct.tools.email_generator
    :members:
    :undoc-members:
    :show-inheritance:

oct.tools.xmltocsv module
-------------------------

.. automodule:: oct.tools.xmltocsv
    :members:
    :undoc-members:
    :show-inheritance:


Module contents
---------------

.. automodule:: oct.tools
    :members:
    :undoc-members:
    :show-inheritance:
