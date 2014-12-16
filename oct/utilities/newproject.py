import os
import shutil
import sys
from oct.multimechanize.utilities.newproject import CONFIG_CONTENT, CONFIG_NAME, SCRIPT_CONTENT, SCRIPT_NAME, \
    SCRIPTS_DIR


TEMPLATE_DIR = 'templates'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

HEAD_CONTENT = """
<!DOCTYPE html>
<html>

<head>
    <title> OCT | Results </title>
    <link rel="stylesheet" type="text/css" href="css/style.css" />
</head>

<body id="main">
"""

FOOTER_CONTENT = """
</body>
</html>
"""


def create_project(
        project_name,
        config_name=CONFIG_NAME,
        script_name=SCRIPT_NAME,
        scripts_dir=SCRIPTS_DIR,
        config_content=CONFIG_CONTENT,
        script_content=SCRIPT_CONTENT,
        template_dir=TEMPLATE_DIR,
        head_content=HEAD_CONTENT,
        footer_content=FOOTER_CONTENT):

    if os.path.exists(project_name):
        sys.stderr.write('\nERROR: project already exists: %s\n\n' % project_name)
        sys.exit(1)
    try:
        os.makedirs(project_name)
        os.makedirs(os.path.join(project_name, scripts_dir))
        os.makedirs(os.path.join(project_name, template_dir))
        os.makedirs(os.path.join(project_name, template_dir, 'css'))
        os.makedirs(os.path.join(project_name, template_dir, 'scripts'))
        os.makedirs(os.path.join(project_name, template_dir, 'img'))
        shutil.copy(os.path.join(BASE_DIR, 'templates', 'css', 'style.css'),
                    os.path.join(project_name, template_dir, 'css'))
    except OSError as e:
        sys.stderr.write('\nERROR: can not create directory for %r\n\n' % project_name)
        sys.exit(1)
    with open(os.path.join(project_name, config_name), 'w') as f:
        f.write(config_content)
    with open(os.path.join(project_name, scripts_dir, script_name), 'w') as f:
        f.write(script_content)
    with open(os.path.join(project_name, template_dir, 'head.html'), 'w') as f:
        f.write(head_content)
    with open(os.path.join(project_name, template_dir, 'footer.html'), 'w') as f:
        f.write(footer_content)


def main():
    try:
        project_name = sys.argv[1]
    except IndexError:
        sys.stderr.write('\nERROR: no project specified\n\n')
        sys.stderr.write('Usage: oct-newproject <project name>\n\n')
        sys.exit(1)

    create_project(project_name)


if __name__ == '__main__':
    main()

