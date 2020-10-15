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
import os, sys

from vyperlogix import misc
from vyperlogix.misc import _utils

def _get_all_buckets(aConnection=None):
    from boto.s3 import connection
    aConnection = connection.S3Connection() if (aConnection is None) else aConnection
    return aConnection.get_all_buckets()

def _get_bucket_named(bucket_name,aConnection=None):
    buckets = _get_all_buckets(aConnection=aConnection)
    bucket = [b for b in buckets if (b.name == bucket_name)]
    return bucket[0] if ((misc.isList(bucket)) and (len(bucket) > 0)) else None

def _set_contents_from_file(bucket_name,fileObj,reduced_redundancy=True,callback=None,aConnection=None):
    aBucket = _get_bucket_named(bucket_name,aConnection=aConnection)
    if (aBucket is None):
        aBucket = aConnection.create_bucket(bucket_name)
    aKey = None
    try:
        _fsize = _utils.fileSize(fileObj.name)
        has_key = len([k for k in aBucket.get_all_keys() if (k.name == __file_name__)]) > 0
        if (not has_key):
            aKey = aBucket.new_key(key_name=fileObj.name)
            _metadata = _utils.explain_stat(os.stat(fileObj.name), asDict=True)
            aKey.set_contents_from_file(fileObj, cb=callback, reduced_redundancy=reduced_redundancy)
    except Exception, e:
	info_string = formattedException(details=ex)
        pass
    return aKey

def set_contents_from_file(bucket_name,fname,reduced_redundancy=True,callback=None,aConnection=None):
    f_in = open(fname, mode='rb', buffering=1)
    aKey = None
    try:
        aKey = _set_contents_from_file(bucket_name, f_in, callback=callback, reduced_redundancy=reduced_redundancy,aConnection=aConnection)
    except:
        aKey = None
    f_in.close()
    return aKey

def _get_directory_from(bucket,fname=None,aConnection=None):
    _is_not_fname = not misc.isString(fname)
    if (bucket):
        keys = [k for k in bucket.get_all_keys() if (_is_not_fname) or (k.name == fname)]
    return keys if (_is_not_fname) else keys[0] if (misc.isList(keys) and (len(keys) > 0)) else []

def get_directory(bucket_name,fname=None,aConnection=None):
    aBucket = _get_bucket_named(bucket_name,aConnection=aConnection)
    return _get_directory_from(aBucket)

def get_key_for_file(bucket_name,fname):
    return get_directory(bucket_name, fname=fname)

def _delete_key_for_file(aKey):
    aKey.delete()

def delete_key_for_file(bucket_name,fname):
    aKey = get_key_for_file(bucket_name, fname)
    _delete_key_for_file(aKey)
