import requests
import re
import lxml.html as lh
from lxml.cssselect import CSSSelector


class Browser(object):
    """
    This class represent a minimal browser. Build on top of lxml awesome library it let you write script for accessing
    or testing website with python scripts

    :param session: The session object to use. If set to None will use requests.Session
    :param base_url: The base url for the website, will append it for every link without a full url
    """
    def __init__(self, session=None, base_url=''):
        self.session = session or requests.Session()
        self._history = []
        self._html = None
        self._url = None
        self._back_index = False
        self._base_url = base_url
        self.form = None
        self.form_data = None

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

    def get_form(self, selector=None, nr=0):
        """
        Get the form selected by the selector and / or the nr param

        :param selector: A css-like selector for finding the form
        :param nr: the index of the form, if selector is set to None, it will search on the hole page
        :return: None
        """
        if self._html is None:
            raise Exception('Cannot find form if no url open')

        if selector is None:
            self.form = self._html.forms[nr]
            self.form_data = dict(self._html.forms[nr].fields)
        else:
            sel = CSSSelector(selector)
            for el in sel(self._html):
                if el.forms:
                    self.form = el.forms[nr]
                    self.form_data = dict(el.forms[0].fields)

    def submit_form(self):
        """
        Submit the form filled with form_data property dict

        :return: Response object after the submit
        """
        if not self._form_waiting:
            raise Exception('No form waiting to be send')

        self.form.fields = self.form_data
        self._history.append(self.form.action)
        r = lh.submit_form(self.form)
        resp = self._parse_html(r)
        self.form_data = None
        self.form = None
        return resp

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
            response = self.session.post(url, data, **kwargs)
            self._url = url
        else:
            response = self.session.get(url, **kwargs)
            self._url = url
        response = self._parse_html(response)
        return response

    def back(self):
        """
        Go to the previous url in the history property

        :return: the Response object
        """
        if self._history[-1]:
            resp = self.open_url(self._history[-1], back=True)
            del self._history[-1]
            return resp
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
            raise Exception('Link not found')
