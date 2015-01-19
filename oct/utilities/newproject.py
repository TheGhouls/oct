import os
import shutil
import sys
from oct.multimechanize.utilities.newproject import CONFIG_NAME, SCRIPT_NAME, \
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

SCRIPT_CONTENT = """from oct.core.generic import GenericTransaction
from octapp import app
import random
import time
import os


CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')


class Transaction(GenericTransaction):
    def __init__(self):
        GenericTransaction.__init__(self, CONFIG_PATH)

    def run(self):
        r = random.uniform(1, 2)
        time.sleep(r)
        self.custom_timers['Example_Timer'] = r


if __name__ == '__main__':
    trans = Transaction()
    trans.run()
    print(trans.custom_timers)
"""

CONFIG_CONTENT = """[global]
run_time = 30
rampup = 0
results_ts_interval = 10
progress_bar = on
console_logging = off
xml_report = off
base_url = http://localhost
default_sleep_time = 2


[user_group-1]
threads = 3
script = %s

[user_group-2]
threads = 3
script = %s

""" % (SCRIPT_NAME, SCRIPT_NAME)

CELERY_CONTENT = """from oct.core.main import app

app.conf.update(
    CELERY_RESULT_BACKEND='amqp',
    BROKER_URL='amqp://guest@localhost//'
)
"""

CELERY_SCRIPT = 'octapp.py'


def create_project(
        project_name,
        config_name=CONFIG_NAME,
        script_name=SCRIPT_NAME,
        scripts_dir=SCRIPTS_DIR,
        config_content=CONFIG_CONTENT,
        script_content=SCRIPT_CONTENT,
        template_dir=TEMPLATE_DIR,
        head_content=HEAD_CONTENT,
        footer_content=FOOTER_CONTENT,
        celery_content=CELERY_CONTENT,
        celery_script=CELERY_SCRIPT):

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
    except OSError:
        sys.stderr.write('\nERROR: can not create directory for %r\n\n' % project_name)
        sys.exit(1)
    with open(os.path.join(project_name, config_name), 'w') as f:
        f.write(config_content)
    with open(os.path.join(project_name, scripts_dir, script_name), 'w') as f:
        f.write(script_content)
    with open(os.path.join(project_name, scripts_dir, celery_script), 'w') as f:
        f.write(celery_content)
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
