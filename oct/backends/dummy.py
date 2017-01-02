import pandas as pd

from oct.backends.base import BaseStore, BaseLoader


class DummyStore(BaseStore):
    """Store that do noting at all
    """
    def write_result(self, data):
        del data

    def add_turret(self, data):
        del data

    def update_turret(self, data):
        del data


class DummyLoader(BaseLoader):
    """Loader that do nothing at all
    """

    @property
    def total_errors(self):
        return 0

    @property
    def epoch_start(self):
        return None

    @property
    def epoch_end(self):
        return None

    @property
    def results_dataframe(self):
        return pd.DataFrame()

    @property
    def custom_timers(self):
        return []

    @property
    def turrets(self):
        return []
