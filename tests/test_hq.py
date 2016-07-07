import os
import sys
import unittest
import shutil
import json
from multiprocessing import Process
from oct_turrets.turret import Turret
from oct_turrets.utils import load_file, validate_conf
from oct.utilities.run import run
from oct.utilities.commands import main


BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def run_turret():
    """Run a simple turret for testing the hq
    """
    module = load_file(os.path.join(BASE_DIR, 'fixtures', 'v_user.py'))
    config = validate_conf(os.path.join(BASE_DIR, 'fixtures', 'turret_config.json'))
    turret = Turret(config, module)
    turret.start()


def run_bad_turret():
    module = load_file(os.path.join(BASE_DIR, 'fixtures', 'bad_user.py'))
    config = validate_conf(os.path.join(BASE_DIR, 'fixtures', 'turret_config.json'))
    turret = Turret(config, module)
    turret.start()


class CmdOpts(object):

    def __init__(self):

        self.project_path = '/tmp/oct-test'
        self.publisher_channel = None
        self.no_results = False


class HQTest(unittest.TestCase):

    def setUp(self):
        self.turret = Process(target=run_turret)
        self.turret.start()
        self.bad_turret = Process(target=run_bad_turret)
        self.bad_turret.start()
        sys.argv = sys.argv[:1]
        sys.argv += ["new-project", "/tmp/oct-test"]
        main()

        # update the runtime for the project
        with open(os.path.join(BASE_DIR, 'fixtures', 'config.json')) as f:
            data = json.load(f)

        with open(os.path.join('/tmp/oct-test', 'config.json'), 'w') as f:
            json.dump(data, f)

    def test_run_hq(self):
        """Test hq
        """
        run(CmdOpts())

    def test_run_argparse(self):
        """Test runing hq with command line arguments
        """
        sys.argv = sys.argv[:1]
        opts = CmdOpts()
        sys.argv += ["run", opts.project_path, "--with-forwarder"]
        main()

    def test_create_errors(self):
        """Test errors when creating project
        """
        with self.assertRaises(OSError):
            sys.argv = sys.argv[:1]
            sys.argv += ["new-project", "/tmp/"]
            main()

    def tearDown(self):
        shutil.rmtree('/tmp/oct-test')
        self.turret.terminate()
        self.bad_turret.terminate()
        if os.path.isfile('/tmp/results.sqlite'):
            os.remove('/tmp/results.sqlite')

if __name__ == '__main__':
    unittest.main()
