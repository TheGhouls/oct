import sys
import six
import json
import tarfile
import os.path
import tempfile
from jinja2 import Environment, PackageLoader

from oct.utilities.configuration import configure_for_turret, cleanup_turret_config


def cleanup_temp_files(turret, files):
    for f in files:
        try:
            os.remove(f)
        except IOError as e:
            print("Error while packagin turret %s" % turret['name'])
            print("Error: %s" % e)


def write_temp_files(turret, files):
    writed_files = []
    for f in files:
        try:
            with open(f['filename'], 'w') as fd:
                fd.write(f['content'])
                writed_files.append(f['filename'])
        except IOError as e:
            print("Error while packaging turret %s" % turret['name'])
            print("Error: %s" % e)
    return writed_files


def get_files_and_content(turret, is_python=False):
    ret = []
    env = Environment(loader=PackageLoader('oct.utilities', 'templates'))
    turret_setup = env.get_template('scripts/setup.j2')

    if is_python:
        tmp_setup = os.path.join(tempfile.gettempdir(), "setup.py")
        turrets_requirements = turret.get('turrets_requirements', [])
        setup_file = turret_setup.render({'turrets_requirements': turrets_requirements,
                                         'name': turret.get('name')})
        ret.append({'filename': tmp_setup, 'content': setup_file})

    content = json.dumps(cleanup_turret_config(turret), indent=2)
    tmp_config = os.path.join(tempfile.gettempdir(), "config.json")
    ret.append({'filename': tmp_config, 'content': content})
    return ret


def pack_turret(turret, temp_files, base_config_path, path=None):
    """pack a turret into a tar file based on the turret configuration

    :param dict turret_config: the turret configuration to pack
    :param str tmp_config_file: the path of the temp config file
    :param str base_config_path: the base directory of the main configuration file
    """
    file_name = turret['name']
    files = temp_files[:]
    for fname in turret.get('extra_files', []):
        if os.path.isabs(fname) or path is None:
            files.append(fname)
        else:
            files.append(os.path.join(path, fname))
    if path is not None:
        file_name = os.path.join(path, file_name)
    tar_file = tarfile.open(file_name + ".tar.gz", 'w:gz')

    for f in files:
        tar_file.add(os.path.abspath(f), arcname=os.path.basename(f))

    script_path = os.path.join(os.path.abspath(base_config_path), turret['script'])
    tar_file.add(script_path, arcname=turret['script'])

    for f in tar_file.getnames():
        print("Added %s" % f)
    tar_file.close()
    print("Archive %s created" % (tar_file.name))
    print("=========================================")


def pack(args):
    if os.path.exists(args.path):
        config_file = os.path.join(os.path.abspath(args.path), "config.json")
        configs = configure_for_turret(args.path, config_file)

        for turret in configs:
            files = get_files_and_content(turret, args.python)
            temp_files = write_temp_files(turret, files)
            pack_turret(turret, temp_files, os.path.dirname(config_file), args.path)
            cleanup_temp_files(turret, temp_files)

    else:
        print("you need to enter a valid project path")
        sys.exit(2)


def pack_turrets(sp):
    if six.PY2:
        parser = sp.add_parser('pack-turrets',
                               help="create turrets packages from a given oct project")
    else:
        parser = sp.add_parser('pack-turrets',
                               help="create turrets packages from a given oct project",
                               aliases=['pack'])
    parser.add_argument('path', type=str, help='path for oct project dir')
    parser.add_argument('--python', action='store_true', default=False, help='If set, a setup.py file will be created')
    parser.set_defaults(func=pack)
