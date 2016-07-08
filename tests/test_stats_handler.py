import os
import shutil
import unittest

from oct.utilities.configuration import configure
from oct.results.stats_handler import init_stats, StatsHandler

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class ReportTest(unittest.TestCase):

    def setUp(self):
        config_file = os.path.join(BASE_DIR, 'fixtures', 'config.json')
        self.config = configure(None, config_file)
        self.handler = StatsHandler(None)

    def test_bad_directory(self):
        """Not existing directory should raise error
        """
        with self.assertRaises(OSError):
            init_stats('/', {})

    def test_write_results(self):
        init_stats('/tmp/oct_stats_tests', self.config)
        data = {
            'elapsed': 1.1,
            'epoch': 22222222222,
            'scriptrun_time': 20,
            'error': '',
            'custom_timers': {}
        }
        for i in range(490):
            self.handler.write_result(data.copy())
        self.handler.write_remaining()

    def tearDown(self):
        if os.path.exists('/tmp/oct_stats_tests'):
            shutil.rmtree('/tmp/oct_stats_tests')
