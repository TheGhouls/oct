import json
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

        with open(os.path.join(pathtoini, 'config.json'), 'r') as f:
            self.config = json.load(f)
        self.id_choice = None
        self.random_url = None
        self.custom_timers = {}
        self.sleep_time = 1

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

    def run(self):
        """
        Run method will be call by multi-mechanize run function
        You must implement it

        """
        raise NotImplementedError("You must implement the run method in your class")

    def tear_down(self):
        """This method will be executed at the end of the run method, usefull if you need to close or clean some
        resources
        """
        pass

    def __repr__(self):
        print("<Generic Transaction>")
