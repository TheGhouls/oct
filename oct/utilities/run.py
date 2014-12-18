__author__ = 'manu'

from oct.utilities.celery import app
import optparse
from subprocess import call
import sys
import os
import time


@app.task
def call_multimech(path, name):
    call(['multimech-run', name, '-d', path])


def oct_main():
    """
    Call the main multi-mechanize run function as a celery task

    :return: None
    """
    usage = 'Usage: %prog <project name> [options]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-n', '--num', dest='num', type='int', help='number of instance to start with celery')
    cmd_opts, args = parser.parse_args()

    try:
        project_name = args[0]
    except IndexError:
        sys.stderr.write('\nERROR: no project specified\n\n')
        sys.stderr.write('%s\n' % usage)
        sys.stderr.write('Example: multimech-run my_project\n\n')
        sys.exit(1)

    if cmd_opts.num:
        for i in range(0, cmd_opts.num):
            call_multimech.delay(os.path.abspath(project_name), project_name)
            time.sleep(0.0001)
    else:
        call_multimech.delay(os.path.abspath(project_name), project_name)