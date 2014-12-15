__author__ = 'manu'

from celery import task
from oct.multimechanize.utilities.run import main


def oct_main():
    main()
