import requests
import re
import lxml.html as lh
from lxml.cssselect import CSSSelector
from oct.core.exceptions import FormNotFoundException, NoUrlOpen, LinkNotFound, NoFormWaiting


class Browser(object):
    """
    This class represent a minimal browser. Build on top of lxml awesome library it let you write script for accessing
    or testing website with python scripts

    :param session: The session object to use. If set to None will use requests.Session
    :param base_url: The base url for the website, will append it for every link without a full url
    """
    def __init__(self, session=None, base_url=''):
        self._sess_bak = session
        self._history = []
        self._html = None
        self._url = None
        self._back_index = False
        self._base_url = base_url
        self._headers = {}
        self.form = None
        self.form_data = None
        self.session = session or requests.Session()

    def add_header(self, name, value):
        """
        Allow you to add custom header, one by one.
        Specify existing name for update
        Headers will be used by every request

        :param name: the key of the header
        :type name: str
        :param value: the associated value
        :type value: str
        :return: None
        """
        self._headers[name] = value

    def del_header(self, key):
        """
        Try to delete the 'key' of headers property

        :param key: the key to delete
        :type key: mixed
        :return: None
        """
        self._headers.pop(key, None)

    def set_headers(self, headers):
        """
        Setter for headers property

        :param headers: a dict containing all headers
        :type headers: dict
        :return: None
        """
        self._headers = headers

    def clean_session(self):
        """
        This function is called by the core of multi-mechanize. It cleans the session for avoiding cache or cookies
        errors, or giving false results based on cache

        :return: None
        """
        del self.session
        self.session = self._sess_bak or requests.Session()

    @property
    def _form_waiting(self):
        """
        Check if a form is actually on hold or not

        :return: True or False
        """
        if self.form is not None:
            return True
        return False

    def _parse_html(self, response):
        """
        Parse the response object and set the html property to response and to itself

        Html property is a lxml.Html object, needed for parsing the content, getting elements like form, etc...
        If you want the raw html, you can use both::

            response.read() # or .content for urllib response objects

        Or use lxml::

            lxml.html.tostring(response.html)

        :param response: Request or Urllib Response object
        :return: the upadted Response object
        """
        if not hasattr(response, 'html'):
            try:
                html = response.content
            except AttributeError:
                html = response.read()
                response.content = html
            tree = lh.fromstring(html)
            tree.make_links_absolute(base_url=self._base_url)
            response.html = tree
            self._html = tree
        return response

    def get_form(self, selector=None, nr=0, at_base=False):
        """
        Get the form selected by the selector and / or the nr param

        Raise:
            * oct.core.exceptions.FormNotFoundException
            * oct.core.exceptions.NoUrlOpen

        :param selector: A css-like selector for finding the form
        :param nr: the index of the form, if selector is set to None, it will search on the hole page
        :param at_base: must be set to true in case of form action is on the base_url page
        :return: None
        """
        if self._html is None:
            raise NoUrlOpen('No url open')

        if selector is None:
            self.form = self._html.forms[nr]
            self.form_data = dict(self._html.forms[nr].fields)
        else:
            sel = CSSSelector(selector)
            for el in sel(self._html):
                if el.forms:
                    self.form = el.forms[nr]
                    self.form_data = dict(el.forms[nr].fields)

        if self.form is None:
            raise FormNotFoundException('Form not found with selector {0} and nr {1}'.format(selector, nr))

        # common case where action was empty before make_link_absolute call
        if (self.form.action == self._base_url and
                self._url is not self._base_url and
                not at_base):
            self.form.action = self._url

    def get_select_values(self):
        """
        Get the available values of all select and select multiple fields in form

        :return: a dict containing all values for each fields
        """
        data = {}
        for i in self.form.inputs:
            if isinstance(i, lh.SelectElement):
                data[i.name] = i.value_options
        return data

    def submit_form(self):
        """
        Submit the form filled with form_data property dict

        Raise:
            oct.core.exceptions.NoFormWaiting

        :return: Response object after the submit
        """
        if not self._form_waiting:
            raise NoFormWaiting('No form waiting to be send')

        self.form.fields = self.form_data
        self._history.append(self.form.action)
        r = lh.submit_form(self.form, open_http=self._open_session_http)
        resp = self._parse_html(r)
        self.form_data = None
        self.form = None
        return resp

    def _open_session_http(self, method, url, values):
        """
        Custom method for form submission, send to lxml submit form method

        :param method: the method of the form (POST, GET, PUT, DELETE)
        :param url: the url of the action of the form
        :param values: the values of the form
        :return: Response object from requests.request method
        """
        return self.session.request(method, url, None, values)

    def open_url(self, url, data=None, back=False, **kwargs):
        """
        Open the given url

        :param url: The url to access
        :param data: Data to send. If data is set, the browser will make a POST request
        :param back: tell if we actually accessing a page of the history
        :return: The Response object from requests call
        """
        if not back:
            self._history.append(self._url)
        if data:
            response = self.session.post(url, data, headers=self._headers, **kwargs)
            self._url = url
        else:
            response = self.session.get(url, headers=self._headers, **kwargs)
            self._url = url
        response = self._parse_html(response)
        response.connection.close()
        return response

    def back(self):
        """
        Go to the previous url in the history property

        :return: the Response object
        """
        try:
            resp = self.open_url(self._history[-1], back=True)
            del self._history[-1]
            return resp
        except IndexError:
            raise Exception("No history, cannot go back")

    @property
    def history(self):
        """
        Return the actual history

        :return: the _history property
        :rtype: list
        """
        return self._history

    def follow_link(self, selector, url_regex=None):
        """
        Will access the first link found with the selector

        Raise:
            oct.core.exceptions.LinkNotFound

        :param selector: a string representing a css selector
        :param url_regex: regex for finding the url, can represent the href attribute or the link content
        :return: Response object
        """
        sel = CSSSelector(selector)
        resp = None

        if self._html is None:
            raise Exception('No url open')

        for e in sel(self._html):
            if url_regex:
                r = re.compile(url_regex)
                if r.match(e.get('href')) or r.match(e.xpath('string()')):
                    resp = self.open_url(e.get('href'))
                    return resp
            else:
                resp = self.open_url(e.get('href'))
                return resp

        if resp is None:
            raise LinkNotFound('Link not found')

    @staticmethod
    def open_in_browser(response):
        """
        Provide a simple interface for `lxml.html.open_in_browser` function.
        Be careful, use this function only for debug purpose

        :param response:
        :return:
        """
        lh.open_in_browser(response.html)