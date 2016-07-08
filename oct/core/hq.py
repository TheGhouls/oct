from __future__ import print_function
import zmq
import time
import ujson
import traceback
from zmq.utils.strtypes import asbytes

from oct.core.turrets_manager import TurretsManager
from oct.results.stats_handler import StatsHandler


class HightQuarter(object):
    """The main hight quarter that will receive informations from the turrets
    and send the start message

    :param str output_dir: output directory for results
    :param dict config: the configuration of the test
    :param str topic: topic for external publishing socket
    :param bool with_forwarder: tell HQ if it should connects to forwarder, default False
    :param bool with_streamer: tell HQ if ti should connects to streamer, default False
    :param str streamer_address: streamer address to connect with form : <ip>:<port>
    """

    def __init__(self, output_dir, config, topic, master=True, *args, **kwargs):
        self.context = zmq.Context()
        self.poller = zmq.Poller()
        self.topic = topic
        self.master = master

        self.result_collector = self.context.socket(zmq.PULL)
        self.external_publisher = self.context.socket(zmq.PUB)
        self.stats_handler = StatsHandler()

        self._configure_sockets(config)
        self.turrets_manager = TurretsManager(config.get('publish_port', 5000), master)
        self.config = config
        self.started = False
        self.messages = 0

        with_forwarder = kwargs.get('with_forwarder', False)
        forwarder_address = None
        if with_forwarder is True:
            forwarder_address = kwargs.get('forwarder_address', None)
            if forwarder_address is None:
                forwarder_address = "127.0.0.1:{}".format(config.get('external_publisher', 5002))

        self._configure_external_publisher(config, with_forwarder, forwarder_address)

        # waiting for init sockets
        print("Warmup")
        time.sleep(1)

    def _configure_external_publisher(self, config, with_forwarder=False, forwarder_address=None):
        external_publisher = config.get('external_publisher', 5002) if not forwarder_address else forwarder_address

        print(external_publisher)
        if with_forwarder:
            self.external_publisher.connect("tcp://{}".format(external_publisher))
        else:
            self.external_publisher.bind("tcp://*:{}".format(external_publisher))

    def _configure_sockets(self, config, with_streamer=False, with_forwarder=False):
        """Configure sockets for HQ

        :param dict config: test configuration
        :param bool with_streamer: tell if we need to connect to streamer or simply bind
        :param bool with_forwarder: tell if we need to connect to forwarder or simply bind
        """
        rc_port = config.get('rc_port', 5001)

        self.result_collector.set_hwm(0)
        self.result_collector.bind("tcp://*:{}".format(rc_port))

        self.poller.register(self.result_collector, zmq.POLLIN)

    def _process_socks(self, socks):
        if self.result_collector in socks:
            data = self.result_collector.recv_string()
            if 'status' not in data:
                self.stats_handler.write_result(ujson.loads(data))
                self.external_publisher.send_multipart([asbytes(self.topic), asbytes(data)])
                self.messages += 1
            else:
                self.turrets_manager.process_message(ujson.loads(data))

    def _print_status(self, elapsed):
        display = 'turrets: {}, elapsed: {}  messages received: {}\r'
        print(display.format(len(self.turrets_manager.turrets), round(elapsed), self.messages,), end='')

    def _clean_queue(self):
        try:
            data = self.result_collector.recv(zmq.NOBLOCK)
            while data:
                data = self.result_collector.recv(zmq.NOBLOCK)
                if b'status' not in data:
                    self.stats_handler.write_result(ujson.loads(data))
        except zmq.Again:
            self.result_collector.close()
            self.turrets_manager.clean()
            self.stats_handler.write_remaining()

    def _run_loop_action(self):
        socks = dict(self.poller.poll(1000))
        self._process_socks(socks)

    def wait_turrets(self, wait_for):
        """Wait until wait_for turrets are connected and ready
        """
        print("Waiting for %d turrets" % (wait_for - len(self.turrets_manager.turrets)))

        while len(self.turrets_manager.turrets) < wait_for:
            self.turrets_manager.status_request()

            socks = dict(self.poller.poll(2000))

            if self.result_collector in socks:
                data = self.result_collector.recv_json()
                self.turrets_manager.process_message(data)

                print("Waiting for %d turrets" % (wait_for - len(self.turrets_manager.turrets)))

    def run(self):
        """Run the hight quarter, lunch the turrets and wait for results
        """
        elapsed = 0
        run_time = self.config['run_time']
        start_time = time.time()
        t = time.time
        self.turrets_manager.start()
        self.started = True

        while elapsed <= run_time:
            try:
                self._run_loop_action()
                self._print_status(elapsed)
                elapsed = t() - start_time
            except (Exception, KeyboardInterrupt):
                print("\nStopping test, sending stop command to turrets")
                self.turrets_manager.stop()
                self.stats_handler.write_remaining()
                traceback.print_exc()
                break

        self.turrets_manager.stop()
        print("\n\nProcessing all remaining messages... This could take time depending on message volume")
        t = time.time()
        self.result_collector.unbind(self.result_collector.LAST_ENDPOINT)
        self._clean_queue()
        print("took %s" % (time.time() - t))
