import os
import unittest

from oct.utilities.configuration import configure, configure_for_turret
from oct.core.exceptions import OctConfigurationError

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class ConfigTest(unittest.TestCase):

    def setUp(self):
        self.good_config = os.path.join(BASE_DIR, 'fixtures', 'config.json')
        self.bad_config = os.path.join(BASE_DIR, 'fixtures', 'bad_config.json')
        self.missing_keys = os.path.join(BASE_DIR, 'fixtures', 'missing_keys.json')

    def test_good_config(self):
        """Configuration should be parsable
        """
        configure(None, None, config_file=self.good_config)

    def test_bad_config(self):
        """Bad configuration file should correctly raise exceptions
        """
        with self.assertRaises(OctConfigurationError):
            configure(None, None, config_file=self.bad_config)

    def test_missing_keys(self):
        """Missing keys in configuration should correctly raise exceptions
        """
        with self.assertRaises(OctConfigurationError):
            configure(None, None, config_file=self.missing_keys)

    def test_config_turrets(self):
        """Turrets must be configurable from a good config file
        """
        configure_for_turret(None, self.good_config)
