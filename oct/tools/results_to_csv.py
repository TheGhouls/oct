import csv
import json
import argparse


def results_to_csv(result_file, output_file, delimiter=';'):
    with open(result_file, 'r') as f:
        json_data = json.load(f)
    headers = ['elapsed', 'epoch', 'turret_name', 'scriptrun_time', 'error']
    headers_row = {}

    for item in json_data:
        for k in item['custom_timers'].keys():
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
        for item in json_data:
            timers = item['custom_timers']
            del item['custom_timers']
            item.update(timers)
            writer.writerow(item)


def main():
    parser = argparse.ArgumentParser("Create a csv file from a json results file")
    parser.add_argument('result_file', help="The orignial result file")
    parser.add_argument('output_file', help="The output path for the csv file")
    parser.add_argument('-d', '--delimiter', type=str, help="The delimiter for the csv file", default=';')
    args = parser.parse_args()

    results_to_csv(args.result_file, args.output_file, args.delimiter)
