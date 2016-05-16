from __future__ import print_function
import zmq
import time
import ujson
import traceback

from oct.core.turrets_manager import TurretsManager
from oct.results.stats_handler import StatsHandler


class HightQuarter(object):
    """The main hight quarter that will receive informations from the turrets
    and send the start message

    :param int publish_port: the port for publishing information to turrets
    :param int rc_port: the result collector port for collecting results from the turrets
    :param StatsHandler stats_handler: the stats handler writer
    :param dict config: the configuration of the test
    """
    def __init__(self, publish_port, rc_port, output_dir, config):
        self.context = zmq.Context()
        self.poller = zmq.Poller()

        self.result_collector = self.context.socket(zmq.PULL)
        self.result_collector.set_hwm(0)
        self.result_collector.bind("tcp://*:{}".format(rc_port))

        self.stats_handler = StatsHandler(output_dir, config)

        self.poller.register(self.result_collector, zmq.POLLIN)

        self.turrets_manager = TurretsManager(publish_port)
        self.config = config
        self.started = False
        self.messages = 0

        # waiting for init sockets
        print("Warmup")
        time.sleep(1)

    def _process_socks(self, socks):
        if self.result_collector in socks:
            self.messages += 1
            data = self.result_collector.recv()
            if b'status' not in data:
                self.stats_handler.write_result(ujson.loads(data))
                self.messages += 1
            else:
                self.turrets_manager.process_message(ujson.loads(data))
        pass

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
