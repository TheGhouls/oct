import unittest

from oct.results.writer import ReportWriter


class ReportTest(unittest.TestCase):

    def test_bad_directory(self):
        """Not existing results directory should be able to instantiate
        """
        ReportWriter('/tmp/bad/dir/for/report', '/')

    def test_bad_permissions(self):
        """Results folder with bad permissions should raise an error
        """
        with self.assertRaises(OSError):
            ReportWriter('/', '/')
