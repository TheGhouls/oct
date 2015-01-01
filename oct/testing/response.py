# This file is fit for containing basic response status check
# All functions have to take a response object in param


def check_response_status(resp, status):
    """
    This will check is the response_code is equal to the status

    :param resp: a response object
    :param status: the expected status
    :type status: int
    :return: None
    :raise: AssertionError
    """
    assert(resp.code == status), "Bad Response: HTTP %s, expected %s, URL : %s" % (resp.code, status, resp.geturl())