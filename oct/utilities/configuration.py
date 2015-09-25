import os
import json

from oct.core.exceptions import OctConfigurationError


REQUIRED_CONFIG_KEYS = [
    'run_time',
    'results_ts_interval',
    'testing',
    'progress_bar',
    'turrets'
]


def configure(project_name, cmd_opts, config_file=None):
    """Get the configuration of the test and return it as a config object

    :return: the configured config object
    :rtype: Object
    """
    if config_file is None:
        config_file = os.path.join(cmd_opts.projects_dir, project_name, 'config.json')
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except ValueError as e:
        raise OctConfigurationError("Configuration setting failed with error: %s" % e)
    for key in REQUIRED_CONFIG_KEYS:
        if key not in config:
            raise OctConfigurationError("Error: the required configuration key %s is not define" % key)
    return config
