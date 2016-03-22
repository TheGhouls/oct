import os
import json
import unittest

from oct.results.output import output
from oct.results.models import set_database, db

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class ReportTest(unittest.TestCase):

    def test_empty_results(self):
        """Test output with empty results
        """
        set_database(os.path.join(BASE_DIR, 'fixtures', 'empty_results.sqlite'), db, {})
        with open(os.path.join(BASE_DIR, 'fixtures', 'config.json')) as f:
            config = json.load(f)
        output(os.path.join(BASE_DIR, '/tmp'),
               config)
