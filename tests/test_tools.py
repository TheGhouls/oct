import os
import unittest

from oct.tools.results_to_csv import results_to_csv


class ToolsTest(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.output_file = '/tmp/oct-test-output.csv'
        self.results_file = os.path.join(self.base_dir, 'fixtures', 'results.sqlite')

    def test_convert_to_csv_success(self):
        """Convert sqlite result file to csv"""
        results_to_csv(self.results_file, self.output_file)
        self.assertTrue(os.path.isfile(self.output_file))

    def test_convert_to_csv_errors(self):
        """Convert sqlite result file to csv error"""
        with self.assertRaises(OSError):
            results_to_csv('bad_result_file', '/tmp/bad_results_file')

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
