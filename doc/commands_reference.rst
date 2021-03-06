Commands reference
==================

Global
------

Since the 0.4.0 version, OCT only provide one entry points for all commands.
To see all avaibles sub-commands type:

.. code-block:: sh

    oct -h

You should see :

.. code-block:: sh

    usage: oct [-h]

           {to-csv,rebuild,pack,rebuild-results,new,results-to-csv,run,new-project,pack-turrets}
           ...

    positional arguments:
      {to-csv,rebuild,pack,rebuild-results,new,results-to-csv,run,new-project,pack-turrets}
                            sub commands avaibles
        new-project (new)   create a new oct project
        pack-turrets (pack)
                            create turrets packages from a given oct project
        run                 run an oct project
        rebuild-results (rebuild)
                            Rebuild the html report from result dir
        results-to-csv (to-csv)
                            Create a csv file from a sqlite results file

    optional arguments:
      -h, --help            show this help message and exit

Each sub command has its own help

New project
-----------

Create a new OCT project

aliases :

* new-project
* new

usage :

.. code-block:: sh

    oct new-project [-h] [-t TEMPLATE] <project_path>

Arguments :

=============== ====  ========== ==================================
name            type  mandatory  description
=============== ====  ========== ==================================
project         str   yes        path of the new project
-t, --template  str   no         path of existing project template
=============== ====  ========== ==================================


Pack turrets
------------

Create all turrets package from config file

aliases :

* pack-turrets
* pack

usage :

.. code-block:: sh

    oct pack-turrets <path-to-project>

Arguments :

======== ====  ========== =======================
name     type  mandatory  description
======== ====  ========== =======================
path     str   yes        path of the project
======== ====  ========== =======================


Run
---

Run an OCT project

aliases :

* run

usage :

.. code-block:: sh

    oct run <path-to-project>

Arguments :

======================= ====  ========== =================================================
name                    type  mandatory  description
======================= ====  ========== =================================================
project                 str   yes        path of the project
-r, --results           str   no         specifiy a custom directory for the results
-d, --directyory        str   no         specify the project directory if not current
-p, --publisher-channel str   no         specify a custom channel for results publication
======================= ====  ========== =================================================

Rebuild results
---------------

Rebuild html results and graph from existing sqlite result file

aliases :

* rebuild-results
* rebuild

usage :

.. code-block:: sh

    oct rebuild-results <path-to-results> <path-to-config> [-f] <path-to-sqlite-results>

Arguments :

================== ====  ========== =============================================
name               type  mandatory  description
================== ====  ========== =============================================
results_dir        str   yes        results directory to rebuild
config_file        str   yes        json config file of the project
-f, --results-file str   no         sqlite results file
================== ====  ========== =============================================

Results to csv
---------------

Convert sqlite results to csv

aliases :

* results-to-csv
* to-csv

usage :

.. code-block:: sh

    oct results-to-csv [-h] [-d DELIMITER] <result_file> <output_file>

Arguments :

================ ====  ========== =============================================
name             type  mandatory  description
================ ====  ========== =============================================
results_file     str   yes        sqlite result file to use
output_file      str   yes        csv output file
-d, --delimiter  str   no         specify custom delimiter for csv file
================ ====  ========== =============================================
