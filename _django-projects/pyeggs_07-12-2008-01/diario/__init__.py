# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: __init__.py 118 2008-02-26 03:46:24Z semente $
# ----------------------------------------------------------------------------
#
#  Copyright (c) 2007, 2008 Guilherme Mesquita Gondim
#
#  This file is part of django-diario.
#
#  django-diario is free software under terms of the GNU General
#  Public License version 3 (GPLv3) as published by the Free Software
#  Foundation. See the file README for copying conditions.
#


"""
Blog application for Django projects.
"""

from diario.utils import get_svn_revision


VERSION = (0, 1, 'joaquim')

def get_version():
    """
    Returns the version as a human-format string.
    """
    v = '.'.join([str(i) for i in VERSION[:-1]])
    return '%s-%s-%s' % (v, VERSION[-1], get_svn_revision())

__author__ = 'See the file AUTHORS.'
__date__ = '$Date: 2008-02-26 00:46:24 -0300 (Tue, 26 Feb 2008) $'[7:-2]
__license__ = 'GNU General Public License (GPL), Version 3'
__url__ = 'http://django-diario.googlecode.com'
__version__ = get_version()
