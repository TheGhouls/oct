import os
import shutil


class Report(object):
    def __init__(self, results_dir, parent):
        self.results_dir = results_dir
        self.fn = os.path.join(results_dir, 'results.html')
        self.templates_dir = os.path.join(results_dir, '../../', 'templates')

        self.set_statics()

    def set_statics(self):
        if not os.path.exists(self.results_dir):
            return
        try:
            shutil.copytree(os.path.join(self.templates_dir, 'css'), os.path.join(self.results_dir, 'css'))
            shutil.copytree(os.path.join(self.templates_dir, 'img'), os.path.join(self.results_dir, 'img'))
            shutil.copytree(os.path.join(self.templates_dir, 'scripts'), os.path.join(self.results_dir, 'scripts'))
        except OSError:
            raise OSError("Could not create directory for results")

    def write_report(self, template):
        with open(self.fn, 'w') as f:
            f.write(template)
