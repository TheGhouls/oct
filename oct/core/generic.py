import csv
import ConfigParser
import os
from mechanize import Browser
from Queue import Queue
import requests
from threading import Thread
import cookielib
from bs4 import BeautifulSoup
from exceptions import OctGenericException
from mechanize import FormNotFoundError
import time
import urllib2
import random


class GenericTransaction(object):
    def __init__(self, handle_robots, pathtoini, **kwargs):
        """
        Initialize the base object for using method in your Transaction

        :param handle_robots: set if robots are handle or not
        :type handle_robots: bool
        :param pathtoini: the path to the ini file
        :type pathtoini: str
        :param threads: number of threads for static files
        :type threads: int
        :param timeout: the timeout in second for static files requests
        :param use_cookies: default to True, set to False if you don't want cookies with browser object
        """
        self.config = ConfigParser.ConfigParser()
        self.config.read(os.path.join(pathtoini, 'config.cfg'))
        self.base_url = self.config.get('global', 'base_url')
        self.br = Browser()
        self.br.set_handle_robots(handle_robots)
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

        if kwargs.pop('use_cookie', True):
            # Cookie Jar
            cj = cookielib.LWPCookieJar()
            self.br.set_cookiejar(cj)

        if 'user_agent' in kwargs:
            self.br.addheaders = [('User-agent', kwargs.pop('user_agent'))]

    def csv_to_list(self, csv_file):
        with open(csv_file, 'rb') as f:
            reader = csv.reader(f)
            csv_list = list(reader)
        return csv_list

    def get_random_csv(self, csvfile):
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
            except ConfigParser.NoOptionError:
                print "No statics_enabled option in config file, set value to False (default value)"
                self.statics_enabled = False
        if not self.statics_enabled:
            return None

        if self.statics_include is None:
            try:
                items = self.config.items('statics')
                self.statics_include = tuple
                for key, value in enumerate(items):
                    self.statics_include += value
            except ConfigParser.NoSectionError:
                self.statics_include = ('', )

        if include is None:
            include = self.statics_include

        soup = BeautifulSoup(response.read())
        img = [i['src'] for i in soup.findAll('img', src=True) if i['src'].startswith(include)]
        scripts = [s['src'] for s in soup.findAll('scripts', src=True) if s['src'].startswith(include)]
        stylesheets = [s['href'] for s in soup.findAll('link', href=True) if s['href'].startswith(include)]
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
            resp = self.br.open(url)
        except urllib2.HTTPError, err:
            raise (OctGenericException("Error accessing url: '{0}', message: {1}".format(url, str(err))))
        except urllib2.URLError, err:
            raise (OctGenericException("URL ERROR with url: '{0}', message: {1}".format(url, str(err))))

        test_func(*args)

        self.custom_timers[timer_name] = time.time() - start_time
        return resp

    def get_form(self, **kwargs):
        """
        This method help you for getting a form in a given response object
        The form will be set inside the br property of the class

        :param form_name: the name attribute of the form
        :type form_name: str
        :param form_id: the id attribute of the form
        :type form_id: str
        :param form_class: the class attribute of the form
        :type form_class: str
        :return: None
        """
        if 'form_name' not in kwargs:
            if 'form_id' in kwargs:
                predicate = lambda f: 'id' in f.attrs and f.attrs['id'] == kwargs['form_id']
            elif 'form_class' in kwargs:
                predicate = lambda f: 'class' in f.attrs and f.attrs['class'] == kwargs['class']
            else:
                raise FormNotFoundError("You have to at least give a name, a class or an id")
            self.br.select_form(predicate=predicate)
        else:
            self.br.select_form(name=kwargs['form_name'])

    def fill_form(self, form_data):
        """
        Fill the form selected in self.br with form_data dict

        :param form_data: dict containing the data
        :type form_data: dict
        """
        for key, data in form_data.iteritems():
            self.br[key] = data

    def open_url(self, url, data=None):
        """
        Open an url with the Browser object

        :param url: the url to open
        :type url: str
        :param data: the data to pass to url
        :type data: dict
        """
        try:
            resp = self.br.open(self.base_url + url, data)
        except urllib2.HTTPError, e:
            raise OctGenericException("Error accessing url: '{0}', error: {0}".format(self.base_url + url, e))
        except urllib2.URLError, e:
            raise OctGenericException("URL ERROR with url: '{0}', error: {0}".format(self.base_url + url, e))
        return resp

    def run(self):
        """
        Run method will be call by multi-mechanize run function
        You must implement it

        """
        raise NotImplementedError("You must implement the run method in your class")

    def __repr__(self):
        print "<Generic Transaction>"