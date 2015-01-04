Using the browser
=================

Basic usages
------------

The browser is actually a part of the `oct.core` module, and it's instantiate by the `GenericTransaction` class in its
 `__init__` method.
By the browser can be used as a stand-alone, and for advanced scripts it's good to know how to use it. So how to use it ?
First simply instantiate it like that :

.. code-block:: python

    from oct.core.browser import Browser

    br = Browser()

Browser object take two optional parameters :

    * `sessions` if you want to use custom session manager, by default set to `requests.Session()`
    * `base_url` for setting up you links when parsing, default to empty string

So wright now, what to do ? Well with simple usages, let's access some urls :

.. code-block:: python

    response = br.open_url('http://localhost/index.html')
    print(response.status_code)
    response = br.open_url('http://localhost/other_page.html')
    print(response.status_code)

This piece of code access two page, and for each print the `status_code` of the response object returned by
 the `open_url` method.

Since the return is simply the return of `requests.get` or `requests.post` method, you can access all properties of
a basic `requests.Response` object. But we add one thing to it, an `html` property, containing an
`lxml.html` object, representing the opened page.

The html property can be used for parsing or getting elements with the `lxml` syntax, since it's a standard object from
 `lxml.html` parsing.

For example you can access all forms object by using :

.. code-block:: python

    response.html.forms

Or even the xpath syntax !

And can you check the render of the page ? Of course, don't need other imports, we've implemented
 an `open_in_browser` static method, calling the `lxml.html.open_in_browser` method. You can use it like this :

.. code-block:: python

    response = br.open_url('http://localhost/index.html')
    br.open_in_browser(response)

This will open the page in your default system browser.

A last thing you need to know. Each time the `.html` property is filled, the browser make a call to the
`make_links_absolute` method of `lxml`. If you want to avoid that, simply don't provide a `base_url` for your browser instance,
 it's used only for this call

Form manipulation
-----------------

Like we said in the previous part of this documentation, you can use all the `lxml` method for parsing your page. But again, we
did a part of the job for you.

Let's say that we have a simple html page like this at the index of your localhost favorite web server:

.. code-block:: html

    <!DOCTYPE html>
    <html>

    <head>
        <title> My test page </title>
    </head>

    <body>
        <div id="my_form_block">
            <form action="/action.py" method="post">
                <input type="text" name="firstname" />
            </form>
        </div>
    </body>

    </html>

A very simple page, but it's just for the example.

Now let's say that we want to get this form and submit it from the browser object. Simple a this :

.. code-block:: python

    from oct.core.browser import Browser

    # instantiate the browser
    br = Browser(base_url='http://localhost')

    # open the url
    br.open_url('http://localhost')

    # now we getting the form, using css selector
    br.get_form(selector='div#my_form_block > form')

    # we now have two properties for handling the form
    # br.form, containing the lxml for object
    # br.form_data, a dict containing all fields and values
    # let's just set the value and submit it
    br.form_data['firstname'] = 'my name'

    # and submit it
    response = br.submit_form()

    # and check the status code
    print(response.status_code)

And yes, that's it ! Simple, no ?
Thanks to the awesome cssselector python library, getting your forms are know simpler (unless you know nothing about css selectors)
but even if we don't want and can use it, we can still use the `get_form` method, and use the `nr` parameter.
The `nr` param simply represent the position of the form in our page. Here, simple we only have one form, so let's update our core :

.. code-block:: python

    from oct.core.browser import Browser

    # instantiate the browser
    br = Browser(base_url='http://localhost')

    # open the url
    br.open_url('http://localhost')

    # now we getting the form, using css selector
    br.get_form(nr=0)

    # we now have two properties for handling the form
    # br.form, containing the lxml for object
    # br.form_data, a dict containing all fields and values
    # let's just set the value and submit it
    br.form_data['firstname'] = 'my name'

    # and submit it
    response = br.submit_form()

    # and check the status code
    print(response.status_code)

And here it is, same result !

For more information about form manipulation, please see the `lxml`_. documentation

.. _lxml: http://lxml.de/lxmlhtml.html

More navigation
---------------

A little more human navigation ? what about follow links and go back ? Of course you can do that !

For example you can follow links inside the html page like this :

.. code-block:: python

    from oct.core.browser import Browser

    # instantiate the browser
    br = Browser(base_url='http://localhost')

    # open the url
    br.open_url('http://localhost')

    # now we can follow any link using css selector or a regex
    # the regex will look at the text or the href attribute of the link
    response = br.follow_link('a.my_links', '.*this link.*')

    # oooops wrong link ! (yeah i know, that's doesn't append in script by try to imagine)
    # let's go back
    response = br.back() # after this we will be again at the index page

And that's it ! The `follow_link` method is pretty simple actually, it's just find a link by regex and / or css selector,
and then open the url contained in the `href` attribute of the link.

What about the history ? Well it's not a big deal, only a small history management, no next management for now. But it allow you to
go back and see all pages opened previously. What append actually when you go back ? It open the previous url in the history list
property, and then delete the next page of it. So yeah, i know, pretty bad for now we can only go back. But stay tuned, better history
management is coming !