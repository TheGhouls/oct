import argparse
import json
import tarfile
import os.path
import tempfile
from jinja2 import Environment, PackageLoader

from oct.utilities.configuration import configure_for_turret


def main():
    parser = argparse.ArgumentParser(description='Give parameters for package a turret config_file and v_user')
    parser.add_argument('path', type=str, help='path for oct project dir')
    args = parser.parse_args()

    if os.path.exists(args.path):
        env = Environment(loader=PackageLoader('oct.utilities', 'templates'))
        turret_config = env.get_template('configuration/turret_config.json')
        turret_setup = env.get_template('scripts/setup.py')

        config_file = os.path.join(os.path.abspath(args.path),  "config.json")
        configs = configure_for_turret(args.path, config_file)

        for turret in configs:
            content = turret_config.render(turret)
            tmp_file = os.path.join(tempfile.gettempdir(), turret['name'] + ".json")
            tmp_setup = os.path.join(tempfile.gettempdir(), turret['name'] + ".py")
            turrets_requirements = turret.get('turrets_requirements', [])
            setup_file = turret_setup.render({'turrets_requirements': turrets_requirements, 'name': turret.get('name')})
            try:
                with open(tmp_file, 'w') as f:
                    f.write(content)
                with open(tmp_setup, 'w') as f:
                    f.write(setup_file)
                pack_turret(turret, tmp_file, tmp_setup, os.path.dirname(config_file))
                os.remove(tmp_file)
                os.remove(tmp_setup)
            except IOError as e:
                print("Error while packaging turret %s" % turret['name'])
                print("Error: %s" % e)
    else:
        parser.error("you need to enter a valid project path")


def pack_turret(turret_config, tmp_config_file, tmp_setup, base_config_path):
    """pack a turret into a tar file based on the turret configuration

    :param turret_config dict: the turret configuration to pack
    :param tmp_config_file str: the path of the temp config file
    :param base_config_path str: the base directory of the main configuration file
    """
    file_name = turret_config['name']
    tar_file = tarfile.open(file_name + ".tar", 'w')
    tar_file.add(os.path.abspath(tmp_config_file), arcname="config.json")
    tar_file.add(os.path.abspath(tmp_setup), arcname="setup.py")

    script_path = os.path.join(os.path.abspath(base_config_path), turret_config['script'])
    tar_file.add(script_path, arcname=turret_config['script'])
    for f in tar_file.getnames():
        print("Added %s" % f)
    tar_file.close()
    print("Archive %s created" % (file_name + ".tar"))
    print("=========================================")
