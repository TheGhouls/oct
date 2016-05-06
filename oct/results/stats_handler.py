import os
import json

from oct.results.models import Result, Turret, set_database, db


def init_stats(output_dir, config):
    """Init all required ressources for stats handling

    :param str output_dir: the output directory for the results
    :param dict config: the project configuration
    """

    try:
        os.makedirs(output_dir, 0o755)
    except OSError:
        print("ERROR: Can not create output directory\n")
        raise

    set_database(output_dir + "results.sqlite", db, config)
    db.connect()
    db.create_tables([Result, Turret])


class StatsHandler(object):
    """This class will handle results and stats comming from the turrets

    :param str output_dir: the output directory for the results
    """
    def __init__(self, output_dir, config):
        self.output_dir = output_dir
        self.trans_count = 0
        self.timer_count = 0
        self.error_count = 0
        self.turret_name = 'Turret'
        self.results = []

    def write_result(self, data):
        """Write the results received to the database

        :param dict data: the data to save in database
        :return: None
        """
        print(data)
        self.trans_count += 1
        self.timer_count += len(data['custom_timers'])
        if data['error']:
            self.error_count += 1

        data['custom_timers'] = json.dumps(data['custom_timers'])
        self.results.append(data)

        if len(self.results) >= 450:  # SQLite limit for inser_many is 500
            with db.execution_context():
                with db.atomic():
                    Result.insert_many(self.results).execute()
                del self.results[:]

    def write_remaining(self):
        """Write the remaning stack content
        """
        with db.atomic():
            Result.insert_many(self.results).execute()
        del self.results[:]
