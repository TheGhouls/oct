import os
import sys
import json
from threading import Thread

from oct.results.models import Result, Turret, set_database, db


class ResultsWriter(Thread):
    """This class will handle results and stats comming from the turrets

    :param output_dir: the output directory for the results
    :type output_dir: str
    """
    def __init__(self, output_dir, config):
        Thread.__init__(self)
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

    def write_turret(self, datas):
        turret = Turret(name=datas['turret'], canons=datas['canons'], script=datas['script'], rampup=datas['rampup'],
                        uuid=datas['uuid'], status=datas['status'])
        turret.save()
        return turret

    def write_result(self, datas):
        self.trans_count += 1
        self.timer_count += len(datas['custom_timers'])
        if datas['error']:
            self.error_count += 1

        datas['custom_timers'] = json.dumps(datas['custom_timers'])
        self.results.append(datas)

        if len(self.results) >= 450:  # SQLite limit for inser_many is 500
            with db.atomic():
                Result.insert_many(self.results).execute()
            del self.results[:]

    def write_remaining(self):
        with db.atomic():
            Result.insert_many(self.results).execute()
        del self.results[:]
