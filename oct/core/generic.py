
import csv
import os
from oct.core.browser import Browser
import requests
from threading import Thread
from lxml import etree
from io import BytesIO
from .exceptions import OctGenericException
import time
from six.moves import urllib, configparser
from six.moves.queue import Queue
import six
import random


class GenericTransaction(object):
    """
    Base class for Transaction, this class provides tools for simpler test writing

    :param handle_robots: set if robots are handle or not
    :type handle_robots: bool
    :param pathtoini: the path to the ini file
    :type pathtoini: str
    :param threads: number of threads for static files
    :type threads: int
    :param timeout: the timeout in second for static files requests
    """

    def __init__(self, pathtoini, **kwargs):

        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(pathtoini, 'config.cfg'))
        self.base_url = self.config.get('global', 'base_url')
        self.br = Browser(base_url=self.base_url)
        self.id_choice = None
        self.random_url = None
        self.q = Queue()
        self.custom_timers = {}
        self.timeout = kwargs.pop('timeout', 10)
        self.req = requests.Session()
        self.statics_include = None
        self.statics_enabled = None
        self.sleep_time = self.config.getfloat('global', 'default_sleep_time')

        for i in range(kwargs.pop('threads', 5)):
            t = Thread(target=self.multi_process_statics)
            t.daemon = True
            t.start()

    @staticmethod
    def csv_to_list(csv_file):
        """
        Take a csv file as parameter and read it. Return a list containing all lines

        :param csv_file: the csv file to read
        :type csv_file: str
        :return: A list containing the lines
        :rtype: list
        """
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            csv_list = [row for row in reader]
        return csv_list

    @staticmethod
    def get_random_csv(csv_list):
        """
        Simply return a random element from csv_list param

        :param csv_list: a list
        :return: random element from the csv_list
        """
        random_url = random.choice(csv_list)
        return random_url

    def multi_process_statics(self):
        """
        Multi threading static getter.
        This function will be call inside a Thread by the get_statics method

        :return: None
        """
        while True:
            url = self.q.get()
            try:
                if url.startswith('//'):
                    url = "http://".join(url)
                requests.get(url, allow_redirects=False, timeout=self.timeout)
            except Exception as e:
                print("Unexpected error: {0}".format(e))
            self.q.task_done()

    def get_statics(self, response, timer_name, include=None):
        """
        Get all static files for given response object. It will exclude all files in the exclude list

        :param response: The response object from browser
        :type response: MechanizeResponse
        :param timer_name: The timer name to increment
        :type timer_name: str
        :param include: The list of statics to exclude
        :type include: tuple
        :return: None
        """
        if self.statics_enabled is None:
            try:
                self.statics_enabled = self.config.getboolean('global', 'statics_enabled')
            except configparser.NoOptionError:
                print("No statics_enabled option in config file, set value to False (default value)")
                self.statics_enabled = False
        if not self.statics_enabled:
            return None

        if self.statics_include is None:
            try:
                items = self.config.items('statics')
                self.statics_include = tuple
                for key, value in enumerate(items):
                    self.statics_include += value
            except configparser.NoSectionError:
                self.statics_include = ('', )

        if include is None:
            include = self.statics_include

        html = response.read()
        parser = etree.HTMLParser()
        tree = etree.parse(BytesIO(html), parser)
        img = [img for img in tree.xpath('//img/@src') if img.startswith(include)]
        scripts = [s for s in tree.xpath('//script/@src') if s.startswith(include)]
        stylesheets = [s for s in tree.xpath('//link/@href') if s.startswith(include)]
        statics = img + scripts + stylesheets
        for key, static in enumerate(statics):
            if static[0] == '/' and static[1] != '/':
                statics[key] = self.base_url + static
            if not static.startswith('/') and not static.startswith('http'):
                statics[key] = self.base_url + "/" + static
        start_time = time.time()
        for static in statics:
            self.q.put(static)
        self.q.join()
        self.custom_timers[timer_name] = time.time() - start_time
        pass

    def run_generic_test(self, timer_name, url, test_func, *args):
        """
        Play the test_func param with *args parameters
        This function will call the browser on the url param for you
        You can pass existing or custom functions, but if you want to create custom
        test function, it must at least take a response object as first parameter

        Example of testing function and calling it::

            def my_test(response, other_param):
                assert(other_param not in response.html)

            # In Transaction run() method
            self.run_generic_test('my_timer', url, my_test, other_param)

        :param timer_name: the name of the timer
        :type timer_name: str
        :param url: the url to test
        :type url: str
        :param test_func: pointer on a testing function
        :type test_func: function
        :param args: the parameters of the test function
        :return: The response object from Mechanize.Browser()
        """
        start_time = time.time()
        try:
            resp = self.br.open_url(self.base_url + url)
        except urllib.error.HTTPError:
            raise OctGenericException
        except urllib.error.URLError:
            raise OctGenericException

        test_func(*args)

        self.custom_timers[timer_name] = time.time() - start_time
        return resp

    def get_form(self, **kwargs):
        """
        This method help you for getting a form in a given response object
        The form will be set inside the br property of the class

        :param selector: the css selector for getting the form
        :type selector: str
        :param nr: the position of the form inside the page, default to 0
        :type nr: int
        :return: None
        """
        self.br.get_form(kwargs.pop('selector', ''), kwargs.pop('nr', 0))

    def fill_form(self, form_data):
        """
        Fill the form selected in self.br with form_data dict

        The data dict must be of the form::

            {
                'field_name': 'field_value',
                'field2': 'field_value'
            }

        :param form_data: dict containing the data
        :type form_data: dict
        """
        for key, data in six.iteritems(form_data):
            self.br.form_data[key] = data

    def open_url(self, url, data=None):
        """
        Open an url with the Browser object

        :param url: the url to open
        :type url: str
        :param data: the data to pass to url
        :type data: dict
        """
        try:
            resp = self.br.open_url(self.base_url + url, data)
        except urllib.error.HTTPError as e:
            raise OctGenericException("Error accessing url: '{0}', error: {1}".format(self.base_url + url, e))
        except urllib.error.URLError as e:
            raise OctGenericException("URL ERROR with url: '{0}', error: {1}".format(self.base_url + url, e))
        return resp

    def auth(self, auth_url, data, use_form=True, **kwargs):
        """
        Authenticate yourself in the website with the provided data

        Data must be of the form::

            {
                'login_field_name': 'login',
                'password_filed_name': 'password'
            }

        :param auth_url: the url of the page for authentication
        :type auth_url: str
        :param selector: the css selector for the form
        :type selector: str
        :param nr: the position of the form inside the page
        :type nr: int
        :return: the response object from the submission
        """
        if not use_form:
            resp = self.br.open_url(self.base_url + auth_url, urllib.parse.urlencode(data))
        else:
            self.br.open_url(self.base_url + auth_url)
            self.get_form(**kwargs)
            self.fill_form(data)
            resp = self.br.submit_form()
        return resp

    def run(self):
        """
        Run method will be call by multi-mechanize run function
        You must implement it

        """
        raise NotImplementedError("You must implement the run method in your class")

    def __repr__(self):
        print("<Generic Transaction>")