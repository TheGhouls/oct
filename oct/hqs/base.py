"""Define base HQ

This HQ will do nothing at all, it must be considered as an interface to build fonctionnal HeadQuarters.
All builtins HQs inherit from it.
HQs must at least contains those methods :

* wait_turrets(wait_for)  # Wait for N turrets to connect to HQ
* run()  # long running for tests, should be able to send start and stop signal to turrets
"""


class HeadQuarter(object):
    """Simple interface defining basic required methods

    :param str output_dir: output directory for results, needed even if you don't write results on disk
    :param dict config: current test configuration
    """
    def __init__(self, output_dir, config, *args, **kwargs):
        self.output_dir = output_dir
        self.config = config

    def wait_turrets(self, wait_for):
        """Wait until `wait_for` turrets are connected and ready.
        First methods that is called by start script, just before `run`

        :param int wait_for: number of turrets to wait for
        :return: None
        """
        raise NotImplementedError("HeadQuarter must implement wait_turrets method")

    def run(self):
        """Main loop of headquarter, will run for test period
        """
        raise NotImplementedError("HeadQUarter must implement run method")
