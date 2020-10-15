__copyright__ = """\
(c). Copyright 2008-2018, Vyper Logix Corp., All Rights Reserved.

Published under Creative Commons License 
(http://creativecommons.org/licenses/by-nc/3.0/) 
restricted to non-commercial educational use only., 

http://www.VyperLogix.com for details

THE AUTHOR VYPER LOGIX CORP DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL,
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
WITH THE USE OR PERFORMANCE OF THIS SOFTWARE !

USE AT YOUR OWN RISK.
"""

def deleteSalesForceObjects(sfdc,list_of_ids):
    import sys, traceback
    from vyperlogix import misc
    from vyperlogix.misc import ObjectTypeName
    deleted_ids = []
    t_sfdc = ObjectTypeName.typeName(sfdc)
    if (t_sfdc.find('.connection.Connection') > -1):
	if (all([misc.isString(id) for id in list_of_ids])):
	    try:
		delete_result = sfdc.delete(list_of_ids)
		deleted_ids = sfdc.resultToIdList(delete_result, success_status=True)
	    except Exception, details:
		exc_info = sys.exc_info()
		info_string = '\n'.join(traceback.format_exception(*exc_info))
		info_string = '%s :: Cannot process, Reason: %s\n%s' % (misc.funcName(),str(details),info_string)
		print >>sys.stderr, info_string
	else:
	    info_string = '%s :: Cannot process, Reason: "%s" is not a list of id(s) each being a string.' % (misc.funcName(),str(list_of_ids))
	    print >>sys.stderr, info_string
    else:
	info_string = '%s :: Cannot process, Reason: "%s" is not a valid connection object to pyax however it appears to be "%s".' % (misc.funcName(),str(sfdc),t_sfdc)
	print >>sys.stderr, info_string
    return deleted_ids

if __name__ == "__main__":
    import sys
    print >>sys.stdout, __copyright__
    print >>sys.stderr, __copyright__
