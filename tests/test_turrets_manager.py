import os
import unittest

from oct.core.turrets_manager import TurretsManager
from oct.backends.sqlite import set_database, db, Turret, Result

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class TestStore(object):
    def add_turret(self, data):
        pass

    def update_turret(self, data):
        pass


class ReportTest(unittest.TestCase):

    def setUp(self):
        set_database(os.path.join(BASE_DIR, 'fixtures', 'avaible_results.sqlite'), db, {})
        if not Result.table_exists() and not Turret.table_exists():
            db.create_tables([Result, Turret])
        self.manager = TurretsManager(0, TestStore())

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

    def test_master_false(self):
        """Turrets manager should act correctly in case of master set to false"""
        self.manager.master = False
        self.manager.process_message("bad")
        self.manager.publish("bad")
        self.manager.master = True

    def tearDown(self):
        for turret in Turret.select():
            turret.delete_instance()
