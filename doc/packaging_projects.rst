Packaging your project as template
==================================

Since version 0.4.2, you can start a new project with an existing template.
It allow you to reuse or share your OCT projects for specific cases


Packaging your project
----------------------

Since OCT wait for a tar archive as template, you can simply package your project like this :


.. code-block:: bash

    $ cd my_project
    $ tar -zcvf my_template_name.tar.gz *

To be used as a template, your project directory structure should look like this :


.. code-block:: bash

    ├── config.json  # config file is mandatory
    ├── README.md
    ├── templates  # templates directory is mandatory
    │   ├── css
    │   │   └── style.css
    │   ├── img
    │   ├── report.html  # html report template is mandatory
    │   └── scripts
    │       └── pygal-tooltip.min.js
    └── test_scripts
        ├── test_script_1.py
        └── test_script_2.py


.. note::
    You can add as many files and directories as you need in your archive, they will be extracted


Using your template
-------------------

OCT provide an option to ``new-project`` command to use a template :

.. code-block:: bash

    oct new-project project_name --template path/to/template.tar.gz

This command will create a new directory with the content of your template
