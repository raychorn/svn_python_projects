# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# $Id: utils.py 109 2008-02-08 01:28:34Z semente $
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

import diario

def markuping(markup, value):
    """
    Transform plain text markup syntaxes to HTML with filters in 
    django.contrib.markup.templatetags.

    *Required arguments:*
    
        * ``markup``: 'markdown', 'rest' or 'texttile'. For any other string 
                    value is returned without modifications.
        * ``value``: plain text input
        
    """
    from django.contrib.markup.templatetags.markup \
        import textile, markdown, restructuredtext
    if markup == 'markdown':
        return markdown(value)
    elif markup == 'rest':
        return restructuredtext(value)
    elif markup == 'textile':
        return textile(value)
    else:
        return value            # raw

def get_svn_revision():
    """
    Returns the SVN revision in the form SVN-XXX,
    where XXX is the revision number.

    Returns SVN-unknown if anything goes wrong, such as an unexpected
    format of internal SVN files.
    """
    try:
        from django.utils import version
        rev = version.get_svn_revision(diario.__path__[0])
    except ImportError:
        rev = u'SVN-unknown'
    return rev
