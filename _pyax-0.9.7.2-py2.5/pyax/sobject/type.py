from pyax.exceptions import NoConnectionError, SObjectTypeError

def verify_type(sfdc, sobject_type):
    if sfdc.svc is None:
        raise NoConnectionError()
    elif sobject_type not in sfdc.global_types:
        errmsg = 'Type "%s" is an invalid Apex object type.' %sobject_type
        raise SObjectTypeError(errmsg)
    
    return

