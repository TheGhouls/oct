import csv
import ConfigParser
import os
from mechanize import Browser
from Queue import Queue
import requests
from threading import Thread
import cookielib
from bs4 import BeautifulSoup
import time


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

    def get_random_from_csv(self, csv_file):
        pass

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
                    url = "http:"  + url
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
            self.statics_enabled = self.config.getboolean('global', 'statics_enabled')
        if not self.statics_enabled:
            return None

        if self.statics_include is None:
            items = self.config.items('statics')
            self.statics_include = tuple
            for key, value in enumerate(items):
                self.statics_include += value

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

    def __repr__(self):
        print "<Generic Transaction>"