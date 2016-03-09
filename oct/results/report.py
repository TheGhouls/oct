import time
import pandas as pd

from oct.results.models import db, Result, Turret


class ReportResults(object):
    """Represent a report containing all tests results

    :param result_file str: the sqlite result file
    :param run_time int: the run_time of the script
    """
    def __init__(self, results_file, run_time):
        self.results_file = results_file
        self.total_transactions = Result.select().count()
        self.total_errors = Result.select().where(Result.error != "", Result.error != None).count()
        self.timers_df = {}
        self.turrets = []

        self.epoch_start = Result.order_by(Result.epoch.asc()).get().epoch
        self.epoch_finish = Result.select().order_by(Result.epoch.desc()).get().epoch
        self.start_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.epoch_start))
        self.finish_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.epoch_finish))

    def _init_data(self):
        """Setup data from database
        """
        for turret in Turret.select():
            self.turrets.append(turret.to_dict())

    def _timer_dataframe(self):
        """Create a dataframe for each action timer
        """
        pass
