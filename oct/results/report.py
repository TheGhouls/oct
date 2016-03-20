import six
import time
import json
import pandas as pd

from oct.results.models import db, Result, Turret


class ReportResults(object):
    """Represent a report containing all tests results

    :param result_file str: the sqlite result file
    :param run_time int: the run_time of the script
    """
    def __init__(self, results_file, run_time, interval):
        self.results_file = results_file
        self.total_transactions = Result.select().count()
        self.total_errors = Result.select().where(Result.error != "", Result.error != None).count()
        self.timers_df = {}
        self.timers_values = {}
        self.turrets = []
        self.main_df = None
        self.summary = None
        self.interval = interval

        if self.total_transactions > 0:
            self.epoch_start = Result.select().order_by(Result.epoch.asc()).get().epoch
            self.epoch_finish = Result.select().order_by(Result.epoch.desc()).get().epoch
            self.start_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.epoch_start))
            self.finish_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.epoch_finish))

        self._get_all_timers()
        self._init_dataframes()

    def _init_dataframes(self):
        """Initialise the main dataframe for the results and the custom timers dataframes
        """
        df = pd.read_sql_query("SELECT elapsed, epoch, scriptrun_time FROM result ORDER BY epoch ASC", db.get_conn())
        self.summary = df.describe(percentiles=[.80, .90, .95]).transpose().loc['scriptrun_time']
        self.main_df = self._get_processed_dataframe(df)

        for key, value in six.iteritems(self.timers_values):
            df = pd.DataFrame(columns=['epoch', 'scriptrun_time'])
            for t in value:
                df = df.append({'epoch': t[0], 'scriptrun_time': t[1]}, ignore_index=True)
            df.index = pd.to_datetime(df['epoch'], unit='s')
            df = self._get_processed_dataframe(df)
            self.timers_df[key] = df

    def _get_all_timers(self):
        for item in Result.select(Result.custom_timers, Result.epoch).order_by(Result.epoch.asc()):
            custom_timers = {}
            if item.custom_timers:
                custom_timers = json.loads(item.custom_timers)
            for key, value in six.iteritems(custom_timers):
                self._process_timer(key, value, item.epoch)

    def _process_timer(self, name, value, epoch):
        """Add a custom timer to class dict. If key exists append the value, else create the key in dict

        :param name str: the name of the timer
        :param value float: the value of the timer
        :param epoch int: the epoch of timer
        """
        if self.timers_values.get(name):
            self.timers_values[name].append((epoch, value))
        else:
            self.timers_values[name] = [(epoch, value)]

    def _get_processed_dataframe(self, dataframe):
        """Generate required dataframe for results from raw dataframe

        :param dataframe pandas.DataFrame: the raw dataframe
        :return: a dataframe containing compiled results
        :rtype: pandas.DataFrame
        """
        dataframe.index = pd.to_datetime(dataframe['epoch'], unit='s')
        df_grp = dataframe.groupby(pd.TimeGrouper(str(self.interval) + 'S'))
        return df_grp.apply(lambda x: x.describe(percentiles=[.80, .90, .95])['scriptrun_time']).unstack().round(2)

    def _init_data(self):
        """Setup data from database
        """
        for turret in Turret.select():
            self.turrets.append(turret.to_dict())
