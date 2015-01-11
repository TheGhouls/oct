from celery import Task, Celery
from celery.utils.log import get_task_logger
from oct.multimechanize.core import load_script
import threading
import time
import sys
import logging

# This is the main app, update it if you need to inside your project
app = Celery('oct', broker=None, backend=None)

logger = get_task_logger(__name__)
logger.trans_count = 0


class Agent(threading.Thread):
    """
    An object representing a agent for executing the script. Inherit from thread class and will be start within celery
     task

    :param process_num: the number of the process
    :param thread_num: the id of the thread
    :param start_time: the start time of the thread
    :param run_time: the total run_time of the test
    :param user_group_name: the name of the related user group
    :param script_module: the module containing the script to execute
    :param console_logging: boolean to know if we must log inside the console
    """
    def __init__(self, process_num, thread_num, start_time, run_time,
                 user_group_name, script_module, script_file, console_logging):
        threading.Thread.__init__(self)
        self.process_num = process_num
        self.thread_num = thread_num
        self.start_time = start_time
        self.run_time = run_time
        self.user_group_name = user_group_name
        self.script_module = script_module
        self.script_file = script_file
        self.console_logging = console_logging
        self.error_count = 0

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
            error = ''
            start = self.default_timer()

            try:
                trans.run()
            except Exception as e:  # test runner catches all script exceptions here
                error = str(e).replace(',', '')

            finish = self.default_timer()

            scriptrun_time = finish - start
            elapsed = time.time() - self.start_time

            # don't include cleaning time into reports
            trans.br.clean_session()

            epoch = time.mktime(time.localtime())

            if error != '':
                # Convert line breaks to literal \n so the CSV will be readable.
                error = '\\n'.join(error.splitlines())
                self.error_count += 1
            logger.info('%d|%.3f|%i|%s|%f|%s|%s' % (logger.trans_count, elapsed, epoch,
                                                    self.user_group_name,
                                                    scriptrun_time, error,
                                                    repr(trans.custom_timers).replace(',', '--')))
            if self.console_logging:
                print(('%i| %.3f| %i| %s| %.3f| %s| %s' % (logger.trans_count, elapsed, epoch,
                                                           self.user_group_name, scriptrun_time,
                                                           error, repr(trans.custom_timers).replace(',', '--'))))


class UserGroup(object):
    """
    This class represent an user group
    Does not actually run anything

    :param process_num: the id of the process
    :param thread_num: the id of the thread
    :param script_file: the path of the tested script
    :param run_time: the time to run
    :param rampup: rampup property in seconds
    :param group_name: the name of the virtual user group
    :param queue: the queue for child threads
    """
    def __init__(self, *args, **kwargs):
        self.start_time = time.time()
        self.process_num = kwargs.pop('process_num', None)
        self.thread_num = kwargs.pop('thread_num', None)
        self.script_file = kwargs.pop('script_file', None)
        self.run_time = kwargs.pop('run_time', None)
        self.rampup = kwargs.pop('rampup', None)
        self.group_name = kwargs.pop('group_name', None)
        self.output_dir = kwargs.pop('output_dir', None)
        self.console_logging = kwargs.pop('console_logging', None)


@app.task
def run_ug(user_group):
    """
    Main celery task for running tests

    :param user_group: User group object containing all options
    :return: None
    """
    script_module = load_script(user_group.script_file)
    threads = []
    fh = logging.FileHandler(user_group.output_dir + 'results.csv')
    logger.addHandler(fh)
    for i in range(user_group.thread_num):
        space = float(user_group.rampup) / float(user_group.thread_num)
        if i > 0:
            time.sleep(space)
        agent_thread = Agent(user_group.process_num, i,
                             user_group.start_time, user_group.run_time,
                             user_group.group_name,
                             script_module, user_group.script_file,
                             user_group.console_logging)
        agent_thread.daemon = True
        threads.append(agent_thread)
        agent_thread.start()
    for agent_thread in threads:
        agent_thread.join()