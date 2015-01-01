examples
========

Installing OCT
--------------

Creating a new project
----------------------

For starting a new project you have access to this command :

.. code-block:: bash

    oct-newproject <project_name>

This command will create a new project inside the current directory named with the `<project_name>` argument

The created directory must look like this :

.. code-block:: bash

    .
    ├── config.cfg
    ├── templates
    │   ├── css
    │   │   └── style.css
    │   ├── footer.html
    │   ├── head.html
    │   ├── img
    │   └── scripts
    └── test_scripts
        └── v_user.py



This folders contains the basic for running an OCT project.

Configuration
-------------

For configuration explanation and examples see the :doc:`config` page

Customizing your templates
--------------------------

You need an other render for the results ? the default template is ugly and you want to change it ? It's ok, we have done
some things for help you to do that.

If you have created your project with the `oct-newproject` command, you have a templates directory inside your project.
This directory is used for writing the results, so each call to `multimech-run` command will read this files.
With this you can easily update the template and customize it to fit your needs. It's simple as that.

For the moment the templates can't be fully modified, but you steel have plenty of options to change them.

Let's take a look at the style.css file :

.. code-block:: css

    /* http://meyerweb.com/eric/tools/css/reset/
       v2.0 | 20110126
       License: none (public domain)
    */

    html, body, div, span, applet, object, iframe,
    h1, h2, h3, h4, h5, h6, p, blockquote, pre,
    a, abbr, acronym, address, big, cite, code,
    del, dfn, em, img, ins, kbd, q, s, samp,
    small, strike, strong, sub, sup, tt, var,
    b, u, i, center,
    dl, dt, dd, ol, ul, li,
    fieldset, form, label, legend,
    table, caption, tbody, tfoot, thead, tr, th, td,
    article, aside, canvas, details, embed,
    figure, figcaption, footer, header, hgroup,
    menu, nav, output, ruby, section, summary,
    time, mark, audio, video {
        margin: 0;
        padding: 0;
        border: 0;
        font-size: 100%;
        font: inherit;
        vertical-align: baseline;
    }
    /* HTML5 display-role reset for older browsers */
    article, aside, details, figcaption, figure,
    footer, header, hgroup, menu, nav, section {
        display: block;
    }
    body {
        line-height: 1;
    }
    ol, ul {
        list-style: none;
    }
    blockquote, q {
        quotes: none;
    }
    blockquote:before, blockquote:after,
    q:before, q:after {
        content: '';
        content: none;
    }
    table {
        border-collapse: collapse;
        border-spacing: 0;
    }

    body {
        background-color: #f4f4f4;
        font-family: "Helvetica Neue", Helvetica, Roboto, Arial, sans-serif;
    }

    h1	{
        font-size: 4em;
        background: #2b2b2b;
        color: white;
        font-weight: bold;
    }

    h2 {
        font-size: 2em;
        background: #f78930;
        margin: 15px 0 15px 0;
    }

    h1, h2, h3, h4, h5, h6 {
        padding: 15px;
    }

    h4 {
        font-weight: bold;
        font-size: 1.3em;
    }

    h3 {
        font-size: 1.5em;
        font-weight: bold;
    }

    .summary {
        padding-left: 15px;
    }

    .summary > b {
        font-weight: bold;
    }

    #main table {
        margin-left: 15px;
        border: 1px solid grey;
    }

    #main th {
        font-weight: bold;
        padding: 10px 0 10px 0;
        border: 1px solid grey;
    }

    #main tr {
        padding: 10px 0 10px 0;
        text-align: center;
    }

    #main td {
        min-width: 70px;
        padding: 10px 5px 10px 5px;
        border: 1px solid grey;
    }

    hr {
        color: #f4f4f4;
        background-color: #f4f4f4;
        border: none;
    }

As you can see, all style present on the result page is here, so feel free to update it.
But you may need some other css files, like a css framework, or even javascript files ? why not after all ?

Well you can do that, you can include all the files you need for customize your results page.

How ? simply edit the `templates/head.html' and include your files, you can even create your own header, add messages at
the top of the page, etc...

A little explanation of how this work :

When you call the `multimech-run` command inside your project directory, the command will look for the templates directory and
read the `head.html` and the `footer.html` files, and will create a new html page with them.
At the same time the command will copy all files insides the `img`, `scripts`, and `css` directories. So everything added in this folders will
be in the associated result directory. In that way you can add all the stuff you want to your results, and not reworking each result after each test


Writing your first script
-------------------------

It's time to write our first script and test it, so first let's take a look at the generated v_user.py file :

.. code-block:: python

    from oct.core.generic import GenericTransaction
    import random
    import time
    import os


    CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')


    class Transaction(GenericTransaction):
    def __init__(self):
        GenericTransaction.__init__(self, True, CONFIG_PATH)

    def run(self):
        r = random.uniform(1, 2)
        time.sleep(r)
        self.custom_timers['Example_Timer'] = r


    if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print trans.custom_timers

So what does this script ? Since it's an example script, actually it just sleep for 1 or 2 seconds.

Let's update this script a little, but first don't forget to update the configuration file to fit your configuration.

Okay so let's write a simple script, just for accessing the index page of our web site and get the statics file of it

.. code-block:: python

    from oct.core.generic import GenericTransaction
    import time
    import os


    CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')


    class Transaction(GenericTransaction):
        def __init__(self):
            GenericTransaction.__init__(self, True, CONFIG_PATH)

        def run(self):
            test_time = time.time()

            resp = self.open_url('/')
            self.get_statics(resp, 'index_statics')

            self.custom_timers['test_time'] = time.time() - test_time


    if __name__ == '__main__':
        trans = Transaction()
        trans.run()
        print trans.custom_timers

So that's it, we just open the index url of the website (based on the base_url configuration variable), get the response
object returned by the `open_url` method and pass it to the `get_statics` method.

So what does this test do ? well it accesses to the index page and retrieve all css, javascript and img files in it. Simple as this

Testing your script
-------------------

So what's next ? Now you got your basic script retrieving your index page and associated statics files. But does it works ?

Let's figure it out. To test your script 1 time, just to make sure all code work, you actually call the script with your python interpreter like this :

.. code-block:: bash

    python my_script.py

With the previous script, if everything is ok, you must see the timer on the standard output.

Everything work find ? Nice, let's now run our tests with lot of users, so update your configuration file and then you just have to run :

.. code-block:: bash

    multimech-run <myproject>

Or if you're already inside the path of you're project, simply run :

.. code-block:: bash

    multimech-run .

You must see the progress bar appears, you now just have to wait till the tests end. This action will create a results directory inside your project folder,
and a sub-directory containing the results in csv or html format.

Handle forms
------------



Handle multiples url
--------------------

Creating different virtual users
--------------------------------

Updating the configuration of your project
------------------------------------------

