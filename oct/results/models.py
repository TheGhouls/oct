import json
import datetime
from peewee import Proxy, TextField, FloatField, CharField, IntegerField, SqliteDatabase, Model, DateTimeField

db = Proxy()


class Result(Model):
    error = TextField(null=True)
    scriptrun_time = FloatField()
    elapsed = FloatField()
    epoch = FloatField()
    custom_timers = TextField(null=True)
    turret_name = CharField(default='Noname')

    def to_dict(self):
        return {
            'error': self.error,
            'scriptrun_time': self.scriptrun_time,
            'elapsed': self.elapsed,
            'epoch': self.epoch,
            'custom_timers': json.loads(self.custom_timers),
            'turret_name': self.turret_name
        }

    class Meta:
        database = db


class Turret(Model):
    name = TextField()
    uuid = TextField()
    canons = IntegerField()
    script = TextField()
    rampup = IntegerField()
    status = TextField()
    updated_at = DateTimeField(default=datetime.datetime.now())

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(Turret, self).save(*args, **kwargs)

    def to_dict(self):
        return {
            'name': self.name,
            'uuid': self.uuid,
            'canons': self.canons,
            'script': self.script,
            'rampup': self.rampup,
            'status': self.status,
            'updated_at': self.updated_at
        }

    class Meta:
        database = db


def set_database(db_path, proxy, config):
    """Initialize the peewee database with the given configuration

    :param db_path str: the path of the sqlite database
    :param proxy peewee.Proxy: the peewee proxy to initialise
    :param config dict: the configuration dictionnary
    """
    if 'testing' in config and config['testing'] is True:
        database = SqliteDatabase('/tmp/results.sqlite', check_same_thread=False)
    else:
        database = SqliteDatabase(db_path, check_same_thread=False)
    proxy.initialize(database)
