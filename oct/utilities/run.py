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


def process_results(output_dir, config):
    """Process results and output them
    """
    print('\nanalyzing results...\n')
    res = output_results(output_dir, config)
    if res:
        print('created: %s/results.html\n' % output_dir)
    else:
        print('results cannot be processed')


def copy_config(project_path, output_dir):
    """Copy current config file to output directory
    """
    project_config = os.path.join(project_path, 'config.json')
    saved_config = os.path.join(output_dir, 'config.json')
    shutil.copy(project_config, saved_config)


def start_hq(output_dir, config, topic, is_master=True, **kwargs):
    """Start a HQ
    """
    hq = HightQuarter(output_dir, config, topic, **kwargs)
    if is_master:
        hq.wait_turrets(config.get("min_turrets", 1))
    hq.run()


def generate_output_path(args, project_path):
    """Generate default output directory
    """
    milisec = datetime.now().microsecond
    dirname = 'results_{}_{}'.format(time.strftime('%Y.%m.%d_%H.%M.%S', time.localtime()), str(milisec))
    return os.path.join(project_path, 'results', dirname)


def run(args):
    """Start an oct project

    :param Namespace args: the commande-line arguments
    """
    kwargs = vars(args)

    if 'func' in kwargs:
        del kwargs['func']

    project_path = kwargs.pop('project_path')
    config = configure(project_path)

    output_dir = kwargs.pop('output_dir', None) or generate_output_path(args, project_path)

    stats_handler.init_stats(output_dir, config)

    topic = args.publisher_channel or uuid.uuid4().hex
    print("External publishing topic is %s" % topic)

    start_hq(output_dir, config, topic, **kwargs)

    if not args.no_results:
        process_results(output_dir, config)

    copy_config(project_path, output_dir)
    print('done.\n')


def run_command(sp):
    """
    Main function to run oct tests.
    """
    parser = sp.add_parser('run', help="run an oct project")
    parser.add_argument('project_path', help="The project directory")
    parser.add_argument('-p', '--publisher-channel', dest='publisher_channel',
                        help='the channel for the external publisher',
                        default=None)
    parser.add_argument('--no-results', action='store_true',
                        help="if set, html report and graphs will not be generated")
    parser.add_argument('-o', '--output-dir', help="output directory for test results")
    parser.add_argument('--with-forwarder', action='store_true',
                        help="Set if HQ should connect to external forwarder")
    parser.add_argument('--forwarder-address',
                        help="with form ip:port. If not set and --with-forwarder flag present HQ will use default values")
    parser.set_defaults(func=run)
