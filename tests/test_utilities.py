import os
import sys
import shutil
import unittest

from oct.utilities.commands import main


class UtilitiesTest(unittest.TestCase):

    def setUp(self):
        self.valid_dir = '/tmp/create-test'
        self.invalid_dir = '/create-test'
        self.test_dir = '/tmp/utiles_tests'

        sys.argv = sys.argv[:1]
        sys.argv += ["new-project", self.test_dir]
        main()

    def test_create_success(self):
        """The newproject utilities should be able to create a project
        """
        sys.argv = sys.argv[:1]
        sys.argv += ["new-project", self.valid_dir]
        main()

    def test_pack_success(self):
        """Should be able to generate tar archives from project folder
        """
        sys.argv = sys.argv[:1]
        sys.argv += ["pack-turrets", self.test_dir]
        main()

        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'navigation.tar')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'random.tar')))

    def test_pack_errors(self):
        """Pack function should correctly raise errors
        """
        with self.assertRaises(SystemExit):
            sys.argv = sys.argv[:1]
            sys.argv += ["pack-turrets", self.invalid_dir]
            main()

        sys.argv = sys.argv[:1]
        sys.argv += ["pack-turrets", self.test_dir]
        open(os.path.join(self.test_dir, 'navigation.tar'), 'a').close()
        os.chmod(os.path.join(self.test_dir, 'navigation.tar'), 0o444)
        main()

    def tearDown(self):
        if os.path.exists(self.valid_dir):
            shutil.rmtree(self.valid_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
