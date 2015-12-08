import os
import sys
import shutil
import unittest

from oct.utilities.newproject import main


class UtilitiesTest(unittest.TestCase):

    def setUp(self):
        self.valid_dir = '/tmp/create-test'
        self.invalid_dir = '/create-test'

    def test_create_success(self):
        """The newproject utilities should be able to create a project
        """
        sys.argv[1] = self.valid_dir
        main()

    def test_create_error(self):
        """The newproject utilities should correctly return errors
        """
        sys.argv = sys.argv[:1]
        with self.assertRaises(IndexError):
            main()

        sys.argv.append(self.invalid_dir)
        with self.assertRaises(OSError):
            main()

    def tearDown(self):
        if os.path.exists(self.valid_dir):
            shutil.rmtree(self.valid_dir)
