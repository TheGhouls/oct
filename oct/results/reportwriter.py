import os
import shutil
import sys


class Report(object):
    def __init__(self, results_dir, parent):
        self.results_dir = results_dir
        self.fn = os.path.join(results_dir, 'results.html')
        self.templates_dir = os.path.join(results_dir, '../../', 'templates')

        with open(os.path.join(self.templates_dir, 'head.html')) as f:
            self.head = f.read()

        with open(os.path.join(self.templates_dir, 'footer.html')) as f:
            self.footer = f.read()

        self.set_statics()

    def set_statics(self):
        if not os.path.exists(self.results_dir):
            return
        try:
            shutil.copytree(os.path.join(self.templates_dir, 'css'), os.path.join(self.results_dir, 'css'))
            shutil.copytree(os.path.join(self.templates_dir, 'img'), os.path.join(self.results_dir, 'img'))
            shutil.copytree(os.path.join(self.templates_dir, 'scripts'), os.path.join(self.results_dir, 'scripts'))
        except OSError:
            sys.stderr.write('\nERROR : can not create directory for results\n\n')
            sys.exit(1)

    def write_line(self, line):
        with open(self.fn, 'a') as f:
            f.write('%s\n' % line)

    def write_report(self, template):
        with open(self.fn, 'w') as f:
            f.write(template)

    def write_head_html(self):
        with open(self.fn, 'w') as f:
            f.write(self.head)

    def write_closing_html(self):
        with open(self.fn, 'a') as f:
            f.write(self.footer)
