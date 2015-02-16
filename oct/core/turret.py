from __future__ import print_function
from oct.multimechanize.core import load_script
import threading
import time
import sys
import os
import zmq


def main_loop(project_name, cmd_opts, config, output_dir):
    """
    Main run loop, will run all the tests.

    :param project_name: the name of the project
    :param cmd_opts: all parsed commands
    :return: None
    """
    script_prefix = os.path.join(cmd_opts.projects_dir, project_name, "test_scripts")
    script_prefix = os.path.normpath(script_prefix)

    turrets = []
    for i, ug_config in enumerate(config.user_group_configs):
        # now we sending messages here, no more instance of anything except the report manager
        script_file = os.path.join(script_prefix, ug_config.script_file)
        turret = Turret(cannons=ug_config.num_threads,
                        script_file=script_file, output_dir=output_dir,
                        run_time=config.run_time, rampup=config.rampup, turret_config=ug_config)
        turrets.append(turret)

    for turret in turrets:
        turret.fire()


class ReportManager(object):
    """
    This class will receive all messages from turrets and display them for user

    :param listen_url: the url for listening for the results
    :type listen_url: str
    :param output_dir: the directory for writing the results
    :type output_dir: str
    """
    def __init__(self, listen_url, output_dir):
        context = zmq.Context()

        self.socket = context.socket(zmq.PULL)
        self.socket.bind(listen_url)
        self.output_dir = output_dir
        self.data = {
            'transactions': 0,
            'errors': 0
        }

    def receive_message(self):

        message = {}

        # listen while turret send stop message
        # the message will be sent when turret have done firing
        # TODO wait untill all turrets have done firing
        while 'stop' not in message.keys() and not message['stop']:
            mess = self.socket.recv_json()
            if 'trans' in mess.keys():
                self.data['transactions'] += mess['trans']
            if 'errors' in mess.keys():
                self.data['errors'] += mess['errors']

            print("transactions : {trans}   errors : {err}".format(trans=self.data['transactions'],
                                                                   err=self.data['errors']), end='\r')

            with open(self.output_dir + 'results.csv', 'w') as f:
                f.write(mess['report'])
                f.flush()


class Turret(object):
    """
    Represent a Turret object that will use Cannon objects to execute scripts

    :param canons: the number of canons (threads) for this Turret
    :type cnanons: int
    :param script_file: the script file to execute
    :type script_file: str
    :param output_dir: the directory for the results
    :type output_dir: str
    :param run_time: the total time of run
    :type run_time: int
    :param rampup: the rampup param, representing the incrementation of cannons over time in seconds
    :type rampup: int
    :param turret_config: a dict containing the configuration variables for the turret
    :type turret_config: dict
    :param report_manager: the report manager instance for sending the results
    :type report_manager: ReportManager
    """
    def __init__(self, cannons, script_file, output_dir, run_time, rampup, turret_config, report_manager):
        self.cannons = cannons
        self.script_file = script_file
        self.script_module = load_script(self.script_file)
        self.run_time = run_time
        self.rampup = rampup
        self.start_time = time.time()
        self.output_dir = output_dir
        self.report_manager = report_manager

        # set the turret configuration and setup the turret
        context = zmq.Context()

        self.receiver = context.socket(zmq.SUB)
        self.receiver.connect(turret_config['connection_string'])
        self.receiver.setsockopt(zmq.SUBSCRIBE, turret_config['topic'])

        # set the report socket configuration
        self.sender = context.socket(zmq.PUSH)
        self.sender.connect(turret_config['report_url'])

    def wait_start(self):

        print("Turret online, waiting for HQ orders")
        while True:
            recv_str = self.receiver.recv()
            message = recv_str.split()[1]

            if message == "start":
                print("Start fire with {nb} cannons".format(nb=self.cannons))
                self.fire()

    def fire(self):

        threads = []
        for i in range(self.cannons):
            space = float(self.rampup) / float(self.cannons)

            if i > 0:
                time.sleep(space)

            cannon = Cannon(self.start_time, self.run_time, "Turret", self.script_module,
                            self.script_file, self.sender)
            cannon.daemon = True
            threads.append(cannon)
            cannon.start()

        for thread in threads:
            timeout = self.run_time - (self.start_time - time.time())
            if timeout < 0:
                timeout = 1
            threads.join(timeout=timeout)

        self.sender.send_json({'stop': True})


class Cannon(threading.Thread):
    """
    An object representing a user for executing the script

    :param process_num: the number of the process
    :param thread_num: the id of the thread
    :param start_time: the start time of the thread
    :param run_time: the total run_time of the test
    :param user_group_name: the name of the related user group
    :param script_module: the module containing the script to execute
    :param console_logging: boolean to know if we must log inside the console
    """
    def __init__(self, start_time, run_time,
                 user_group_name, script_module, script_file, sender):
        threading.Thread.__init__(self)
        self.start_time = start_time
        self.run_time = run_time
        self.user_group_name = user_group_name
        self.script_module = script_module
        self.script_file = script_file
        self.sender = sender

        # choose most accurate timer to use (time.clock has finer granularity
        # than time.time on windows, but shouldn't be used on other systems).
        if sys.platform.startswith('win'):
            self.default_timer = time.clock
        else:
            self.default_timer = time.time

    def run(self):
        elapsed = 0
        trans = self.script_module.Transaction()
        trans.custom_timers = {}

        # scripts have access to these vars, which can be useful for loading unique data
        trans.thread_num = self.thread_num
        trans.process_num = self.process_num

        while elapsed < self.run_time:
            error_count = 0
            trans_count = 0
            error = ''
            start = self.default_timer()

            try:
                trans.run()
            except Exception as e:  # test runner catches all script exceptions here
                error = str(e).replace(',', '')

            finish = self.default_timer()

            scriptrun_time = finish - start
            elapsed = time.time() - self.start_time
            self.trans_count += 1

            # don't include cleaning time into reports
            trans.br.clean_session()

            epoch = time.mktime(time.localtime())

            if error != '':
                # Convert line breaks to literal \n so the CSV will be readable.
                error = '\\n'.join(error.splitlines())
                error_count = 1
            else:
                trans = 1
            report_line = '%.3f|%i|%s|%f|%s|%s' % (elapsed, epoch,
                                                   self.user_group_name,
                                                   scriptrun_time, error,
                                                   repr(trans.custom_timers).replace(',', '--'))

            self.sender.send_json({'trans': trans_count, 'errors': error_count, 'report': report_line})
