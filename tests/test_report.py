import unittest

from oct.results.reportwriter import Report


class ReportTest(unittest.TestCase):

    def test_bad_directory(self):
        """Not existing results directory should be able to instantiate
        """
        Report('/tmp/bad/dir/for/report', '/')

    def test_bad_permissions(self):
        """Results folder with bad permissions should raise an error
        """
        with self.assertRaises(OSError):
            Report('/', '/')
