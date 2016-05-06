import os
import unittest

from oct.core.turrets_manager import TurretsManager
from oct.results.models import set_database, db

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class ReportTest(unittest.TestCase):

    def setUp(self):
        set_database(os.path.join(BASE_DIR, 'fixtures', 'avaible_results.sqlite'), db, {})
        self.manager = TurretsManager(0)

    def test_bad_message(self):
        """Turrets manager should correctly handle bad messages
        """
        res = self.manager.process_message({'bad': 'message'})
        self.assertFalse(res)

    def test_is_started(self):
        """Turrets manager should correctly handle turrets if tests are already started
        """
        res = self.manager.process_message({
            'cannons': 10,
            'rampup': 0,
            'turret': 'navigation',
            'script': 'v_user.py',
            'uuid': 'f26bda4a-e906-4e6c-b55a-5c1a0d00b7a6',
            'status': 'ready'}, is_started=True)
        self.assertTrue(res)

    def test_update(self):
        """Turrets manager should correctly handle message if no uuid is provided
        """
        res = self.manager.update({'not': 'present'})
        self.assertFalse(res)
