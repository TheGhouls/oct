from __future__ import print_function
import argparse

from oct.utilities.newproject import new_project
from oct.utilities.pack import pack_turrets
from oct.utilities.run import run_command
from oct.utilities.run_device import run_device_command
from oct.tools.rebuild_results import rebuild_results
from oct.tools.results_to_csv import results_to_csv
from oct.tools.from_armory import from_armory


PARSERS = [
    new_project,
    pack_turrets,
    run_command,
    rebuild_results,
    results_to_csv,
    run_device_command,
    from_armory
]


def build_parser():
    parser = argparse.ArgumentParser(prog='oct')
    subparsers = parser.add_subparsers(help='sub commands availables', dest='parser')
    subparsers.required = True

    for p in PARSERS:
        p(subparsers)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
