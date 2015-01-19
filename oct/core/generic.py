from threading import Thread
from lxml import etree
from io import BytesIO
from .exceptions import OctGenericException
import time
from six.moves import urllib, configparser
from six.moves.queue import Queue
from oct.core.browser import Browser
import requests
import six
import random
import csv
import os


class GenericTransaction(object):
    """
    Base class for Transaction, this class provides tools for simpler test writing

    :param handle_robots: set if robots are handle or not
    :type handle_robots: bool
    :param pathtoini: the path to the ini file
    :type pathtoini: str
    :param timeout: the timeout in second for static files requests
    :type timeout: int
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
        self.sleep_time = self.config.getfloat('global', 'default_sleep_time')

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
