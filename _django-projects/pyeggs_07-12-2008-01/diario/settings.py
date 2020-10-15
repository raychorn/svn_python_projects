# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: settings.py 114 2008-02-26 02:49:35Z semente $
# ----------------------------------------------------------------------------
#
#  Copyright (c) 2007 Guilherme Mesquita Gondim
#
#  This file is part of django-diario.
#
#  django-diario is free software under terms of the GNU General
#  Public License version 3 (GPLv3) as published by the Free Software
#  Foundation. See the file README for copying conditions.
#


"""
Default Diário application settings.

If you not configure the settings below in your own project settings.py,
they assume default values::

    DIARIO_DEFAULT_MARKUP_LANG
        Markup language for blog entries. Options: 'rest', 'textile',
        'markdown' or 'raw' for raw text.
        Default: 'raw'.

    DIARIO_NUM_LATEST
        Number of latest itens on object_list view. Default: 10.
"""

from django.conf import settings


#
#  (!!!)
#
#  DON'T EDIT THESE VALUES, CONFIGURE IN YOUR OWN PROJECT settings.py
#

DIARIO_DEFAULT_MARKUP_LANG = getattr(settings, 'DIARIO_DEFAULT_MARKUP_LANG',
                                     'raw')
DIARIO_NUM_LATEST = getattr(settings, 'DIARIO_NUM_LATEST', 10)


# django-tagging support
HAS_TAG_SUPPORT = 'tagging' in settings.INSTALLED_APPS
try:
    import tagging
except ImportError:
    HAS_TAG_SUPPORT = False
