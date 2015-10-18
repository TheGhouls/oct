#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#  Copyright (c) 2010-2012 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize | Performance Test Framework
#
from __future__ import print_function
import multiprocessing
import optparse
import os
# -- NOT-NEEDED: import Queue
import shutil
import sys
import time
from datetime import datetime
from oct.results.resultsoutput import output as output_results


import oct.multimechanize.core as core
import oct.results.resultswriter as resultswriter
import oct.multimechanize.progressbar as progressbar
from oct.multimechanize import __version__ as version
from oct.utilities.configuration import configure
from oct.core.hq import HightQuarter


def main():
    """
    Main function to run multimechanize benchmark/performance test.
    """

    usage = 'Usage: %prog <project name> [options]'
    parser = optparse.OptionParser(usage=usage, version=version)
    parser.add_option('-p', '--port', dest='port', type='int', help='rpc listener port')
    parser.add_option('-r', '--results', dest='results_dir', help='results directory to reprocess')
    parser.add_option('-b', '--bind-addr', dest='bind_addr', help='rpc bind address', default='localhost')
    parser.add_option('-d', '--directory', dest='projects_dir', help='directory containing project folder', default='.')
    cmd_opts, args = parser.parse_args()

    try:
        project_name = args[0]
    except IndexError:
        sys.stderr.write('\nERROR: no project specified\n\n')
        sys.stderr.write('%s\n' % usage)
        sys.stderr.write('Example: multimech-run my_project\n\n')
        sys.exit(1)

    core.init(cmd_opts.projects_dir, project_name)

    # -- ORIGINAL-MAIN:
    if cmd_opts.results_dir:  # don't run a test, just re-process results
        rerun_results(project_name, cmd_opts, cmd_opts.results_dir)
    else:
        run(project_name, cmd_opts)
    return


def run(project_name, cmd_opts, remote_starter=None):
    if remote_starter is not None:
        remote_starter.test_running = True
        remote_starter.output_dir = None

    config = configure(project_name, cmd_opts)

    run_localtime = time.localtime()
    milisec = datetime.now().microsecond
    output_dir = '%s/%s/results/results_%s' % (cmd_opts.projects_dir, project_name,
                                               time.strftime('%Y.%m.%d_%H.%M.%S_'+str(milisec)+'/', run_localtime))

    # this queue is shared between all processes/threads
    rw = resultswriter.ResultsWriter(output_dir, config)

    script_prefix = os.path.join(cmd_opts.projects_dir, project_name, "test_scripts")
    script_prefix = os.path.normpath(script_prefix)

    hq = HightQuarter(config.get('publish_port', 5000), config.get('rc_port', 5001), rw, config)
    hq.run()

    # all agents are done running at this point
    time.sleep(.2)  # make sure the writer queue is flushed
    print('\n\nanalyzing results...\n')
    if output_results(output_dir, 'results.sqlite', config):
        print('created: %sresults.html\n' % output_dir)

    # copy config file to results directory
    project_config = os.sep.join([cmd_opts.projects_dir, project_name, 'config.json'])
    saved_config = os.sep.join([output_dir, 'config.json'])
    shutil.copy(project_config, saved_config)

    print('done.\n')

    if remote_starter is not None:
        remote_starter.test_running = False
        remote_starter.output_dir = output_dir

    return


def rerun_results(project_name, cmd_opts, results_dir):
    output_dir = '%s/%s/results/%s/' % (cmd_opts.projects_dir, project_name, results_dir)
    saved_config = '%s/config.cfg' % output_dir
    (run_time, rampup, results_ts_interval, console_logging, progress_bar, results_database,
     post_run_script, xml_report, user_group_configs) = configure(project_name, cmd_opts, config_file=saved_config)
    print('\n\nanalyzing results...\n')
    # results.output_results(output_dir, 'results.csv', run_time, rampup, results_ts_interval, user_group_configs,
    #                       xml_report)
    print('created: %sresults.html\n' % output_dir)
    if xml_report:
        print('created: %sresults.jtl' % output_dir)
        print('created: last_results.jtl\n')


class UserGroupConfig(object):
    def __init__(self, num_threads, name, script_file):
        self.num_threads = num_threads
        self.name = name
        self.script_file = script_file


if __name__ == '__main__':
    main()
