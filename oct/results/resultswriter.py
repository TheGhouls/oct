import os
import sys
import time
import json
from six.moves import queue
import threading
import sqlite3
from oct.results.models import Result, set_database, db


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

        set_database(self.output_dir + "results.sqlite", db)
        db.connect(check_same_thread=False)
        db.create_tables([Result])

    def write_result(self, datas):
        self.trans_count += 1
        self.timer_count += len(datas['custom_timers'])
        if datas['error']:
            self.error_count += 1

        result = Result(error = datas['error'], script_runtime = datas['scriptrun_time'],elapsed = datas['elapsed'], epoch = datas['epoch'],
                        custom_timer = json.dumps(datas['custom_timers']),turrent_name = datas['turret_name'])
        result.save()

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
