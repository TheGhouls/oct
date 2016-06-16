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
import uuid
from datetime import datetime
from oct.results.output import output as output_results

import oct.results.stats_handler as stats_handler
from oct.utilities.configuration import configure
from oct.core.hq import HightQuarter


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

    topic = cmd_args.publisher_channel or uuid.uuid4().hex
    print("External publishing topic is %s" % topic)

    hq = HightQuarter(config.get('publish_port', 5000),
                      config.get('rc_port', 5001),
                      output_dir, config, topic)
    hq.wait_turrets(config.get("min_turrets", 1))
    hq.run()

    print('\nanalyzing results...\n')
    if output_results(output_dir, config):
        print('created: %sresults.html\n' % output_dir)

    project_config = os.path.join(cmd_args.project_dir, project_name, 'config.json')
    saved_config = os.path.join(output_dir, 'config.json')
    shutil.copy(project_config, saved_config)
    print('done.\n')


def run_command(sp):
    """
    Main function to run oct tests.
    """
    parser = sp.add_parser('run', help="run an oct project")
    parser.add_argument('project_name', help="The project directory")
    parser.add_argument('-r', '--results', dest='results_dir', help='results directory to reprocess')
    parser.add_argument('-d', '--directory', dest='project_dir', help='directory containing project folder',
                        default='.')
    parser.add_argument('-p', '--publisher-channel', dest='publisher_channel',
                        help='the channel for the external publisher',
                        default=None)
    parser.set_defaults(func=run)
