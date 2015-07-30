import os
import shutil
import sys
from jinja2 import Environment, PackageLoader

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def create_project(project_name):

    env = Environment(loader=PackageLoader('oct.utilities', 'templates'))

    config_content = env.get_template('configuration/config.cfg').render(script_name='v_user.py')
    script_content = env.get_template('scripts/v_user.py').render()
    head_content = env.get_template('html/head.html').render()
    footer_content = env.get_template('html/footer.html').render()

    if os.path.exists(project_name):
        sys.stderr.write('\nERROR: project already exists: %s\n\n' % project_name)
        raise OSError()
    try:
        os.makedirs(project_name)
        os.makedirs(os.path.join(project_name, 'test_scripts'))
        os.makedirs(os.path.join(project_name, 'templates'))
        os.makedirs(os.path.join(project_name, 'templates', 'css'))
        os.makedirs(os.path.join(project_name, 'templates', 'scripts'))
        os.makedirs(os.path.join(project_name, 'templates', 'img'))
        shutil.copy(os.path.join(BASE_DIR, 'templates', 'css', 'style.css'),
                    os.path.join(project_name, 'templates', 'css'))
    except OSError:
        sys.stderr.write('\nERROR: can not create directory for %r\n\n' % project_name)
        raise
    with open(os.path.join(project_name, 'config.cfg'), 'w') as f:
        f.write(config_content)
    with open(os.path.join(project_name, 'test_scripts', 'v_user.py'), 'w') as f:
        f.write(script_content)
    with open(os.path.join(project_name, 'templates', 'head.html'), 'w') as f:
        f.write(head_content)
    with open(os.path.join(project_name, 'templates', 'footer.html'), 'w') as f:
        f.write(footer_content)


def main():
    try:
        project_name = sys.argv[1]
    except IndexError:
        sys.stderr.write('\nERROR: no project specified\n\n')
        sys.stderr.write('Usage: oct-newproject <project name>\n\n')
        raise

    create_project(project_name)


if __name__ == '__main__':
    main()
