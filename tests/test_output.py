import os
import json
import unittest

from oct.results.output import output

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class ReportTest(unittest.TestCase):

    def test_empty_results(self):
        """Test output with empty results
        """
        with open(os.path.join(BASE_DIR, 'fixtures', 'config.json')) as f:
            config = json.load(f)
            config['testing'] = False
            config['results_database'] = {'db_uri': os.path.join(BASE_DIR, 'fixtures', 'empty_results.sqlite')}
        output(os.path.join(BASE_DIR, '/tmp'),
               config)
