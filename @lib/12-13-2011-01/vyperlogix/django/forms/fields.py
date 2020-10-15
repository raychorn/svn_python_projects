import sys

from vyperlogix.misc import _utils

from django.utils.datastructures import SortedDict as SortedDictFromList

from vyperlogix.classes.SmartObject import SmartObject

def fields_for_model(model, formfield_callback=lambda f: f.formfield()):
    """
    Returns a list of fields for the given Django model class.

    Provide ``formfield_callback`` if you want to define different logic for
    determining the formfield for a given database field. It's a callable that
    takes a database Field instance and returns a form Field instance.
    """
    field_list = []
    try:
        opts = model._meta
        for f in opts.fields + opts.many_to_many:
            if not f.editable:
                continue
            formfield = formfield_callback(f)
            if formfield:
                field_list.append((f.name, formfield))
    except Exception, details:
        print >>sys.stderr, _utils.formattedException(details=details)
    return SortedDictFromList(dict(field_list))

