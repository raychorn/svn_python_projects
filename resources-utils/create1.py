import os
import re

from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName

from vyperlogix.hash import lists

import sys

from vyperlogix.sql.sqlalchemy import SQLAgent

from sqlalchemy import types as sqltypes

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

from vyperlogix import oodb
dbx_name = lambda fpath,name:oodb.dbx_name(name,fpath)

metadata = MetaData()
node_table = Table('library_node', metadata,
                    Column('id', sqltypes.Integer, nullable=False, default=0, primary_key=True),
                    Column('name', sqltypes.String(128), nullable=False),
                    Column('parent', sqltypes.Integer, nullable=True),
                    Column('creation_date', sqltypes.DateTime, nullable=False),
                    Column('modification_date', sqltypes.DateTime, nullable=False),
                    Column('is_active', sqltypes.Boolean, nullable=False),
                    Column('is_file', sqltypes.Boolean, nullable=False)
)

class Node(SQLAgent.BaseObject):
    pass

import socket
_cname = socket.gethostbyname_ex(socket.gethostname())[0].lower()
if (_cname == 'web22.webfaction.com'):
    conn_str = 'mysql://raychorn_resourc:peekab00@localhost:3306/raychorn_resourc'
elif (_cname == 'undefined3'):
    conn_str = 'mysql://root:peekab00@sql2005:3306/resources'
elif (_cname == 'misha-lap.ad.magma-da.com'):
    conn_str = 'mysql://root:peekaboo@localhost:3306/resources'
    
try:
    agent = SQLAgent.SQLAgent(conn_str,Node,node_table)
except SQLAgent.sqlalchemy.exc.OperationalError, details:
    print >>sys.stderr, _utils.formattedException(details=details)

#top = r'Z:\@myFiles\@Python'
top = r'Z:\@myFiles\@C++'

pattern = '@python'

_symbol_InternetShortcut = '[InternetShortcut]'

svnFilter = '[._]svn' 
rxSVN=re.compile(svnFilter)

py26Filter = '@Python_2.6a3' 
rxPy26=re.compile(py26Filter)

filter = lambda f:(f.lower().find(pattern) > -1)

def root_folders(_top,_filter=None):
    files = os.listdir(_top)
    return [os.sep.join([_top,f]) for f in files if (not callable(_filter)) or ((callable(_filter)) and _filter(f))]

def save_dict(fname, d_obj):
    from vyperlogix import oodb
    if (not lists.isDict(d_obj)):
	print >>sys.stderr, '(%s) :: ERROR: d_obj is not of type "dict" however it is of type "%s" and this is unacceptable.' % (misc.funcName(),ObjectTypeName.typeClassName(d_obj))
	return
    dbx = oodb.PickledFastCompressedHash2(fname)
    try:
	for k,v in d_obj.iteritems():
	    dbx[k] = v
    except Exception, details:
	_details = _utils.formattedException(details)
	print >>sys.stderr, _details
    finally:
	dbx.close()

def read_dict(fname):
    from vyperlogix import oodb
    return oodb.PickledFastCompressedHash2(fname)

def dictWalker(d_parent={},s_parent=[],pid=-1):
    '''d_parent is the dict, s_parent is the current path, pid is the id of the parent node in the database.'''
    if (lists.isDict(d_parent)):
	_files = root_folders(top)
        for k,v in d_parent.iteritems():
            s_parent.append(k)
            if (lists.isDict(v)):
                if (len(v) > 0):
                    dictWalker(d_parent=v,s_parent=s_parent,pid=-1)
		else:
		    p = os.sep.join([top,os.sep.join(s_parent)])
		    print '(%s) %s' % (os.path.exists(p),p)
		    s_parent.pop()
	    else:
		p = os.sep.join([os.sep.join(s_parent),v])
		print '(%s) %s' % (os.path.exists(p),p)
		s_parent.pop()

