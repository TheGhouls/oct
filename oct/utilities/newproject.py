from __future__ import print_function
import os
import six
import sys
import shutil
import tarfile
from jinja2 import Environment, PackageLoader

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def check_template(members):

    required_members = [
        'config.json',
        'test_scripts',
        'templates',
        'templates/report.html'
    ]

    for fname in required_members:
        assert fname in members, "Required file %s not in archive" % fname

    return True


def from_template(args):
    """Create a new oct project from existing template

    :param Namespace args: command line arguments
    """
    project_name = args.name
    template = args.template

    with tarfile.open(template) as tar:
        check_template(tar.getnames())
        tar.extractall(project_name)


def from_oct(args):
    """Create a new oct project

    :param Namespace args: the command line arguments
    """
    project_name = args.name
    env = Environment(loader=PackageLoader('oct.utilities', 'templates'))

    config_content = env.get_template('configuration/config.json').render(script_name='v_user.py')
    script_content = env.get_template('scripts/v_user.j2').render()

    try:
        os.makedirs(project_name)
        os.makedirs(os.path.join(project_name, 'test_scripts'))
        os.makedirs(os.path.join(project_name, 'templates'))
        os.makedirs(os.path.join(project_name, 'templates', 'img'))

        shutil.copytree(os.path.join(BASE_DIR, 'templates', 'css'),
                        os.path.join(project_name, 'templates', 'css'))
        shutil.copytree(os.path.join(BASE_DIR, 'templates', 'javascript'),
                        os.path.join(project_name, 'templates', 'scripts'))
        shutil.copytree(os.path.join(BASE_DIR, 'templates', 'fonts'),
                        os.path.join(project_name, 'templates', 'fonts'))

        shutil.copy(os.path.join(BASE_DIR, 'templates', 'html', 'report.html'),
                    os.path.join(project_name, 'templates'))
    except OSError:
        print('ERROR: can not create directory for %r' % project_name, file=sys.stderr)
        raise
    with open(os.path.join(project_name, 'config.json'), 'w') as f:
        f.write(config_content)
    with open(os.path.join(project_name, 'test_scripts', 'v_user.py'), 'w') as f:
        f.write(script_content)


def create_project(args):

    if os.path.exists(args.name):
        raise OSError("Project %s already exists" % args.name)

    if args.template is not None:
        from_template(args)
    else:
        from_oct(args)


def new_project(sp):
    if six.PY2:
        parser = sp.add_parser('new-project', help="create a new oct project")
    else:
        parser = sp.add_parser('new-project', help="create a new oct project", aliases=['new'])
    parser.add_argument('name', type=str)
    parser.add_argument('-t', '--template', type=str, default=None, help="use existing project template")
    parser.set_defaults(func=create_project)
