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

WARNING_CONFIG_KEYS = [
    'hq_address',
    'publish_port',
    'rc_port'
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


def configure_for_turret(project_name, config_file):
    """Load the configuration file in python dict and check for keys that will be set to default value if not present

    :param project_name str: the name of the project
    :param config_file str: the path of the configuration file
    :return: the loaded configuration
    :rtype: dict
    """
    config = configure(project_name, None, config_file)
    for key in WARNING_CONFIG_KEYS:
        if key not in config:
            print("WARNING: %s configuration key not present, the value will be set to default value" % key)
    common_config = {
        'hq_address': config.get('hq_address', '127.0.0.1'),
        'hq_publisher': config.get('publish_port', 5000),
        'hq_rc': config.get('rc_port', 5001)
    }
    configs = []
    for turret in config['turrets']:
        turret.update(common_config)
        configs.append(turret)
    return configs
