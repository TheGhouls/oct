from __future__ import print_function
import zmq
import time
import json


class HightQuarter(object):
    """The main hight quarter that will receive informations from the turrets
    and send the start message

    :param publish_port int: the port for publishing information to turrets
    :param rc_port int: the result collector port for collecting results from the turrets
    :param results_writer ResultsWriter: the results writer
    :param config dict: the configuration of the test
    """
    def __init__(self, publish_port, rc_port, results_writer, config):
        context = zmq.Context()

        self.poller = zmq.Poller()

        self.result_collector = context.socket(zmq.PULL)
        self.result_collector.bind("tcp://*:{}".format(rc_port))

        self.publisher = context.socket(zmq.PUB)
        self.publisher.bind("tcp://*:{}".format(publish_port))

        self.poller.register(self.result_collector, zmq.POLLIN)

        self.results_writer = results_writer
        self.config = config
        self.turrets = []

        self._publish({'command': 'status_request', 'msg': None})

    def _turret_already_exists(self, turret_data):
        for t in self.turrets:
            if turret_data['uuid'] == t['uuid']:
                return False
        return True

    def _update_turret(self, turret_data):
        for t in self.turrets:
            if turret_data['uuid'] == t['uuid']:
                t['status'] = turret_data['status']
                break

    def _publish(self, message):
        data = json.dumps(message)
        self.publisher.send_multipart([bytes('hq', 'UTF-8'), bytes(data, 'UTF-8')])

    def wait_turrets(self, wait_for):
        """Wait until wait_for turrets are connected and ready
        """
        print("waiting for {} turrets to connect".format(wait_for - len(self.turrets)))
        while len(self.turrets) < wait_for:
            socks = dict(self.poller.poll(1000))
            if self.result_collector in socks:
                data = self.result_collector.recv_json()
                if 'turret' in data and 'status' in data and not self._turret_already_exists(data):
                    self.turrets.append({'turret': data['turret'], 'status': data['status'], 'uuid': data['uuid']})
                    print("{} turrets are now connected".format(len(self.turrets)))
                    print("waiting for {} turrets to connect".format(wait_for - len(self.turrets)))
                elif 'turret' in data and 'status' in data and self._turret_already_exists(data):
                    self._update_turret(data)

    def run(self):
        """Run the hight quarter, lunch the turrets and wait for results
        """
        elapsed = 0
        start_time = time.time()
        self._publish({'command': 'start', 'msg': 'open fire'})
        display = 'turrets: {}, elapsed: {}   transactions: {}  timers: {}  errors: {}\r'
        while elapsed < (self.config['run_time'] + 1):
            try:
                socks = dict(self.poller.poll(1000))
                if self.result_collector in socks:
                    data = self.result_collector.recv_json()
                    if 'status' in data:
                        self.turrets.append((data['turret'], data['status']))
                    else:
                        self.results_writer.write_result(data)
                print(display.format(self.turrets, round(elapsed), self.results_writer.trans_count,
                                     self.results_writer.timer_count,
                                     self.results_writer.error_count), end='')
                elapsed = time.time() - start_time
            except (Exception, KeyboardInterrupt) as e:
                print("\nStopping test, sending stop command to turrets")
                self._publish({'command': 'stop', 'msg': 'premature stop'})
                print(e)
                break
        self._publish({'command': 'stop', 'msg': 'stopping fire'})
