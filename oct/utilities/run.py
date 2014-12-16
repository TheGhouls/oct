__author__ = 'manu'

from celery import task
from oct.multimechanize.utilities.run import main


@task
def oct_main():
    """
    Call the main multi-mechanize run function as a celery task

    :return: None
    """
    main()
