from __future__ import print_function
import zmq
import time
import traceback

from oct.core.turrets_manager import TurretsManager


class HightQuarter(object):
    """The main hight quarter that will receive informations from the turrets
    and send the start message

    :param int publish_port: the port for publishing information to turrets
    :param int rc_port: the result collector port for collecting results from the turrets
    :param StatsHandler stats_handler: the stats handler writer
    :param dict config: the configuration of the test
    """
    def __init__(self, publish_port, rc_port, stats_handler, config):
        self.context = zmq.Context()
        self.poller = zmq.Poller()

        self.result_collector = self.context.socket(zmq.PULL)
        self.result_collector.bind("tcp://*:{}".format(rc_port))

        self.poller.register(self.result_collector, zmq.POLLIN)

        self.stats_handler = stats_handler
        self.turrets_manager = TurretsManager(publish_port)
        self.config = config
        self.started = False

        # waiting for init sockets
        print("Warmup")
        time.sleep(1)

    def _process_socks(self, socks):
        if self.result_collector in socks:
            data = self.result_collector.recv_json()
            if 'status' not in data:
                self.stats_handler.write_result(data)
            else:
                self.turrets_manager.process_message(data)

    def _print_status(self, elapsed):
        display = 'turrets: {}, elapsed: {}   transactions: {}  timers: {}  errors: {}\r'
        print(display.format(len(self.turrets_manager.turrets), round(elapsed),
                             self.stats_handler.trans_count,
                             self.stats_handler.timer_count,
                             self.stats_handler.error_count), end='')

    def _clean_queue(self):
        try:
            data = self.result_collector.recv_json(zmq.NOBLOCK)
            while data:
                data = self.result_collector.recv_json(zmq.NOBLOCK)
                if 'status' not in data:
                    self.stats_handler.write_result(data)
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
        start_time = time.time()
        self.turrets_manager.start()
        self.started = True

        while elapsed <= (self.config['run_time']):
            try:
                self._run_loop_action()
                self._print_status(elapsed)
                elapsed = time.time() - start_time
            except (Exception, KeyboardInterrupt):
                print("\nStopping test, sending stop command to turrets")
                self.turrets_manager.stop()
                traceback.print_exc()
                break

        self.turrets_manager.stop()
        print("\n\nProcessing all remaining messages...")
        self.result_collector.unbind(self.result_collector.LAST_ENDPOINT)
        self._clean_queue()
