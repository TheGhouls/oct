from __future__ import print_function
import os
import shutil
import sys
from jinja2 import Environment, PackageLoader

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_project(project_name):
    """Create a new oct project

    :param str project_name: the name of the project
    """
    env = Environment(loader=PackageLoader('oct.utilities', 'templates'))

    config_content = env.get_template('configuration/config.json').render(script_name='v_user.py')
    script_content = env.get_template('scripts/v_user.py').render()

    if os.path.exists(project_name):
        sys.stderr.write('\nERROR: project already exists: %s\n\n' % project_name)
        raise OSError("Project %s already exists" % project_name)
    try:
        os.makedirs(project_name)
        os.makedirs(os.path.join(project_name, 'test_scripts'))
        os.makedirs(os.path.join(project_name, 'templates'))
        os.makedirs(os.path.join(project_name, 'templates', 'img'))

        shutil.copytree(os.path.join(BASE_DIR, 'templates', 'css'),
                        os.path.join(project_name, 'templates', 'css'))
        shutil.copytree(os.path.join(BASE_DIR, 'templates', 'javascript'),
                        os.path.join(project_name, 'templates', 'scripts'))

        shutil.copy(os.path.join(BASE_DIR, 'templates', 'html', 'report.html'),
                    os.path.join(project_name, 'templates'))
    except OSError:
        print('ERROR: can not create directory for %r' % project_name, file=sys.stderr)
        raise
    with open(os.path.join(project_name, 'config.json'), 'w') as f:
        f.write(config_content)
    with open(os.path.join(project_name, 'test_scripts', 'v_user.py'), 'w') as f:
        f.write(script_content)


def main():
    try:
        project_name = sys.argv[1]
    except IndexError:
        print('ERROR: no project specified', file=sys.stderr)
        print('Usage: oct-newproject <project name>')
        raise

    create_project(project_name)
