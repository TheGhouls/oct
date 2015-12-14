import os
import sys
import shutil
import unittest

from oct.utilities.newproject import main as main_new_project, create_project
from oct.utilities.pack import main as main_pack


class UtilitiesTest(unittest.TestCase):

    def setUp(self):
        self.valid_dir = '/tmp/create-test'
        self.invalid_dir = '/create-test'
        self.test_dir = '/tmp/utiles_tests'

        create_project(self.test_dir)

    def test_create_success(self):
        """The newproject utilities should be able to create a project
        """
        sys.argv[1] = self.valid_dir
        main_new_project()

    def test_create_error(self):
        """The newproject utilities should correctly return errors
        """
        sys.argv = sys.argv[:1]
        with self.assertRaises(IndexError):
            main_new_project()

        sys.argv.append(self.invalid_dir)
        with self.assertRaises(OSError):
            main_new_project()

    def test_pack_success(self):
        """Should be able to generate tar archives from project folder
        """
        sys.argv = sys.argv[:1]
        sys.argv.append(self.test_dir)
        main_pack()

        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'navigation.tar')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'random.tar')))

    def test_pack_errors(self):
        """Pack function should correctly raise errors
        """
        sys.argv = sys.argv[:1]
        sys.argv.append(self.invalid_dir)
        with self.assertRaises(SystemExit):
            main_pack()

        sys.argv = sys.argv[:1]
        sys.argv.append(self.test_dir)
        open(os.path.join(self.test_dir, 'navigation.tar'), 'a').close()
        os.chmod(os.path.join(self.test_dir, 'navigation.tar'), 0o444)
        main_pack()

    def tearDown(self):
        if os.path.exists(self.valid_dir):
            shutil.rmtree(self.valid_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
