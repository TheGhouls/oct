import argparse
import json
import tarfile
import os.path
from oct_turrets.utils import is_valid_conf


def main():
    parser = argparse.ArgumentParser(description='Give parameters for package a turret config_file and v_user')
    parser.add_argument('oct_project_path', type=str, default='', help='path for oct project dir')
    args = parser.parse_args()
    path = args.oct_project_path

    if os.path.exists(path):
        config_file_path = os.path.abspath(path) + "/config.json"
        tar_path = tar_me(config_file_path, path)
    else:
        print("you need to enter a valid path")


def tar_me(config_file, dir_path):
    conf_file = 0
    if os.path.isfile(config_file):
        with open(config_file) as f:
            conf_file = f.read()

    json_parsed = json.loads(conf_file)
    turrets = json_parsed['turrets']

    for turret in turrets:
        # if is_valid_conf(turret):
        if True:
            tar_file_name = turret['name']
            tar_file = tarfile.open(tar_file_name+".tar", 'w')
            tar_file.add(os.path.abspath(config_file), arcname="config.json")
            test_dir = os.path.dirname(os.path.abspath(config_file))
            tar_file.add(os.path.join(test_dir, turret['script']), arcname=os.path.basename(turret['script']))
            for f in tar_file.getnames():
                print("Added %s" % f)
            print("tar file is: %s" % dir_path+tar_file_name+".tar")
            tar_file.close()
