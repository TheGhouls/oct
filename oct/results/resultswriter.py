import os
import sys
import time
import json
from six.moves import queue
import threading
import sqlite3


class ResultsWriter(threading.Thread):
    """This class will handle results and stats comming from the turrets

    :param output_dir: the output directory for the results
    :type output_dir: str
    """
    def __init__(self, queue, output_dir):
        threading.Thread.__init__(self)
        self.output_dir = output_dir
        self.trans_count = 0
        self.timer_count = 0
        self.error_count = 0
        self.turret_name = 'Turret'
        self.results = []
        self.queue = queue

        try:
            os.makedirs(self.output_dir, 0o755)
        except OSError:
            sys.stderr.write("ERROR: Can not create output directory\n")
            sys.exit(1)

        self.conn = sqlite3.connect(self.output_dir + "results.sqlite", check_same_thread=False)
        self.conn.text_factory = str
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE results (error text, scriptrun_time real, elapsed real, epoch real,
            custom_timers text, turret_name text)
        ''')
        self.conn.commit()

    def write_result(self, datas):
        self.trans_count += 1
        self.timer_count += len(datas['custom_timers'])
        if datas['error']:
            self.error_count += 1
        self.cur.execute('''INSERT INTO results
            (error, scriptrun_time, elapsed, epoch, custom_timers, turret_name)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (datas['error'], datas['scriptrun_time'], datas['elapsed'], datas['epoch'], json.dumps(datas['custom_timers']), datas['turret_name']))
        self.conn.commit()

    def end_file(self):
        self.conn.close()

    def run(self):
        while True:
            try:
                elapsed, epoch, self.user_group_name, scriptrun_time, error, custom_timers = self.queue.get(False)
                datas = dict(elapsed=elapsed, epoch=epoch, turret_name=self.user_group_name,
                             scriptrun_time=scriptrun_time,
                             error=error, custom_timers=custom_timers)
                self.write_result(datas)
            except queue.Empty:
                time.sleep(.05)
