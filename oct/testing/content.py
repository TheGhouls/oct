# This file is fit for containing basic content check
import lxml.html as lh


def must_contain(resp, pattern):
    """
    Test if the pattern is in content

    :param pattern: pattern to find
    :type pattern: str
    :param resp: a response object
    :return: None
    :raise: AssertionError
    """
    assert (pattern in lh.tostring(resp.html)), "The response does not contain the %s pattern" % pattern


def must_not_contain(resp, pattern):
    """
    Test if the pattern is not in content

    :param pattern: pattern to find
    :type pattern: str
    :param resp: a response object
    :return: None
    :raise: AssertionError
    """
    assert(pattern not in lh.tostring(resp.html)), "The response contain the %s pattern" % pattern

