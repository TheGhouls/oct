from __future__ import print_function
import zmq
import time
import json
import traceback


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

        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind("tcp://*:{}".format(publish_port))

        self.poller.register(self.result_collector, zmq.POLLIN)

        self.stats_handler = stats_handler
        self.config = config
        self.turrets = []
        self.started = False

        # waiting for init sockets
        print("Warmup")
        time.sleep(1)

    def _turret_already_exists(self, turret_data):
        for t in self.turrets:
            if turret_data['uuid'] == t.uuid:
                return True
        return False

    def _add_turret(self, turret_data):
        self.turrets.append(self.stats_handler.write_turret(turret_data))
        if self.started:
            self._publish({'command': 'start', 'msg': 'open fire'})

    def _update_turret(self, turret_data):
        for t in self.turrets:
            if turret_data['uuid'] == t.uuid:
                t.status = turret_data['status']
                t.save()
                break

    def _publish(self, message, channel=''):
        data = json.dumps(message)
        self.publisher.send_string("%s %s" % (channel, data))

    def _process_turret_status(self, data):
        if 'status' in data:
            if self._turret_already_exists(data):
                self._update_turret(data)
            else:
                self._add_turret(data)
            return True
        else:
            return False

    def _process_socks(self, socks):
        if self.result_collector in socks:
            data = self.result_collector.recv_json()
            if 'status' not in data:
                self.stats_handler.write_result(data)
            else:
                self._process_turret_status(data)

    def _print_status(self, elapsed):
        display = 'turrets: {}, elapsed: {}   transactions: {}  timers: {}  errors: {}\r'
        print(display.format(len(self.turrets), round(elapsed), self.stats_handler.trans_count,
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
            self.publisher.close()
            self.stats_handler.write_remaining()

    def _run_loop_action(self):
        socks = dict(self.poller.poll(1000))
        self._process_socks(socks)

    def wait_turrets(self, wait_for):
        """Wait until wait_for turrets are connected and ready
        """
        print("waiting for {} turrets to connect".format(wait_for - len(self.turrets)))
        while len(self.turrets) < wait_for:
            self._publish({'command': 'status_request', 'msg': None})
            socks = dict(self.poller.poll(2000))
            if self.result_collector in socks:
                data = self.result_collector.recv_json()
                self._process_turret_status(data)
                print("waiting for {} turrets to connect".format(wait_for - len(self.turrets)))

    def run(self):
        """Run the hight quarter, lunch the turrets and wait for results
        """
        elapsed = 0
        start_time = time.time()
        self._publish({'command': 'start', 'msg': 'open fire'})
        self.started = True
        while elapsed <= (self.config['run_time']):
            try:
                self._run_loop_action()
                self._print_status(elapsed)
                elapsed = time.time() - start_time
            except (Exception, KeyboardInterrupt):
                print("\nStopping test, sending stop command to turrets")
                self._publish({'command': 'stop', 'msg': 'premature stop'})
                traceback.print_exc()
                break
        self._publish({'command': 'stop', 'msg': 'stopping fire'})
        print("\n\nProcessing all remaining messages...")
        self.result_collector.unbind(self.result_collector.LAST_ENDPOINT)
        self._clean_queue()
