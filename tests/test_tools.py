import os
import unittest

from oct.tools.results_to_csv import results_to_csv
from oct.tools.email_generator import email_generator_func


class ToolsTest(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.output_file = '/tmp/oct-test-output.csv'
        self.results_file = os.path.join(self.base_dir, 'results.json')
        self.email_file = '/tmp/oct-test-email.csv'

    def test_convert_to_csv(self):
        """Convert json result file to csv"""
        results_to_csv(self.results_file, self.output_file)
        self.assertTrue(os.path.isfile(self.output_file))

    def test_email_generator(self):
        """Generate random mail addresses"""
        email_generator_func(self.email_file, 'e')
        email_generator_func(self.email_file, 'z')
        self.assertTrue(os.path.isfile(self.email_file))

    def tearDown(self):
        try:
            os.remove(self.output_file)
            os.remove(self.email_file)
        except OSError:
            # Already removed
            pass
