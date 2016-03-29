import six
import time
import json
import pandas as pd
from collections import defaultdict

from oct.results.models import db, Result, Turret


class ReportResults(object):
    """Represent a report containing all tests results

    :param int run_time: the run_time of the script
    :param int interval: the time interval between each group of results
    """
    def __init__(self, run_time, interval):
        self.total_transactions = 0
        self.total_errors = Result.select(Result.id).where(Result.error != "", Result.error != None).count()
        self.total_timers = 0
        self.timers_results = {}
        self._timers_values = defaultdict(list)
        self.turrets = []
        self.main_results = {}
        self.interval = interval

        self._init_turrets()

    def _init_dates(self):
        """Initialize all dates properties
        """
        if self.total_transactions == 0:
            return None
        self.epoch_start = Result.select(Result.epoch).order_by(Result.epoch.asc()).limit(1).get().epoch
        self.epoch_finish = Result.select(Result.epoch).order_by(Result.epoch.desc()).limit(1).get().epoch
        self.start_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.epoch_start))
        self.finish_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.epoch_finish))

    def _init_dataframes(self):
        """Initialise the main dataframe for the results and the custom timers dataframes
        """
        df = pd.read_sql_query("SELECT elapsed, epoch, scriptrun_time FROM result ORDER BY epoch ASC", db.get_conn())
        self.main_results = self._get_processed_dataframe(df)

        # create all custom timers dataframes
        for key, value in six.iteritems(self._timers_values):
            df = pd.DataFrame(value, columns=['epoch', 'scriptrun_time'])
            df.index = pd.to_datetime(df['epoch'], unit='s')
            timer_results = self._get_processed_dataframe(df)
            self.timers_results[key] = timer_results

    def _get_all_timers(self):
        """Get all timers and set them in the _timers_values property
        """
        query = Result.select(Result.custom_timers, Result.epoch).order_by(Result.epoch.asc())
        for item in query:
            custom_timers = {}
            if item.custom_timers:
                custom_timers = json.loads(item.custom_timers)
            for key, value in six.iteritems(custom_timers):
                self._timers_values[key].append((item.epoch, value))
                self.total_timers += 1

    def _get_processed_dataframe(self, dataframe):
        """Generate required dataframe for results from raw dataframe

        :param pandas.DataFrame dataframe: the raw dataframe
        :return: a dict containing raw, compiled, and summary dataframes from original dataframe
        :rtype: dict
        """
        dataframe.index = pd.to_datetime(dataframe['epoch'], unit='s', utc=True)
        del dataframe['epoch']
        summary = dataframe.describe(percentiles=[.80, .90, .95]).transpose().loc['scriptrun_time']
        df_grp = dataframe.groupby(pd.TimeGrouper('{}S'.format(self.interval)))
        df_final = df_grp.apply(lambda x: x.describe(percentiles=[.80, .90, .95])['scriptrun_time']).unstack()

        return {
            "raw": dataframe.round(2),
            "compiled": df_final.round(2),
            "summary": summary.round(2)
        }

    def _init_turrets(self):
        """Setup data from database
        """
        for turret in Turret.select():
            self.turrets.append(turret.to_dict())

    def compile_results(self):
        """Compile all results for the current test
        """
        self._get_all_timers()
        self._init_dataframes()

        self.total_transactions = len(self.main_results['raw'])
        self._init_dates()
