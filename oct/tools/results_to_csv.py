import os
import six
import csv

from oct.results.models import db, Result, set_database


def to_csv(args):
    """Take a sqlite filled database of results and return a csv file

    :param str result_file: the path of the sqlite database
    :param str output_file: the path of the csv output file
    :param str delimiter: the desired delimiter for the output csv file
    """
    result_file = args.result_file
    output_file = args.output_file
    delimiter = args.delimiter
    if not os.path.isfile(result_file):
        raise OSError("Results file does not exists")
    headers = ['elapsed', 'epoch', 'turret_name', 'scriptrun_time', 'error']
    headers_row = {}

    set_database(result_file, db, {})

    results = Result.select()

    for item in results:
        result_item = item.to_dict()
        for k in result_item['custom_timers'].keys():
            if k not in headers:
                headers.append(k)
                headers_row[k] = k

    with open(output_file, "w+") as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter=delimiter)
        headers_row.update({
            'elapsed': 'elapsed time',
            'epoch': 'epoch (in seconds)',
            'turret_name': 'turret name',
            'scriptrun_time': 'transaction time',
            'error': 'error'
        })
        writer.writerow(headers_row)
        for result_item in results:
            line = result_item.to_dict()
            for key, value in line['custom_timers'].items():
                line[key] = value
            del line['custom_timers']
            writer.writerow(line)


def results_to_csv(sp):
    if six.PY2:
        parser = sp.add_parser('results-to-csv', help="Create a csv file from a sqlite results file")
    else:
        parser = sp.add_parser('results-to-csv',
                               help="Create a csv file from a sqlite results file",
                               aliases=['to-csv'])
    parser.add_argument('result_file', help="The orignial result file")
    parser.add_argument('output_file', help="The output path for the csv file")
    parser.add_argument('-d', '--delimiter', type=str, help="The delimiter for the csv file", default=';')
    parser.set_defaults(func=to_csv)
