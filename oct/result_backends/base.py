class BaseStore(object):
    """Base class for defining how to store results for specific backend
    """
    def __init__(self, result_backend_config, output_dir):
        self.config = result_backend_config
        self.output_dir = output_dir

    def write_result(self, data):
        """Method called by HQ when data are received from turrets.

        This object is instanciated only one time on the HQ, so you can store multiple results in
        list to insert data by batch into store.

        :param dict data: data to save
        :return: None
        """
        raise NotImplementedError("Write result must be implemented")

    def after_tests(self):
        """Called at the end of HQ main loop. Useful if have remaining elements to write

        Default to `pass` statement, override not mandatory
        """
        pass


class BaseLoader(object):
    """Base class for retrieve results for a specific backend

    Mainly composed of properties. All properties returning more than one elements
    could use `yield` syntax
    """
    def __init__(self, config, output_dir):
        self.config = config
        self.output_dir = output_dir

    @property
    def total_errors(self):
        """Return total number of errors encountered during tests"""
        raise NotImplementedError('Property not implemented')

    @property
    def epoch_start(self):
        """Return epoch of test start"""
        raise NotImplementedError('Property not implemented')

    @property
    def epoch_end(self):
        """Return epoch of test end"""
        raise NotImplementedError('Property not implemented')

    @property
    def results_dataframe(self):
        """Only property that return a full dataframe. This choice is explained
        by the fact that pandas have a lot of optimised method to load data from different
        places.

        Returning directly a dataframe allow you to call pandas specific methods like `read_sql_query` for
        example.

        The dataframe MUST contains the following columns :
        * elapsed
        * epoch
        * scriptrun_time

        ..note::
            The dataframe should be return "raw". Thats mean that's you don't need to manipulate any
            data or index on it. Indexes and calculation will be made later by report class

        See documentation for more information about storing results
        """
        raise NotImplementedError('Property not implemented')

    @property
    def custom_timers(self):
        """Return a list or an iterator for getting all custom timers

        Custom timers don't carry epoch, so you MUST return a tuple containing
        the epoch and the then timers values with the following order::

            return epoch, timers

        See documentation or SQLiteLoader for example.
        """
        raise NotImplementedError('Property not implemented')

    @property
    def turrets(self):
        """Return list or iterator of all turrets"""
        raise NotImplementedError('Property not implemented')
