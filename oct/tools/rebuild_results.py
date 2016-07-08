import six
from oct.core.exceptions import OctConfigurationError

from oct.results.output import output
from oct.results.models import db, set_database
from oct.utilities.configuration import configure, get_db_uri


def rebuild(args):
    config = configure(None, args.config_file)

    if args.results_file is None:
        db_uri = get_db_uri(config, args.results_dir)
    else:
        db_uri = args.results_file

    if not db_uri:
        raise OctConfigurationError("Bad database configured, if you use sqlite database use -f option")

    set_database(db_uri, db, config)
    output(args.results_dir, config)


def rebuild_results(sp):
    if six.PY2:
        parser = sp.add_parser('rebuild-results', help="Rebuild the html report from result dir")
    else:
        parser = sp.add_parser('rebuild-results', help="Rebuild the html report from result dir", aliases=['rebuild'])
    parser.add_argument('results_dir', help="The directory containing the results")
    parser.add_argument('config_file', help="The configuration file")
    parser.add_argument('-f', '--results-file', help="The sqlite result file", default=None)
    parser.set_defaults(func=rebuild)
