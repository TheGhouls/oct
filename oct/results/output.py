from __future__ import print_function

import os
import time
from jinja2 import Environment, FileSystemLoader

from oct.results import graphs
from oct.results.report import ReportResults
from oct.results.writer import ReportWriter


def generate_graphs(data, name, results_dir):
    """Generate all reports from original dataframe

    :param dic data: dict containing raw and compiled results dataframes
    :param str name: name for prefixing graphs output
    :param str results_dir: results output directory
    """
    graphs.resp_graph_raw(data['raw'], name + '_response_times.svg', results_dir)
    graphs.resp_graph(data['compiled'], name + '_response_times_intervals.svg', results_dir)
    graphs.tp_graph(data['compiled'], name + '_throughput.svg', results_dir)


def print_infos(results):
    """Print informations in standard output

    :param ReportResults results: the report result containing all compiled informations
    """
    print('transactions: %i' % results.total_transactions)
    print('timers: %i' % results.total_timers)
    print('errors: %i' % results.total_errors)
    print('test start: %s' % results.start_datetime)
    print('test finish: %s\n' % results.finish_datetime)


def write_template(data, results_dir, parent):
    """Write the html template

    :param dict data: the dict containing all data for output
    :param str results_dir: the ouput directory for results
    :param str parent: the parent directory
    """
    print("Generating html report...")
    partial = time.time()
    j_env = Environment(loader=FileSystemLoader(os.path.join(results_dir, parent, 'templates')))
    template = j_env.get_template('report.html')

    report_writer = ReportWriter(results_dir, parent)
    report_writer.write_report(template.render(data))
    print("HTML report generated in {} seconds\n".format(time.time() - partial))


def output(results_dir, config, parent='../../'):
    """Write the results output for the given test

    :param str results_dir: the directory for the results
    :param dict config: the configuration of the test
    :param str parents: the parent directory
    """
    start = time.time()
    print("Compiling results...")
    results_dir = os.path.abspath(results_dir)
    results = ReportResults(config['run_time'], config['results_ts_interval'])
    results.compile_results()
    print("Results compiled in {} seconds\n".format(time.time() - start))

    if results.total_transactions == 0:
        print("No results, cannot create report")
        return False

    print_infos(results)

    data = {
        'report': results,
        'run_time': config['run_time'],
        'ts_interval': config['results_ts_interval'],
        'turrets_config': results.turrets,
        'results': {"all": results.main_results, "timers": results.timers_results}
    }

    print("Generating graphs...")
    partial = time.time()
    generate_graphs(results.main_results, 'All_Transactions', results_dir)

    for key, value in results.timers_results.items():
        generate_graphs(value, key, results_dir)
    print("All graphs generated in {} seconds\n".format(time.time() - partial))

    write_template(data, results_dir, parent)
    print("Full report generated in {} seconds".format(time.time() - start))
    return True
