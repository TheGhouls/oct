import os
import unittest

from oct.tools.xmltocsv import sitemap_to_csv
from oct.tools.results_to_csv import results_to_csv
from oct.tools.email_generator import email_generator_func


class ToolsTest(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.output_file = '/tmp/oct-test-output.csv'
        self.results_file = os.path.join(self.base_dir, 'results.sqlite')
        self.email_file = '/tmp/oct-test-email.csv'
        self.sitemap_xml = os.path.join(self.base_dir, 'sitemap.xml')
        self.sitemap_csv = '/tmp/oct-test-sitemap.xml'

    def test_convert_to_csv_success(self):
        """Convert sqlite result file to csv"""
        results_to_csv(self.results_file, self.output_file)
        self.assertTrue(os.path.isfile(self.output_file))

    def test_convert_to_csv_errors(self):
        """Convert sqlite result file to csv error"""
        with self.assertRaises(OSError):
            results_to_csv('bad_result_file', '/tmp/bad_results_file')

    def test_email_generator_success(self):
        """Generate random mail addresses"""
        email_generator_func(self.email_file, 'e')
        email_generator_func(self.email_file, 'z')
        self.assertTrue(os.path.isfile(self.email_file))

    def test_email_generator_errors(self):
        """Random email generator errors"""
        with self.assertRaises(IOError):
            email_generator_func('/bad/path/to/test/', 'e')

    def test_sitemap_generator_success(self):
        """CSV generation from sitemap.xml"""
        sitemap_to_csv(self.sitemap_xml, self.sitemap_csv)
        self.assertTrue(os.path.isfile(self.sitemap_csv))

    def test_sitemap_generator_errors(self):
        """CSV generation from sitemap.xml errors"""
        with self.assertRaises(IOError):
            sitemap_to_csv('/bad/path/to/input', self.sitemap_csv)

        with self.assertRaises(IOError):
            sitemap_to_csv(self.sitemap_xml, '/bad/pat/to/output')

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        if os.path.exists(self.email_file):
            os.remove(self.email_file)
        if os.path.exists(self.sitemap_csv):
            os.remove(self.sitemap_csv)
