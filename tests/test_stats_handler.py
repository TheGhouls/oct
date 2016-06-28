import unittest

from oct.results.stats_handler import init_stats


class ReportTest(unittest.TestCase):

    def test_bad_directory(self):
        """Not existing directory should raise error
        """
        with self.assertRaises(OSError):
            init_stats('/', {})
