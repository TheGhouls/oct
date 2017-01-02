import os
import unittest

from oct.results.report import ReportResults
from oct.backends import SQLiteLoader

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class ReportTest(unittest.TestCase):

    def test_empty_results(self):
        """Test report with empty results
        """
        config = {
            'testing': False,
            'results_database': {
                'db_uri': os.path.join(BASE_DIR, 'fixtures', 'empty_results.sqlite')
            }
        }
        loader = SQLiteLoader(config, '')
        report = ReportResults(60, 10, loader)
        report.compile_results()
