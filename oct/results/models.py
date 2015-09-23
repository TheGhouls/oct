from peewee import *

db = Proxy()

class Result(Model):
    error = TextField()
    script_runtime = FloatField()
    elapsed = FloatField()
    epoch = FloatField()
    custom_timer = TextField()
    turret_name = CharField()

    class Meta:
        database = db

def set_database(db_path, proxy):
    database = SqliteDatabase(db_path)
    proxy.initialize(database)
