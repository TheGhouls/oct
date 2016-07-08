import os
import ujson

from oct.utilities.configuration import get_db_uri
from oct.results.models import Result, Turret, set_database, db


def init_stats(output_dir, config):
    """Init all required ressources for stats handling
    :param str output_dir: the output directory for the results
    :param dict config: the project configuration
    """

    try:
        os.makedirs(output_dir, 0o755)
    except OSError as e:
        print("ERROR: Can not create output directory: %s\n" % e)
        raise

    db_uri = get_db_uri(config, output_dir)

    set_database(db_uri, db, config)

    tables_to_create = [t for t in [Result, Turret] if not t.table_exists()]

    db.connect()
    db.create_tables(tables_to_create)


class StatsHandler(object):
    """This class will handle results and stats comming from the turrets"""
    def __init__(self):
        self.results = []

    def write_result(self, data):
        """Write the results received to the database
        :param dict data: the data to save in database
        :return: None
        """
        data['custom_timers'] = ujson.dumps(data['custom_timers'])
        self.results.append(data)

        if len(self.results) >= 490:  # SQLite limit for inser_many is 500
            with db.execution_context():
                with db.atomic():
                    Result.insert_many(self.results).execute()
                del self.results[:]

    def write_remaining(self):
        """Write the remaning stack content
        """
        if not self.results:
            return
        with db.execution_context():
            with db.atomic():
                Result.insert_many(self.results).execute()
        del self.results[:]
