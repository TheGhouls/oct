from __future__ import print_function
import zmq
import time
import json
import traceback


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
        self.started = False

        # waiting for init sockets
        print("Warmup")
        time.sleep(1)

    def _turret_already_exists(self, turret_data):
        for t in self.turrets:
            if turret_data['uuid'] == t['uuid']:
                return True
        return False

    def _add_turret(self, turret_data):
        turret = {
            'name': turret_data['turret'],
            'canons': turret_data['canons'],
            'script': turret_data['script'],
            'rampup': turret_data['rampup']
        }
        self.results_writer.write_turret(turret)
        turret['uuid'] = turret_data['uuid']
        self.turrets.append(turret)
        if self.started:
            self._publish({'command': 'start', 'msg': 'open fire'})

    def _update_turret(self, turret_data):
        for t in self.turrets:
            if turret_data['uuid'] == t['uuid']:
                t['status'] = turret_data['status']
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
        display = 'turrets: {}, elapsed: {}   transactions: {}  timers: {}  errors: {}\r'
        while elapsed <= (self.config['run_time']):
            try:
                socks = dict(self.poller.poll(1000))
                if self.result_collector in socks:
                    data = self.result_collector.recv_json()
                    if 'status' not in data:
                        self.results_writer.write_result(data)
                    else:
                        self._process_turret_status(data)
                print(display.format(self.turrets, round(elapsed), self.results_writer.trans_count,
                                     self.results_writer.timer_count,
                                     self.results_writer.error_count), end='')
                elapsed = time.time() - start_time
            except (Exception, KeyboardInterrupt):
                print("\nStopping test, sending stop command to turrets")
                self._publish({'command': 'stop', 'msg': 'premature stop'})
                traceback.print_exc()
                break
        self._publish({'command': 'stop', 'msg': 'stopping fire'})
        self.result_collector.close()
        self.publisher.close()
