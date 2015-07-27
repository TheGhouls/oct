import shutil
import unittest

from six.moves import configparser

from oct.utilities.newproject import create_project
from oct.multimechanize.utilities.run import run_test as run


run.no_test = True


class CmdOpts(object):

    def __init__(self, results_dir, projects_dir):
        self.port = None
        self.bind_addr = None
        self.results = results_dir
        self.projects_dir = projects_dir


class MainTest(unittest.TestCase):

    def setUp(self):
        self.project_path = '/tmp/oct-test'
        self.cmd_opts = CmdOpts(self.project_path + "/results", self.project_path)
        create_project(self.project_path)

        # update the runtime for the project
        config = configparser.RawConfigParser()
        config.read(self.project_path + "/config.cfg")
        config.set('global', 'run_time', 10)
        with open(self.project_path + "/config.cfg", 'w') as f:
            config.write(f)

    def test_run_project(self):
        """Test a simple 10sec run of the project"""
        run('.', self.cmd_opts)

    def tearDown(self):
        shutil.rmtree(self.project_path)
