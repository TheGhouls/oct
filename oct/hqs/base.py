"""Define base HQ

This HQ will do nothing at all, it must be considered as an interface to build fonctionnal HeadQuarters.
All builtins HQs inherit from it.
HQs must at least contains those methods :

* wait_turrets(wait_for)  # Wait for N turrets to connect to HQ
* run()  # long running for tests, should be able to send start and stop signal to turrets

By default this headquarter will try to load store_class based on test configuration. If you want to write a
reusable headquarter, don't enforce store_class, always let users choose wich store fit their needs
"""
import zmq

from oct.core.exceptions import OctConfigurationError
from oct.utilities.configuration import get_store_class


class HeadQuarter(object):
    """Simple interface defining basic required methods.
    Since all protocol of OCT is based on zeromq, this base headquarter will create zmq_context itself and
    store it in `self.context` attribute.

    :param str output_dir: output directory for results, needed even if you don't write results on disk
    :param dict config: current test configuration
    """
    def __init__(self, output_dir, config, *args, **kwargs):
        self.context = zmq.Context()
        self.output_dir = output_dir
        self.config = config

        try:
            store_class = get_store_class(config)
            self.store = store_class(config, output_dir)
        except Exception:
            raise OctConfigurationError("Cannot load store class, check your configuration")

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
