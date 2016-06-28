import unittest
from multiprocessing import Process

from oct.core.devices import forwarder, streamer
from oct.utilities.run_device import start_device, run_device


class DummyArgs:

    device = 'forwarder'
    frontend = 0
    backend = 0


class DevicesTest(unittest.TestCase):

    def test_forwarder(self):
        """Should be able to start forwarder correctly
        """
        p = Process(target=forwarder, args=(0, 0))
        p.start()
        p.join(timeout=1)
        p.terminate()

    def test_streamer(self):
        """Should be able to start streamer
        """
        p = Process(target=streamer, args=(0, 0))
        p.start()
        p.join(timeout=1)
        p.terminate()

    def test_start_device_function(self):
        """Should be able to start device with start_device function
        """
        p = Process(target=start_device, args=('streamer', 0, 0))
        p.start()
        p.join(timeout=1)
        p.terminate()

    def test_run_device_function(self):
        """Should be able start device with run_device function
        """
        p = Process(target=start_device, args=('forwarder', 0, 0))
        p.start()
        p.join(timeout=1)
        p.terminate()
