class OctConfigurationError(Exception):
    """Provide an oct configuration error
    """
    pass


class OctGenericException(Exception):
    """
    Provide generic exception for reports

    """
    pass


class FormNotFoundException(Exception):
    """
    Raised in case of FormNotFound with browser

    """
    pass


class NoUrlOpen(Exception):
    """
    Raised in case of no url open but requested inside browser class

    """
    pass


class LinkNotFound(Exception):
    """
    Raised in case of link not found in current html document

    """
    pass


class NoFormWaiting(Exception):
    """
    Raised in case of action required form if no form selected

    """
    pass
