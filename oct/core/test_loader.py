import os
import imp
import inspect


class InvalidTestError(Exception):
    pass


def is_test_valid(test_module):
    """Test if the test_module file is valid

    We only check for the transaction class, since the generic transaction
    parent will raise a NotImplemented exception if the run method is not present
    :return: True if the test is valid, else False
    :rtype: bool
    :raises: InvalidTestError
    """
    if not hasattr(test_module, "Transaction"):
        raise InvalidTestError("No transaction class found")
    getattr(test_module, "Transaction")
    return True


def load_module(path):
    """Load a single module based on a path on the system

    :param str path: the full path of the file to load as a module
    :return: the module imported
    :rtype: mixed
    :raises: ImportError, InvalidTestError
    """
    if not os.path.exists(path):
        raise ImportError("File does not exists: {}".format(path))
    try:
        module_name = inspect.getmodulename(os.path.basename(path))
        module = imp.load_source(module_name, path)
        if is_test_valid(module):
            return module
        raise InvalidTestError("Module not valid")
    except ImportError as e:
        print("Error importing the tests script {}\nError: {}".format(module_name, e))
        raise InvalidTestError(e)


def load_file(file_name):
    """Load a single file based on its full path as a module

    :param str filename: the full path of the file
    :return: the module loaded
    :rtype: mixed
    :raises: ImportError, InvalidTestError
    """
    if not os.path.exists(file_name):
        raise ImportError("File does not exists: {}".format(file_name))
    realpath = os.path.realpath(os.path.abspath(file_name))
    return load_module(realpath)


def load_all(path, exclude=None):
    """Load all python scripts on the given folder path and return a dict containing thread_num

    the returned dict will be returned in the form::

        {
            'module_name': module_reference
        }

    :param str path: the pass of the folder
    :param list exclude: the list of files to exclude from the import
    :return: a dict containing the modules
    :rtype: dict
    """
    if exclude is None:
        exclude = []
    modules = {}
    package = os.path.realpath(os.path.abspath(path))
    if not os.path.isdir(package):
        return None
    for script in os.listdir(package):
        if not script.endswith('.py'):
            continue
        basename = os.path.basename(script)
        if basename.startswith('__') or basename == "octapp.py":
            continue
        os.path.join(package, basename)
        print("Loading module {}".format(basename))
        module = load_module(os.path.join(package, basename))
        if module:
            modules[module.__name__] = module
    return modules
