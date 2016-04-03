import unittest

from oct.results.stats_handler import StatsHandler


class ReportTest(unittest.TestCase):

    def test_bad_directory(self):
        """Not existing directory should raise error
        """
        with self.assertRaises(OSError):
            StatsHandler('/', '/')
