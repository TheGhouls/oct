import csv


class GenericTransaction(object):

    def __init__(self, csv_dir=None):
        self.csv_dir = csv_dir

    def get_random_from_csv(self, csv_file):
        pass

    def __repr__(self):
        print "<Generic Transaction>"