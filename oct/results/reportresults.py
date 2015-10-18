import six
import time
import json
import numpy as np
from collections import defaultdict
from oct.results.models import Result


def split_series(points, interval):
    offset = points[0][0]
    maxval = int((points[-1][0] - offset) // interval)
    vals = defaultdict(list)
    for key, value in points:
        vals[(key - offset) // interval].append(value)
    series = [vals[i] for i in range(maxval + 1)]
    return series


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Results(object):
    def __init__(self, results_file_name, run_time):
        self.results_file_name = results_file_name
        self.run_time = run_time
        self.total_transactions = 0
        self.total_errors = 0
        self.uniq_timer_names = set()
        self.uniq_user_group_names = set()

        self.resp_stats_list = self.__parse_file()

        if len(self.resp_stats_list) > 0:
            self.epoch_start = self.resp_stats_list[0].epoch_secs
            self.epoch_finish = self.resp_stats_list[-1].epoch_secs
            self.start_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.epoch_start))
            self.finish_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.epoch_finish))

    def __parse_file(self):
        # set_database(self.results_file_name, db)
        resp_stats_list = []
        for item in Result.select():
            if item.error:
                self.total_errors += 1
            self.total_transactions += 1
            if item.custom_timers:
                custom_timers = json.loads(item.custom_timers)
            else:
                custom_timers = {}
            for name, value in six.iteritems(custom_timers):
                self.uniq_timer_names.add(name)
            r = ResponseStats(item.elapsed, item.epoch, item.turret_name, item.scriptrun_time,
                              item.error, custom_timers)
            resp_stats_list.append(r)

        return resp_stats_list


class ResponseStats(object):
    def __init__(self, elapsed_time, epoch_secs, user_group_name, trans_time, error, custom_timers):
        self.elapsed_time = elapsed_time
        self.epoch_secs = epoch_secs
        self.user_group_name = user_group_name
        self.trans_time = trans_time
        self.error = error
        self.custom_timers = custom_timers


class IntervalDetailsResults(object):

    def __init__(self, trans_timer_points, interval_secs):
        self.avg_resptime_points = {}
        self.percentile_80 = {}
        self.percentile_90 = {}
        self.percentile_95 = {}
        self.max = {}
        self.min = {}
        self.avg = {}
        self.stdev = {}
        self.rate = {}
        self.count = {}
        self.interval = interval_secs
        self.interval_list = []
        self.splat_series = split_series(trans_timer_points, interval_secs)
        self.process()

    def process(self):
        for i, bucket in enumerate(self.splat_series):
            interval_start = int((i + 1) * self.interval)
            count = len(bucket)

            if count == 0:
                continue
            else:
                rate = count / float(self.interval)
                min_trans = min(bucket)
                max_trans = max(bucket)
                avg_trans = np.average(bucket)
                pct_80 = np.percentile(bucket, 80)
                pct_90 = np.percentile(bucket, 90)
                pct_95 = np.percentile(bucket, 95)
                stdev = np.std(bucket)

                self.avg_resptime_points[interval_start] = avg_trans
                self.percentile_80[interval_start] = pct_80
                self.percentile_90[interval_start] = pct_90
                self.percentile_95[interval_start] = pct_95
                self.max[interval_start] = max_trans
                self.min[interval_start] = min_trans
                self.stdev[interval_start] = stdev
                self.rate[interval_start] = rate
                self.count[interval_start] = count
                self.interval_list.append(interval_start)


class ReportResults(object):
    def __init__(self, results, interval_secs):
        self.all_results = {}
        self.results = results
        self.custom_timers = []
        self.interval = interval_secs

    def set_dict(self, trans_timer_points, trans_timer_vals, name=None):
        data = {
            'min_trans_val': np.average(trans_timer_vals),
            'average_trans_val': np.average(trans_timer_vals),
            'pct_80_trans_val': np.percentile(trans_timer_vals, 80),
            'pct_90_trans_val': np.percentile(trans_timer_vals, 90),
            'pct_95_trans_val': np.percentile(trans_timer_vals, 95),
            'max_trans_val': max(trans_timer_vals),
            'stdev_trans_val': np.std(trans_timer_vals),
            'interval_results': IntervalDetailsResults(trans_timer_points, self.interval),
            'throughput_points': {},
            'trans_timer_points': trans_timer_points,
            'trans_timer_vals': trans_timer_vals
        }

        for i, bucket in enumerate(data['interval_results'].splat_series):
            data['throughput_points'][int((i + 1) * self.interval)] = len(bucket) / self.interval

        if name is not None:
            data['name'] = name

        return data

    def set_all_transactions_results(self):
        resp_stats_list = self.results.resp_stats_list
        trans_timer_points = []
        trans_timer_vals = []
        for resp_stats in resp_stats_list:
            points = (resp_stats.elapsed_time, resp_stats.trans_time)
            trans_timer_points.append(points)
            trans_timer_vals.append(resp_stats.trans_time)

        self.all_results = self.set_dict(trans_timer_points, trans_timer_vals)

    def clear_all_transactions(self):
        del self.all_results

    def set_custom_timers(self):
        resp_stats_list = self.results.resp_stats_list
        for timer_name in sorted(self.results.uniq_timer_names):
            custom_timer_points = []
            custom_timer_vals = []
            for resp_stats in resp_stats_list:
                try:
                    val = resp_stats.custom_timers[timer_name]
                    custom_timer_points.append((resp_stats.elapsed_time, val))
                    custom_timer_vals.append(val)
                except KeyError:
                    pass  # the timer has never been used

            self.custom_timers.append(self.set_dict(custom_timer_points, custom_timer_vals, timer_name))
