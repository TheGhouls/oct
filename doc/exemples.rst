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


Advanced configuration
----------------------


Writing your first script
-------------------------

Testing your script
-------------------


Handle forms
------------

Handle multiples url
--------------------

Creating different virtual users
--------------------------------

Updating the configuration of your project
------------------------------------------

