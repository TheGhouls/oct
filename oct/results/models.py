import os
import json
import datetime

from playhouse.db_url import connect
from peewee import Proxy, TextField, FloatField, CharField, IntegerField, Model, DateTimeField

db = Proxy()


class Result(Model):
    """Define a result model
    """
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
    """Define a turret model
    """
    name = TextField()
    uuid = TextField()
    cannons = IntegerField()
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
            'cannons': self.cannons,
            'script': self.script,
            'rampup': self.rampup,
            'status': self.status,
            'updated_at': self.updated_at
        }

    class Meta:
        database = db


def set_database(db_url, proxy, config):
    """Initialize the peewee database with the given configuration

    If the given db_url is a regular file, it will be used as sqlite database

    :param str db_url: the connection string for database or path if sqlite file
    :param peewee.Proxy proxy: the peewee proxy to initialise
    :param dict config: the configuration dictionnary
    """
    db_config = config.get('results_database', {}).get('params', {})

    if 'testing' in config and config['testing'] is True:
        database = connect('sqlite:////tmp/results.sqlite', check_same_thread=False, threadlocals=True)
    else:
        if os.path.isfile(db_url) or os.path.isdir(os.path.dirname(db_url)):
            db_url = "sqlite:///" + db_url
            db_config.update(check_same_thread=False, threadlocals=True)
        database = connect(db_url, **db_config)
    proxy.initialize(database)
