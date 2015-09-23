import os
import shutil
import unittest
import json

from oct.utilities.newproject import create_project
from oct.multimechanize.utilities.run import run


class CmdOpts(object):

    def __init__(self, results_dir, projects_dir):
        self.port = None
        self.bind_addr = None
        self.results = results_dir
        self.projects_dir = projects_dir


class MainTest(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.realpath(__file__))
        self.project_path = '/tmp/oct-test'
        self.cmd_opts = CmdOpts(self.project_path + "/results", self.project_path)
        self.bad_cmd_opts = CmdOpts('/bad/project/path', '/bad/project/path')
        create_project(self.project_path)

        # update the runtime for the project
        with open(os.path.join(self.base_dir, 'config.json')) as f:
            data = json.load(f)

        with open(os.path.join(self.project_path, 'config.json'), 'w') as f:
            json.dump(data, f)

    def test_create_project_errors(self):
        """Test errors for create project"""
        with self.assertRaises(OSError):
            create_project('/bad/path/for/project')

        with self.assertRaises(OSError):
            create_project('/tmp')

    def test_run_project_success(self):
        """Test a simple 5sec run of the project"""
        run('.', self.cmd_opts)

    def tearDown(self):
        shutil.rmtree(self.project_path)
        if os.path.isfile('/tmp/results.sqlite'):
            os.remove('/tmp/results.sqlite')
