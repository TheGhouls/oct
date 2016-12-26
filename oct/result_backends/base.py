class BaseStore:
    """Base class for defining how to store results for specific backend
    """
    def __init__(self, result_backend_config):
        self.config = result_backend_config

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


class BaseLoader:
    """Base class for retrieve results for a specific backend

    Mainly composed of properties. All properties returning more than one elements
    could use `yield` syntax
    """
    def __init__(self, result_backend_config):
        self.config = result_backend_config

    @property
    def total_errors(self):
        raise NotImplementedError('Property not implemented')

    @property
    def epoch_start(self):
        raise NotImplementedError('Property not implemented')

    @property
    def epoch_end(self):
        raise NotImplementedError('Property not implemented')

    @property
    def results(self):
        raise NotImplementedError('Property not implemented')

    @property
    def custom_timers(self):
        raise NotImplementedError('Property not implemented')

    @property
    def turrets(self):
        raise NotImplementedError('Property not implemented')
