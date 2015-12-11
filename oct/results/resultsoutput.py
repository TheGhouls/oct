import os
import time
from jinja2 import Environment, FileSystemLoader
from oct.multimechanize import graph
from oct.results.reportresults import Results, ReportResults
from oct.results.reportwriter import Report


def output(results_dir, results_file, config, parent='../../'):
    """Write the results output for the given test

    :param results_dir str: the directory for the results
    :param results_file str: the file for the results
    :param run_time int: the total test time elapsed
    :param rampup int: the rampup setting for the test
    :param ts_interval int: the interval in second setting for the test
    :param turrets: the turrets configuration
    :param parents str: the parent directory
    """
    start = time.time()
    results_dir = os.path.abspath(results_dir)
    results = Results(os.path.join(results_dir, results_file), config['run_time'])

    if len(results.resp_stats_list) == 0:
        print("No results, cannot create report")
        return False

    print('transactions: %i' % results.total_transactions)
    print('errors: %i' % results.total_errors)
    print('')
    print('test start: %s' % results.start_datetime)
    print('test finish: %s' % results.finish_datetime)
    print('')

    report_results = ReportResults(results, config['results_ts_interval'])
    report_results.set_all_transactions_results()

    data = {
        'report': report_results,
        'run_time': config['run_time'],
        'ts_interval': config['results_ts_interval'],
        'turrets_config': results.turrets,
        'all_results': report_results.all_results,
    }

    graph.resp_graph_raw(report_results.all_results['trans_timer_points'], 'All_Transactions_response_times.svg',
                         results_dir)
    graph.resp_graph(report_results.all_results['interval_results'].avg_resptime_points,
                     report_results.all_results['interval_results'].percentile_80,
                     report_results.all_results['interval_results'].percentile_90,
                     'All_Transactions_response_times_intervals.svg',
                     results_dir)
    graph.tp_graph(report_results.all_results['throughput_points'],
                   'All_Transactions_throughput.svg',
                   results_dir)

    report_results.clear_all_transactions()
    report_results.set_custom_timers()

    for timer in report_results.custom_timers:
        graph.resp_graph_raw(timer['trans_timer_points'], timer['name'] + '_response_times.svg', results_dir)
        graph.tp_graph(timer['throughput_points'], timer['name'] + '_throughput.svg', results_dir)
        graph.resp_graph(timer['interval_results'].avg_resptime_points,
                         timer['interval_results'].percentile_80,
                         timer['interval_results'].percentile_90,
                         timer['name'] + '_response_times_intervals.svg',
                         results_dir)

    # generate the jinja template
    j_env = Environment(loader=FileSystemLoader(os.path.join(results_dir, parent, 'templates')))
    template = j_env.get_template('report.html')

    report = Report(results_dir, parent)
    report.write_report(template.render(data))
    print("Report generated in {} seconds".format(time.time() - start))
    return True
