import unittest
from multiprocessing import Process

from oct.core.devices import forwarder, streamer


class DevicesTest(unittest.TestCase):

    def test_forwarder(self):
        """Should be able to start forwarder correctly
        """
        p = Process(target=forwarder, args=(0, 0))
        p.start()
        p.join(timeout=2)
        p.terminate()

    def test_streamer(self):
        """Should be able to start streamer
        """
        p = Process(target=streamer, args=(0, 0))
        p.start()
        p.join(timeout=2)
        p.terminate()
