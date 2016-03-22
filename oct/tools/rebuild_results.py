import argparse

from oct.results.output import output
from oct.results.models import db, set_database
from oct.utilities.configuration import configure


def main():
    parser = argparse.ArgumentParser("Rebuild the html report from result dir")
    parser.add_argument('results_dir', help="The directory containing the results")
    parser.add_argument('results_file', help="The result file")
    parser.add_argument('config_file', help="The configuration file")

    args = parser.parse_args()

    config = configure(None, None, args.config_file)
    set_database(args.results_file, db, config)
    output(args.results_dir, config)