def main():
    _root_ = os.path.abspath('.')
    print '_root_ is "%s".' % (_root_)
    fname = oodb.getMungedFilenameFor(oodb.dbx_name('The_Catalog',_root_))
    if (os.path.exists(fname)):
	dbx = read_dict(fname)
	try:
	    dictWalker(d_parent=dbx,s_parent=[],pid=-1)
	finally:
	    dbx.close()
    else:
	_files = root_folders(top)
	i = 1
	n = len(_files)
	_d_ = lists.HashedLists2()
	begin_ts = _utils.timeSeconds()
	try:
	    for _r_ in _files:
		files = os.listdir(_r_)
		_rr_ = os.path.dirname(_r_)
		i2 = 1
		n2 = len(files)
		for f in files:
		    _f = os.sep.join([_r_,f])
		    for root, dirs, files in os.walk(_f):
			if (not rxSVN.search(root)) and (not rxPy26.search(root)):
			    _root = os.sep.join([s for s in root.replace(_rr_,'').split(os.sep) if (len(s) > 0)])
			    if (len(_root) > 0) and (len(files) > 0):
				n_pcent = (float(i) / float(n))
				pcent = n_pcent * 100.0
				pcent2 = (float(i2) / float(n2)) * 100.0
				curr_ts = _utils.timeSeconds()
				et_ts = curr_ts - begin_ts
				x_et_ts = (float(et_ts) * 100.0) / pcent
				s_et_ts = '%-10.2f'%x_et_ts
				s_et_ts = s_et_ts.strip()
				x_et_ts2 = (float(et_ts) * 100.0) / pcent2
				s_et_ts2 = '%-10.2f'%x_et_ts2
				s_et_ts2 = s_et_ts2.strip()
				print 'BEGIN: (%2.0f%%)/(%2.0f%%) (%s/%s secs remain) "%s"' % (pcent,pcent2,s_et_ts,s_et_ts2,_root)
				d_parent = None
				for name in files:
				    isInternetShortcut = False
				    _name = os.sep.join([_rr_,_root,name])
				    _url = ''
				    d_url = lists.HashedLists2()
				    if (name.lower().endswith('.url')):
					#assert os.path.exists(_name), 'Oops, something went wrong "%s" does not seem to exist however it should.' % (_name)
					if (os.path.exists(_name)):
					    fIn = open(_name, 'rb')
					    try:
						bytes = fIn.read()
					    finally:
						fIn.close()
					    l_bytes = bytes.split('\r\n')
					    if (l_bytes[0] == _symbol_InternetShortcut):
						isInternetShortcut = True
						toks = ''.join(l_bytes[1:]).split('=')
						_url = ''.join(toks[1:])
						d_url[name] = ''.join(toks[1:])
						print '%s' % (_url)
						pass
				    if (not isInternetShortcut):
					# build this as a nested series of dictionary objects where the parent is the key for the parent dict.
					# nodes with no contents are leaf nodes otherwise the key is the name of the node.
					d_data = _d_
					s_name = _name.replace(_rr_,'')
					print '\t%s' % (s_name)
					nodes = s_name.split(os.sep)
					for s in nodes[0:]:
					    if (len(s) == 0):
						continue
					    #if (s.startswith('Python ')):
						#s = s.replace('Python ', '')
					    if (not d_data.has_key(s)):
						d_data[s] = lists.HashedLists2()
					    d_parent = d_data
					    d_data = d_data[s]
				    elif (d_parent is not None):
					for k,v in d_url.iteritems():
					    d_parent[k] = v
				    else:
					d_data = _d_
					s_name = _name.replace(_rr_,'')
					print '\t%s' % (s_name)
					nodes = s_name.split(os.sep)
					for s in nodes[0:]:
					    if (len(s) == 0):
						continue
					    #if (s.startswith('Python ')):
						#s = s.replace('Python ', '')
					    if (not d_data.has_key(s)):
						d_data[s] = lists.HashedLists2()
					    d_parent = d_data
					    d_data = d_data[s]
					for k,v in d_url.iteritems():
					    d_data[k] = v
				print 'END! (%2.0f%%)/(%2.0f%%) (%s/%s secs remain) "%s"' % (pcent,pcent2,s_et_ts,s_et_ts2,_root)
				print '='*80
				print
				
		    i2 += 1
		i += 1
	except Exception, details:
	    print _utils.formattedException(details=details)
	finally:
	    print 'Saving to "%s".' % (fname)
	    save_dict(fname,_d_)
	#fOut = open(os.sep.join([_root_,'The_Catalog.txt']),'w')
	#print fOut.name
	#lists.prettyPrint(_d_,title='The Catalog',fOut=fOut)
	#fOut.flush()
	#fOut.close()
    print 'DONE !!!'

if (__name__ == '__main__'):
    from vyperlogix.misc import _psyco
    _psyco.importPsycoIfPossible(func=main)

    main()
