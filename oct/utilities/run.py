#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#  Copyright (c) 2010-2012 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize | Performance Test Framework
#
from __future__ import print_function
import os
import shutil
import time
from datetime import datetime
from oct.results.output import output as output_results

import oct.results.stats_handler as stats_handler
from oct.utilities.configuration import configure
from oct.core.hq import HightQuarter


def run_command(sp):
    """
    Main function to run oct tests.
    """
    parser = sp.add_parser('run', help="run an oct project")
    parser.add_argument('project_name', help="The project directory")
    parser.add_argument('-r', '--results', dest='results_dir', help='results directory to reprocess')
    parser.add_argument('-d', '--directory', dest='project_dir', help='directory containing project folder',
                        default='.')
    parser.set_defaults(func=run)


def run(cmd_args):
    """Start an oct project

    :param Namespace cmd_args: the commande-line arguments
    """
    project_name = cmd_args.project_name
    config = configure(project_name, cmd_args)

    run_localtime = time.localtime()
    milisec = datetime.now().microsecond
    output_dir = '%s/%s/results/results_%s' % (cmd_args.project_dir, project_name,
                                               time.strftime('%Y.%m.%d_%H.%M.%S_' + str(milisec) + '/', run_localtime))

    stats_handler.init_stats(output_dir, config)
    # rw = stats_handler.StatsHandler(output_dir, config)

    script_prefix = os.path.join(cmd_args.project_dir, project_name, "test_scripts")
    script_prefix = os.path.normpath(script_prefix)

    hq = HightQuarter(config.get('publish_port', 5000), config.get('rc_port', 5001), output_dir, config)
    hq.wait_turrets(config.get("min_turrets", 1))
    hq.run()

    print('\n\nanalyzing results...\n')
    if output_results(output_dir, config):
        print('created: %sresults.html\n' % output_dir)

    # copy config file to results directory
    project_config = os.sep.join([cmd_args.project_dir, project_name, 'config.json'])
    saved_config = os.sep.join([output_dir, 'config.json'])
    shutil.copy(project_config, saved_config)

    print('done.\n')

    return
