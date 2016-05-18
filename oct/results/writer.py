import os
import shutil


class ReportWriter(object):
    """A class representing a report, used to output the result

    :param str results_dir: the output directory for the report
    :param str parent: the parent directory
    """
    def __init__(self, results_dir, parent):
        self.results_dir = results_dir
        self.fn = os.path.join(results_dir, 'results.html')
        self.templates_dir = os.path.join(results_dir, '../../', 'templates')

        self.set_statics()

    def set_statics(self):
        """Create statics directory and copy files in it
        """
        if not os.path.exists(self.results_dir):
            return None
        try:
            shutil.copytree(os.path.join(self.templates_dir, 'css'), os.path.join(self.results_dir, 'css'))
            shutil.copytree(os.path.join(self.templates_dir, 'img'), os.path.join(self.results_dir, 'img'))
            shutil.copytree(os.path.join(self.templates_dir, 'scripts'), os.path.join(self.results_dir, 'scripts'))
            shutil.copytree(os.path.join(self.templates_dir, 'fonts'), os.path.join(self.results_dir, 'fonts'))
        except OSError as e:
            if e.errno == 17:  # File exists
                print("WARNING : existing output directory for static files, will not replace them")
            else:  # in all other cases, re-raise exceptions
                raise

    def write_report(self, template):
        """Write the compiled jinja template to the results file

        :param template str: the compiled jinja template
        """
        with open(self.fn, 'w') as f:
            f.write(template)
