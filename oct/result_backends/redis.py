import pandas as pd

from oct.core.exceptions import OctConfigurationError
from oct.result_backends.base import BaseStore, BaseLoader

try:
    import redis
    import msgpack
except ImportError:
    raise OctConfigurationError('Redis or msgpack not installed but required for this feature')


class RedisStore(BaseStore):
    """Default store for redis backend
    """
    def __init__(self, config, output_dir):
        super(RedisStore, self).__init__(config, output_dir)
        self.redis_config = self.config.get('results_backend', {}).get('backend_params', {})

        server_config = {
            'host': self.redis_config.get('host', 'localhost'),
            'port': self.redis_config.get('port', 6379),
            'db': self.redis_config.get('db', 0)
        }
        self.redis = redis.StrictRedis(**server_config)
        self.prefix = self.redis_config.get('key_prefix', 'oct')
        self.timers_key = "{}_{}".format(self.prefix, 'custom_timers')
        self.results_key = "{}_{}".format(self.prefix, 'results')
        self.turrets_key = "{}_{}".format(self.prefix, 'turrets')

        if self.redis_config.get('must_flush', False):
            self.redis.flushdb()

    def write_result(self, data):
        new_timers = {'epoch': data['epoch'], 'timers': data['custom_timers']}
        del data['custom_timers']

        self.redis.rpush(self.timers_key, msgpack.packb(new_timers))
        self.redis.rpush(self.results_key, msgpack.packb(data))

    def add_turret(self, data):
        key = "{}_{}".format(self.turrets_key, data.get('uuid'))
        self.redis.set(key, msgpack.packb(data))

    def update_turret(self, data):
        key = "{}_{}".format(self.turrets_key, data.get('uuid'))
        turret = self.redis.get(key)
        if turret:
            self.redis.set(key, msgpack.packb(data))


class RedisLoader(BaseLoader):
    """Default loader for redis backend
    """
    def __init__(self, config, output_dir):
        super(RedisLoader, self).__init__(config, output_dir)
        self.redis_config = self.config.get('results_backend', {}).get('backend_params', {})

        server_config = {
            'host': self.redis_config.get('host', 'localhost'),
            'port': self.redis_config.get('port', 6379),
            'db': self.redis_config.get('db', 0)
        }
        self.redis = redis.StrictRedis(**server_config)
        self.prefix = self.redis_config.get('key_prefix', 'oct')
        self.timers_key = "{}_{}".format(self.prefix, 'custom_timers')
        self.results_key = "{}_{}".format(self.prefix, 'results')
        self.turrets_key = "{}_{}".format(self.prefix, 'turrets')
        self._results_list = None

    @property
    def results_list(self):
        if self._results_list is None:
            res = [msgpack.unpackb(i, encoding='utf-8') for i in self.redis.lrange(self.results_key, 0, -1)]
            self._results_list = sorted(res, key=lambda k: k['epoch'])
        return self._results_list

    @property
    def total_errors(self):
        return len([i for i in self.results_list if i['error']])

    @property
    def epoch_start(self):
        if self.results_list:
            return self.results_list[0]['epoch']
        return 0

    @property
    def epoch_end(self):
        if self.results_list:
            return self.results_list[-1]['epoch']

    @property
    def results_dataframe(self):
        return pd.DataFrame(self.results_list)

    @property
    def custom_timers(self):
        for i in self.redis.lrange(self.timers_key, 0, -1):
            result = msgpack.unpackb(i, encoding='utf-8')
            yield result['epoch'], result['timers']

    @property
    def turrets(self):
        keys = self.redis.keys(self.turrets_key + '*')
        for k in keys:
            yield msgpack.unpackb(self.redis.get(k), encoding='utf-8')
