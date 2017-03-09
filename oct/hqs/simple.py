from __future__ import print_function
import time
import traceback

import zmq
import ujson
from zmq.utils.strtypes import asbytes

from oct.hqs.base import HeadQuarter
from oct.core.turrets_manager import TurretsManager


class SimpleHeadQuarter(HeadQuarter):
    """This class represent the simplest possible HQ, using default turret manager to communicate with
    turrets using json.

    This headquarter works alone, receiving informations directly from turrets and managing all messages itself.
    Perfect for small tests will small amount of messages per seconds.
    In addition this HQ provide an external publisher socket to monitor received messages from outside of OCT

    :param str topic: topic for external publishing socket
    """
    def __init__(self, output_dir, config, topic, *args, **kwargs):
        super(SimpleHeadQuarter, self).__init__(output_dir, config, *args, **kwargs)

        self.poller = zmq.Poller()
        self.topic = topic

        self.result_collector = self.context.socket(zmq.PULL)
        self.external_publisher = self.context.socket(zmq.PUB)

