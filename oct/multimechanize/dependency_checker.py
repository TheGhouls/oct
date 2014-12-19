#!/usr/bin/env python
#
#  Copyright (c) 2010 Corey Goldberg (corey@goldb.org)
#  License: GNU LGPLv3
#
#  This file is part of Multi-Mechanize | Performance Test Framework
#


""" script to verify all multi-mechanize dependencies are satisfied """


try:
    import mechanicalsoup
    print('imported MechanicalSoup succesfully')
except ImportError:
    print('can not import MechanicalSoup')


try:
    import pylab
    print('imported Matplotlib succesfully')
except ImportError:
    print('can not import Matplotlib')


try:
    import sqlalchemy
    print('imported SQLAlchemy succesfully')
except ImportError:
    print('can not import SQLAlchemy')

