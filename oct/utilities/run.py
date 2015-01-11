from __future__ import print_function
__author__ = 'manu'

from oct.multimechanize.core import init
from oct.multimechanize.results import output_results
from six.moves import configparser
from datetime import datetime
from oct.core.main import UserGroup, run_ug, app
from celery import group
import optparse
import sys
import os
import time
import shutil
import csv


class Configuration(object):
    """
    A simple configuration object. It just parses the command options and set its properties

    :param project_name: the name of the project
    :param cmd_opts: the parsed command options
    :param config_file: the configuration file to parse
    """
    def __init__(self, project_name, cmd_opts, config_file=None):
        self.user_group_configs = []
        self.config = configparser.ConfigParser()
        if config_file is None:
            config_file = '%s/%s/config.cfg' % (cmd_opts.projects_dir, project_name)
        self.config.read(config_file)
        for section in self.config.sections():
            if section == 'global':
                self.run_time = self.config.getint(section, 'run_time')
                self.rampup = self.config.getint(section, 'rampup')
                self.results_ts_interval = self.config.getint(section, 'results_ts_interval')
                try:
                    self.console_logging = self.config.getboolean(section, 'console_logging')
                except configparser.NoOptionError:
                    self.console_logging = False
                try:
                    self.progress_bar = self.config.getboolean(section, 'progress_bar')
                except configparser.NoOptionError:
                    self.progress_bar = True
                try:
                    results_database = self.config.get(section, 'results_database')
                    if results_database == 'None':
                        self.results_database = None
                except configparser.NoOptionError:
                    self.results_database = None
                try:
                    post_run_script = self.config.get(section, 'post_run_script')
                    if post_run_script == 'None':
                        self.post_run_script = None
                except configparser.NoOptionError:
                    self.post_run_script = None
                try:
                    self.xml_report = self.config.getboolean(section, 'xml_report')
                except configparser.NoOptionError:
                    self.xml_report = False
            else:
                self.threads = self.config.getint(section, 'threads')
                self.script = self.config.get(section, 'script')
                self.user_group_name = section
                self.ug_config = UserGroupConfig(self.threads, self.user_group_name, self.script)
                self.user_group_configs.append(self.ug_config)


class UserGroupConfig(object):
    """
    A simple object representing the configuration for an user group


    :param num_threads: the number of threads inside the user_group
    :param name: the name of the group
    :param script_file: the path to the script file of the group
    """
    def __init__(self, num_threads, name, script_file):
        self.num_threads = num_threads
        self.name = name
        self.script_file = script_file


def main():
    """
    Lunch the test from command line

    :return: None
    """

    usage = 'Usage: %prog <project name> [options]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-r', '--results', dest='results_dir', help='results directory to reprocess')
    parser.add_option('-d', '--directory', dest='projects_dir', help='directory containing project folder', default='.')
    cmd_opts, args = parser.parse_args()

    try:
        project_name = args[0]
    except IndexError:
        sys.stderr.write('\nERROR: no project specified\n\n')
        sys.stderr.write('%s\n' % usage)
        sys.stderr.write('Example: multimech-run my_project\n\n')
        sys.exit(1)

    init(cmd_opts.projects_dir, project_name)

    # -- ORIGINAL-MAIN:
    if cmd_opts.results_dir:  # don't run a test, just re-process results
        rerun_results(project_name, cmd_opts, cmd_opts.results_dir)
    else:
        run_test(project_name, cmd_opts)
    return


def rerun_results(project_name, cmd_opts, results_dir):
    """
    In case csv file is generated but graphics aren't

    :param project_name: the name of the project
    :param cmd_opts: the parsed commands
    :param results_dir: the result dir
    :return:
    """
    output_dir = '%s/%s/results/%s/' % (cmd_opts.projects_dir, project_name, results_dir)
    saved_config = '%s/config.cfg' % output_dir
    config = Configuration(project_name, cmd_opts, config_file=saved_config)
    print('\n\nanalyzing results...\n')
    output_results(output_dir, 'results.csv', config.run_time, config.rampup, config.results_ts_interval,
                   config.user_group_configs,
                   config.xml_report)
    print('created: %sresults.html\n' % output_dir)
    if config.xml_report:
        print('created: %sresults.jtl' % output_dir)
        print('created: last_results.jtl\n')


def run_test(project_name, cmd_opts):
    """
    Main run function, will run all the tests.

    :param project_name: the name of the project
    :param cmd_opts: all parsed commands
    :return: None
    """
    config = Configuration(project_name, cmd_opts)

    run_localtime = time.localtime()
    milisecond = datetime.now().microsecond
    output_dir = '%s/%s/results/results_%s' % (cmd_opts.projects_dir, project_name,
                                               time.strftime('%Y.%m.%d_%H.%M.%S_'+str(milisecond)+'/', run_localtime))

    try:
        os.makedirs(output_dir, 0o755)
    except OSError:
        sys.stderr.write('ERROR: Can not create output directory\n')
        sys.exit(1)

    script_prefix = os.path.join(cmd_opts.projects_dir, project_name, "test_scripts")
    script_prefix = os.path.normpath(script_prefix)

    user_groups = []
    threads = 0
    for i, ug_config in enumerate(config.user_group_configs):
        script_file = os.path.join(script_prefix, ug_config.script_file)
        ug = UserGroup(process_num=i, group_name=ug_config.name, thread_num=ug_config.num_threads,
                       script_file=script_file, output_dir=output_dir,
                       run_time=config.run_time, rampup=config.rampup, console_logging=config.console_logging)
        user_groups.append(ug)
        threads += ug_config.num_threads

    res = group(run_ug.s(ug) for ug in user_groups)()

    if config.console_logging:
        res.get(timeout=config.run_time + 5)
    else:
        print('\nuser_groups: {0}'.format(len(user_groups)), end='')
        print('\tthreads: {0}'.format(threads))

        st = 0
        while not res.ready():
            try:
                with open(output_dir + 'results.csv') as f:
                    r = csv.reader(f, delimiter='|')
                    rows = [row for row in r]
                    row_count = len(rows)
                    errors = sum(1 for row in rows if row[4] != '')
                    print('time : {0}/{1} seconds transactions: {2} errors : {3}'.format(
                        st, config.run_time, row_count, errors), end='\r')
                time.sleep(1)
                st += 1
            except KeyboardInterrupt:
                # purge all tasks in case of user interruption
                print('\nPurging all tasks...')
                app.control.purge()
                # revoke all tasks in case of KeyBoardInterrupt
                res.revoke(terminate=True)
                sys.exit(1)
            except EnvironmentError:
                if st <= 1:
                    # pass if we just start the test and the worker need a warmup
                    pass

    # all celery tasks are done at this point
    print('\n\nanalyzing results...\n')
    output_results(output_dir, 'results.csv', config.run_time, config.rampup,
                   config.results_ts_interval, config.user_group_configs,
                   config.xml_report)
    print('created: %sresults.html\n' % output_dir)

    # copy config file to results directory
    project_config = os.sep.join([cmd_opts.projects_dir, project_name, 'config.cfg'])
    saved_config = os.sep.join([output_dir, 'config.cfg'])
    shutil.copy(project_config, saved_config)

    print('done.\n')

    return
