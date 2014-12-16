from __future__ import absolute_import
__author__ = 'manu'

from celery import Celery

app = Celery('utilities',
             broker='amqp://guest@localhost//',
             include=['oct', 'oct.utilities', 'oct.utilities.run'])

if __name__ == '__main__':
    print "tata"
    app.start()