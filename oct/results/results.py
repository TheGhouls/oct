import time
import json


class Results(object):
    def __init__(self, results_file_name, run_time):
        self.results_file_name = results_file_name
        self.run_time = run_time
        self.total_transactions = 0
        self.total_errors = 0
        self.uniq_timer_names = set()
        self.uniq_user_group_names = set()

        self.resp_stats_list = self.__parse_file()

        self.epoch_start = self.resp_stats_list[0].epoch_secs
        self.epoch_finish = self.resp_stats_list[-1].epoch_secs
        self.start_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.epoch_start))
        self.finish_datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.epoch_finish))

    def __parse_file(self):
        with open(self.results_file_name, 'r') as f:
            datas = json.load(f)
        resp_stats_list = []
        for item in datas:
            if item['error']:
                self.total_errors += 1
            self.total_transactions += 1
            r = ResponseStats(item['elapsed'], item['epoch'], item['turret_name'], item['scriptrun_time'],
                              item['error'], item['custom_timers'])
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
