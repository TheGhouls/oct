import ujson
import pandas as pd

from oct.utilities.configuration import get_db_uri
from oct.result_backends.base import BaseStore, BaseLoader
from oct.results.models import Result, Turret, set_database, db


class SQLiteStore(BaseStore):
    """Base class for defining how to store results for specific backend
    """
    def __init__(self, result_backend_config, output_dir):
        super(SQLiteStore, self).__init__(result_backend_config, output_dir)

        db_uri = get_db_uri(self.config, self.output_dir)
        set_database(db_uri, db, self.config)

        db.connect()

        Result.create_table(fail_silently=True)
        Turret.create_table(fail_silently=True)

        self.results = []
        self.insert_limit = 150
        self.turrets = {}

    def write_result(self, data):
        """Method called by HQ when data are received from turrets.

        This object is instanciated only one time on the HQ, so you can store multiple results in
        list to insert data by batch into store.

        :param dict data: data to save
        :return: None
        """
        data['custom_timers'] = ujson.dumps(data['custom_timers'])
        self.results.append(data)

        if len(self.results) >= 150:  # 150 rows for SQLite default limit
            with db.execution_context():
                with db.atomic():
                    Result.insert_many(self.results).execute()
                del self.results[:]

    def after_tests(self):
        """Called at the end of HQ main loop. Useful if have remaining elements to write

        Default to `pass` statement, override not mandatory
        """
        if not self.results:
            return
        with db.execution_context():
            with db.atomic():
                Result.insert_many(self.results).execute()
        del self.results[:]

    def add_turret(self, data):
        """Called when turret manager need to register a new turret.
        Since this method is called by turret manager, you can asume that data are correct and complete.

        :param dict data: turret data sent by turret manager
        """
        turret = Turret(**data)
        with db.execution_context():
            turret.save()

        self.turrets[turret.uuid] = turret

    def update_turret(self, data):
        """Called when a turret change status. Since this method is
        called by turret manager, you can asume that data are correct and complete.

        :param dict data: turret data sent by turret manager
        """
        turret = self.turrets.get(data['uuid'])
        if not turret:
            return

        turret.update(**data)
        with db.execution_context():
            turret.save()


class SQLiteLoader(BaseLoader):
    """Base class for retrieve results for a specific backend

    Mainly composed of properties. All properties returning more than one elements
    can use `yield` syntax
    """
    def __init__(self, config, output_dir):
        super(SQLiteLoader, self).__init__(config, output_dir)

        db_uri = get_db_uri(self.config, self.output_dir)
        set_database(db_uri, db, self.config)

        db.connect()

    @property
    def total_errors(self):
        return Result.select(Result.id)\
                     .where(Result.error != "", Result.error != None)\
                     .count()

    @property
    def epoch_start(self):
        return Result.select(Result.epoch).order_by(Result.epoch.asc()).limit(1).get().epoch

    @property
    def epoch_end(self):
        return Result.select(Result.epoch).order_by(Result.epoch.desc()).limit(1).get().epoch

    @property
    def results_dataframe(self):
        return pd.read_sql_query(
            "SELECT elapsed, epoch, scriptrun_time, custom_timers FROM result ORDER BY epoch ASC",
            db.get_conn()
        )

    @property
    def custom_timers(self):
        for item in Result.select(Result.custom_timers, Result.epoch).order_by(Result.epoch.asc()):
            yield item.epoch, ujson.loads(item.custom_timers)

    @property
    def turrets(self):
        for turret in Turret.select():
            yield turret.to_dict()
