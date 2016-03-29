import os
import sys
import json

from oct.results.models import Result, Turret, set_database, db


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

        try:
            os.makedirs(self.output_dir, 0o755)
        except OSError:
            sys.stderr.write("ERROR: Can not create output directory\n")
            sys.exit(1)

        set_database(self.output_dir + "results.sqlite", db, config)
        db.connect()
        db.create_tables([Result, Turret])

    def write_turret(self, data):
        """Write the turret information in database

        :param dict data: the data of the turret to save
        :return: The turret object after save
        """
        turret = Turret(name=data['turret'], canons=data['canons'], script=data['script'], rampup=data['rampup'],
                        uuid=data['uuid'], status=data['status'])
        turret.save()
        return turret

    def write_result(self, data):
        """Write the results received to the database

        :param dict data: the data to save in database
        :return: None
        """
        self.trans_count += 1
        self.timer_count += len(data['custom_timers'])
        if data['error']:
            self.error_count += 1

        data['custom_timers'] = json.dumps(data['custom_timers'])
        self.results.append(data)

        if len(self.results) >= 450:  # SQLite limit for inser_many is 500
            with db.atomic():
                Result.insert_many(self.results).execute()
            del self.results[:]

    def write_remaining(self):
        """Write the remaning stack content
        """
        with db.atomic():
            Result.insert_many(self.results).execute()
        del self.results[:]
