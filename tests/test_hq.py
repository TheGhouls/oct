import os
import unittest
import shutil
import json
from multiprocessing import Process
from oct_turrets.turret import Turret
from oct_turrets.utils import load_file, validate_conf
from oct.utilities.run import run
from oct.utilities.newproject import create_project


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def run_turret():
    """Run a simple turret for testing the hq
    """
    module = load_file(os.path.join(BASE_DIR, 'fixtures', 'v_user.py'))
    config = validate_conf(os.path.join(BASE_DIR, 'fixtures', 'turret_config.json'))
    turret = Turret(config, module)
    turret.start()


class CmdOpts(object):
    projects_dir = '/tmp/oct-test'


class HQTest(unittest.TestCase):

    def setUp(self):
        self.turret = Process(target=run_turret)
        self.turret.start()
        create_project('/tmp/oct-test')

        # update the runtime for the project
        with open(os.path.join(BASE_DIR, 'fixtures', 'config.json')) as f:
            data = json.load(f)

        with open(os.path.join('/tmp/oct-test', 'config.json'), 'w') as f:
            json.dump(data, f)

    def test_run_hq(self):
        """Test hq
        """
        run('.', CmdOpts())

    def tearDown(self):
        shutil.rmtree('/tmp/oct-test')
        self.turret.terminate()

if __name__ == '__main__':
    unittest.main()
