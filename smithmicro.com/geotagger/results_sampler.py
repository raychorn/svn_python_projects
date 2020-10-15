from vyperlogix import misc
from vyperlogix.misc import _utils

from vyperlogix.misc import ObjectTypeName

from vyperlogix.misc import threadpool
_Q_ = threadpool.ThreadQueue(50)

from vyperlogix.django import django_utils
from vyperlogix.classes.SmartObject import SmartFuzzyObject
from vyperlogix.misc import _utils

from vyperlogix.json import json_to_python
from vyperlogix.xml.xml_utils import xml_to_json, python_to_xml

from vyperlogix.xml.XMLJSON import python_to_json

from vyperlogix.lists import ListWrapper
from vyperlogix.hash.lists import HashedLists

from sqlalchemy import *

import os, sys
import random

import uuid

import sqlalchemy_models

from geotaggerhook import geotagger

from vyperlogix.misc import Args
from vyperlogix.misc import PrettyPrint

import tempfile, shutil, os, time

_has_mondogb = False
try:
    from pymongo import Connection as mongoConnection
    _has_mondogb = True
except ImportError:
    pass

_start_lat = 37.0
_start_lng = -122

_num_lat = 1
_num_lng = 1

_xml_template__ = '''<?xml version="1.0" standalone="yes"?>
<RECORDS>
{{ records }}
</RECORDS>'''

__xml_record_template__ = '''<RECORD>
<id>{{ id }}</id>
<heat_lat>{{ heat_lat }}</heat_lat>
<heat_lng>{{ heat_lng }}</heat_lng>
<heat_x>{{ heat_x }}</heat_x>
<heat_y>{{ heat_y }}</heat_y>
<heat_num>{{ heat_num }}</heat_num>
<{{ data_node_name }}>{{ data_node_value }}</{{ data_node_name }}>
</RECORD>'''

__data_nodes_ = [
    {'name':'peak_speed','num':70,'report':'Average Peak Download Speed Heat Map'},
    {'name':'signal_strength','num':69,'report':'Average Signal Strength Heat Map'},
    {'name':'num_failures','num':72,'report':'Connection Failure Rate Heat Map'},
    {'name':'connections','num':66,'report':'Connections per Day Heat Map'},
    {'name':'error_freq','num':71,'report':'Error Frequency Heat Map'},
    {'name':'throughput','num':68,'report':'Throughput per Day Heat Map'},
    {'name':'sum_conn_attempts','num':61,'report':'Total Connections Heat Map'},
    {'name':'throughput','num':67,'report':'Total Throughput Heat Map'},
]

def new_context_from(_id,heat_lat,heat_lng,heat_x,heat_y,heat_num,data_node_name,data_node_value):
    c = {
        'id':_id,
        'heat_lat':heat_lat,
        'heat_lng':heat_lng,
        'heat_x':heat_x,
        'heat_y':heat_y,
        'heat_num':heat_num,
        'data_node_name':data_node_name,
        'data_node_value':data_node_value,
    }
    return c

def write_xml_for_into(records,_fname):
    f = open(_fname,'w')
    try:
        xml = django_utils.render_from_string(_xml_template__,context={'records':records})
        print >>f, xml
    except Exception, e:
        print >> sys.stderr, _utils.formattedException(details=e)
    f.flush()
    f.close()

def write_data_for(name,num,num_records=25):
    record_choices = []
    _i_ = 0
    _id_ = 0
    _data_node_name = name
    random.seed()
    random_choice = lambda x:random.randrange(0,x*10,1)/10
    records = ''
    _step = 1.0/50
    _lat = lat = _start_lat
    _lng = _start_lng
    while (lat < _lat+_num_lat):
        lng = _start_lng
        while (lng > _lng-_num_lng):
            if (_id_ > 0):
                records += '\n'
            if (_i_ % 100) == 0:
                print >>sys.stderr, '%s/%s :: %s,%s to %s,%s Center: %s,%s' % (_i_,_id_,lat,lng,lat+(_step),lng-(_step),lat+(_step/2),lng-(_step/2))
            g = SmartFuzzyObject(geotagger(lat,lng))
            record = django_utils.render_from_string(__xml_record_template__,context=new_context_from(_id_,g.heat_lat,g.heat_lng,g.heat_x,g.heat_y,g.heat_num,_data_node_name,random_choice(100)))
            record_choices.append(record)
            _id_ += 1
            lng -= _step
            _i_ += 1
        lat += _step
    for n in xrange(0,num_records+1):
        records += random.choice(record_choices)
    _fname = 'sample_result_%s.xml' % (num)
    print >>sys.stderr, 'WRITING DATA into "%s"...' % (_fname)
    write_xml_for_into(records,_fname)
    print >>sys.stderr, 'DONE WRITING DATA in "%s"!\n\n' % (_fname)

def geotagger_on(d):
    normalize = lambda x,y:float(x['heat_%s'%(y)]['data'])
    normalize_lat = lambda x:normalize(x,'lat')
    normalize_lng = lambda x:normalize(x,'lng')
    random_choice = lambda x:random.randrange(0,x*10,1)/10
    try:
	try:
	    items = d['RECORDS']['RECORD']
	except:
	    items = d
	if (misc.isList(items)):
	    _id_ = 0
	    for item in items:
		_heat_lat = normalize_lat(item)
		_heat_lng = normalize_lng(item)
		del item['heat_lat']['data']
		del item['heat_lng']['data']
		_item = SmartFuzzyObject(item)
		g = SmartFuzzyObject(geotagger(_heat_lat,_heat_lng))
		_item.id = _id_
		_item.heat_lat = g.heat_lat
		_item.heat_lng = g.heat_lng
		_item.heat_gps = {'lat':_heat_lat,'lng':_heat_lng}
		_item.heat_x = g.heat_x
		_item.heat_y = g.heat_y
		_item.heat_num = g.heat_num
		if (item.has_key('data_node_name')):
		    del item['data_node_name']
		    random.seed()
		    _item.num_connections = random_choice(100)
		    for k in _item.keys():
			if (k != '__dict__'):
			    item[k] = _item[k]
		_id_ += 1
	else:
	    print 'WARNING: Cannot process the data for purpose of geotagging...'
    except Exception, e:
	info_string = _utils.formattedException(details=e)
	print info_string

def smsi_json_from(d,is_aggregate=True):
    try:
	columns = [k for k in d[0].keys() if (k != 'id')]
    except:
	columns = []
    _data = []
    if (is_aggregate):
	d_aggregated = {}
	d_col_name = [c for c in columns if (not c.startswith('heat_'))][0]
	d_aggregated[d_col_name] = {}
	_d_ = HashedLists()
	target_d = d_aggregated[d_col_name]
	for item in d:
	    k = '%s@%s' % (item['heat_x'],item['heat_y'])
	    _d_[k] = item
	    if (len(_d_[k]) == 1):
		target_d[k] = item
	    else:
		target_d[k][d_col_name] = target_d[k][d_col_name] + item[d_col_name]
	for k,v in target_d.iteritems():
	    _data.append(v)
	_fext = os.path.splitext(_fpath)
	for k,v in _d_.iteritems():
	    __fext = ListWrapper.ListWrapper(misc.copy(_fext))
	    __fext[-1] = '.json'
	    __fext.insert(1,k)
	    __json = smsi_json_from(v,is_aggregate=False)
	    #__json = python_to_json(v,seps=(',', ':'))
	    _fpath4 = '%s-json-%s%s' % tuple(__fext)
	    print 'Writing JSON to "%s".' % (_fpath4)
	    _utils.writeFileFrom(_fpath4,__json)
    results = []
    for item in d if (len(_data) == 0) else _data:
	aResult = []
	for c in columns:
	    aResult.append(item[c])
	results.append(aResult)
    data = {}
    data['results'] = results
    data['columns'] = columns
    json = python_to_json(data,seps=(',', ':'))
    return json

_vector = SmartFuzzyObject({'count':0})

def verbose_mongo_objects():
    if (_isMONGODB):
	db = aMongoConnection[_mongodb_dbname]
	collection_names = [c for c in db.collection_names() if (c not in ['system.indexes'])]
	print >>sys.stderr, '%s' % ('='*30)
	for cname in collection_names:
	    if (cname not in ['coords','geocodes','system.indexes','values']):
		aColl = db[cname]
		print >>sys.stderr, 'BEGIN: %s' % (cname)
		_cursor = aColl.find()
		try:
		    _aggregations = 'aggregations'
		    for item in _cursor:
			_keys = [k for k in item.keys() if (k not in [_aggregations,'name'])]
			for k in _keys:
			    print >>sys.stderr, '\t%s=%s' % (k,item[k])
			_tabs = '\t\t\t'
			_json = python_to_json(item[_aggregations],seps=(',\n'+_tabs,':'))
			print >>sys.stderr, '\t\t%s\n%s%s' % (_aggregations,_tabs,_json)
		except:
		    pass
		print >>sys.stderr, 'END!   %s\n' % (cname)
	print >>sys.stderr, '%s\n\n' % ('='*30)
	db.logout()

def key_reduce(t,toks):
    '''t is the target ListWrapper() instance, toks is the list of tokens in the form of ['_x','_y'] or ['_lat','_lng']'''
    _fx_ = t.findFirstContaining(toks[0])
    _fy_ = t.findFirstContaining(toks[-1])
    if (_fx_ > -1) and (_fy_ > -1):
	_dx_ = HashedLists(dict([(i,i) for i in t[_fx_].split('_')]))
	_dy_ = HashedLists(dict([(i,i) for i in t[_fy_].split('_')]))
	_d_ = HashedLists({})
	for k,v in _dx_.iteritems():
	    _d_[k] = v
	for k,v in _dy_.iteritems():
	    _d_[k] = v
	_da_ = _d_.insideOut()
	for k,v in _da_.iteritems():
	    del _da_[k]
	    _da_[k] = len(v)
	_db_ = HashedLists(_da_.asDict())
	_db_ = _db_.insideOut()
	__i__ = misc.sortCopy(_db_.keys())
	__k__ = __k__ = eval(_db_[__i__[-1]][0])[0]
	__ii__ = ','.join(misc.sortCopy([eval(i)[0] for i in _db_[__i__[0]]]))
	del t[max(_fx_,_fy_)]
	t[min(_fx_,_fy_)] = '_'.join([__k__,__ii__])

def gather_key_from(toks,_d_):
    parts = []
    for i in toks[-1].split(','):
	k = '_'.join([toks[0],i])
	if (_d_.has_key(k)):
	    parts.append('%d'%(int(_d_[k])))
    return 'x'.join(parts)

def _handle_some_records(f_out,_num,items):
    from sets import Set
    as_normalized_json = lambda aProxy:''.join(python_to_json(aProxy).split('\n'))
    print 'DEBUG_%s: BEGIN: #%s' % (misc.funcName(),_num)
    _i_ = 1
    _k_ = len(items)/10
    for item in items:
	if (_isETL):
	    s = [i for i in list(Set(item.__dict__.keys())) if (i not in ['_sa_instance_state', u'id']) and (not i.startswith('heat_'))]
	    for i in s:
		print >> f_out, '<RECORD><id>%s</id><heat_gps>%s</heat_gps><heat_lat>%s</heat_lat><heat_lng>%s</heat_lng><heat_x>%s</heat_x><heat_y>%s</heat_y><heat_num>%s</heat_num><data_name>%s</data_name><data_value>%s</data_value><timestamp>%s</timestamp></RECORD>' % (uuid.uuid4(),item.heat_gps,int(item.heat_lat),int(item.heat_lng),int(item.heat_x),int(item.heat_y),int(item.heat_num),i,int(item.__dict__[i]),_utils.timeStampMySQL())
	elif (_isMONGODB):
	    db = aMongoConnection[_mongodb_dbname]
	    try:
		_l_ = list(Set(item.__dict__.keys()))
		s = [i for i in _l_ if (i not in ['_sa_instance_state', u'id']) and (not i.startswith('heat_'))]
		t = ListWrapper.ListWrapper([i for i in _l_ if (i.startswith('heat_')) and (any([i.endswith(tok) for tok in ['_lat','_lng','_x','_y']]))])
		key_reduce(t,['_x','_y'])
		key_reduce(t,['_lat','_lng'])
		for i in s:
		    _it_ = '%s' % (i)
		    aggregations = db[_it_]
		    _val = item.__dict__[i]
		    aValueProxy = {}
		    for tok in t:
			_toks_ = tok.split('_')
			_ext_ = ''.join(_toks_[-1].split(','))
			__key__ = gather_key_from(_toks_,item.__dict__)
			aValueProxy['key_%s'%(_ext_)] = __key__
		    ###########################################
		    aValue = aggregations.find_one(aValueProxy)
		    if (not aValue):
			for tok in t:
			    _toks_ = tok.split('_')
			    _ext_ = ''.join(_toks_[-1].split(','))
			    __key__ = gather_key_from(_toks_,item.__dict__)
			    aValueProxy['value_%s'%(_ext_)] = _val
			aValueId = aggregations.save(aValueProxy)
			if (_isVerbose):
			    print 'DEBUG: %s.%s.%s #(%s) aggregations.%s.count()=%s' % (misc.funcName(),_num,_i_,aValueId,i,aggregations.count())
		    else:
			_doc_value = {}
			for tok in t:
			    _toks_ = tok.split('_')
			    _ext_ = ''.join(_toks_[-1].split(','))
			    __key__ = gather_key_from(_toks_,item.__dict__)
			    _value_key = 'value_%s'%(_ext_)
			    if (aValue.has_key(_value_key)):
				aValue[_value_key] = aValue[_value_key] + _val
			    else:
				aValue[_value_key] = _val
			    _doc_value[_value_key] = aValue[_value_key]
			_doc = { "$set" : _doc_value }
			aggregations.update( aValueProxy, _doc );
			if (_isDebug):
			    aValue = aggregations.find_one(aValueProxy)
			if (_isVerbose):
			    print 'DEBUG: %s.%s.%s #(%s) aggregations.count()=%s' % (misc.funcName(),_num,_i_,i,aggregations.count())
		    ###########################################
		if (_isVerbose):
		    verbose_mongo_objects()
	    except Exception, ex:
		info_string = _utils.formattedException(details=ex)
		print >>sys.stderr, info_string
	    db.logout()
	else:
	    g = SmartFuzzyObject(geotagger(item.heat_lat,item.heat_lng))
	    s = [i for i in list(Set(item.__dict__.keys()) - Set(g.keys())) if (i not in ['_sa_instance_state', u'id'])]
	    _heat_gps = ','.join(str([('%s=%s'%(str(k).strip(),str(v).strip())).strip() for k,v in {'lat':item.heat_lat,'lng':item.heat_lng}.iteritems()]).split(', ')).replace('[','').replace(']','').replace("'",'')
	    _extra = ''.join(['<%s>%s</%s>'%(i,item.__dict__[i],i) for i in s])
	    print >> f_out, '<RECORD><id>%d</id><heat_lat>%s</heat_lat><heat_lng>%s</heat_lng><heat_x>%d</heat_x><heat_y>%d</heat_y><heat_num>%d</heat_num><heat_gps>%s</heat_gps>%s</RECORD>' % (item.id,g.heat_lat,g.heat_lng,g.heat_x,g.heat_y,g.heat_num,_heat_gps,_extra)
	if (_i_ % _k_) == 0:
	    print '%s.%s.%s' % (misc.funcName(),_num,_i_)
	_i_ += 1
    verbose_mongo_objects()
    print 'DEBUG_%s: END! #%s' % (misc.funcName(),_num)

@threadpool.threadify(_Q_)
def handle_some_records(f_out,_num,items):
    _handle_some_records(f_out,_num,items)

@threadpool.threadify(_Q_)
def gather_id_list(f_out,_num,items):
    print 'DEBUG_%s: BEGIN: #%s' % (misc.funcName(),_num)
    _i_ = 1
    _k_ = len(items)/10
    for item in items:
	print >> f_out, '%s' % (item.id)
	if (_i_ % _k_) == 0:
	    print '%s.%s.%s' % (misc.funcName(),_num,_i_)
	_i_ += 1
    print 'DEBUG_%s: END! #%s' % (misc.funcName(),_num)

def begin_xml(f_out):
    print >> f_out, '<?xml version="1.0" standalone="yes"?>'
    print >> f_out, '<RECORDS>'
    
def end_xml(f_out):
    print >> f_out, '</RECORDS>'

def process_mySQL():
    value1_unless_value2 = lambda value1,value2,clause:value1 if (clause) else value2
    min_value_unless = lambda value1,value2,clause:min(value1,value2) if (clause) else value1
    _vector.count = 0
    def handle_items(items):
	n = len(items)
	print 'DEBUG_%s: Retrieved %d items.' % (misc.funcName(),n)
	_vector.count = _vector.count + n
    session,samples = sqlalchemy_models.get_gps1M_qry()
    _n_ = min_value_unless(samples.count(),_limits,(_limits > 0))
    _s_ = value1_unless_value2(_n_/100,_n_,(_limits < 1))
    _i_ = 1
    print 'DEBUG_%s: There are %d items by %s total.' % (misc.funcName(),_n_,_s_)
    f_out = None
    if (not _isMONGODB):
	f_out = open('data.xml',mode='w')
	begin_xml(f_out)
    for i in xrange(0,_n_,_s_):
	j = i+(_s_ if ((i + _s_) < _n_) else _n_ - i)
	items = samples[i:j]
	print 'DEBUG_%s: %s :: samples[%d:%d]=%s items' % (misc.funcName(),_i_,i,j,len(items))
	print '\tDEBUG_%s: %s' % (misc.funcName(),['%s:%s'%(k,items[0].__dict__[k]) for k in items[0].__dict__.keys() if (k not in ['_sa_instance_state'])])
	if (not _isThreads):
	    _handle_some_records(f_out,_i_,items)
	else:
	    handle_some_records(f_out,_i_,items)
	#gather_id_list(f_out,_i_,items)
	_i_ += 1
    print 'DEBUG_%s: @@@' % (misc.funcName())
    print 'DEBUG_%s: Waiting for all threads to complete...' % (misc.funcName())
    _Q_.join()
    print 'DEBUG_%s: All threads have completed!' % (misc.funcName())
    if (not _isMONGODB):
	end_xml(f_out)
	f_out.flush()
	f_out.close()
    try:
	session.flush()
	session.commit()
    except Exception:
	pass
    print 'DEBUG_%s: Exiting !' % (misc.funcName())
    sys.exit(111)

if (__name__ == '__main__'):
    #g = SmartFuzzyObject(geotagger(48.8,2.3999999999999773))
    #sys.exit()
    
    def ppArgs():
	pArgs = [(k,args[k]) for k in args.keys()]
	pPretty = PrettyPrint.PrettyPrint('',pArgs,True,' ... ')
	pPretty.pprint()

    args = {'--help':'show some help.',
	    '--verbose':'output more stuff.',
	    '--debug':'debug some stuff.',
	    '--mysql':'use mySQL.',
	    '--limits=?':'use limits, typically for mySQL.',
	    '--etl':'use ETL.',
	    '--threads':'use threads.',
	    '--mongodb=?':'use mongodb named database.',
	    '--mongoip=?':'use mongodb server ip address.',
	    '--mongoport=?':'use mongodb server port.',
	    '--dropdb':'drop the named database.',
	    '--profiler':'use profiler.',
	    '--fpath=?':'file name for input or nothing for default.',
	    }
    __args__ = Args.SmartArgs(args)

    if (len(sys.argv) == 1):
	ppArgs()
    else:
	_progName = __args__.programName
	
	_isVerbose = __args__.get_var('isVerbose',bool,False)
	_isDebug = __args__.get_var('isDebug',bool,False)
	_isHelp = __args__.get_var('isHelp',bool,False)
	_isMySQL = __args__.get_var('isMysql',bool,False)
	_isETL = __args__.get_var('isEtl',bool,False)
	_isProfiler = __args__.get_var('isProfiler',bool,False)
	_isDropDb = __args__.get_var('isDropdb',bool,False)
	_isThreads = __args__.get_var('isThreads',bool,False)

	_fpath = __args__.get_var('fpath',misc.isString,'')
	_mongoip = __args__.get_var('mongoip',misc.isString,'127.0.0.1')
	_mongoport = __args__.get_var('mongoport',int,27017)
	
	_limits = __args__.get_var('limits',int,-1)

	aMongoConnection = None
	_mongodb_dbname = 'sample-data'
	try:
	    __mongodb_dbname = __args__.get_var('mongodb',misc.isString,_mongodb_dbname)
	    _isMONGODB = _has_mondogb
	    if (_isMONGODB):
		try:
		    aMongoConnection = mongoConnection(_mongoip, _mongoport)
		    db = aMongoConnection[_mongodb_dbname]
		    if (db):
			if (_isDropDb):
			    aMongoConnection.drop_database(db)
			db.logout()
		    else:
			print >>sys.stderr, 'WARNING: Cannot use the mongo database named "%s".' % (_mongodb_dbname)
		except Exception, ex:
		    info_string = _utils.formattedException(details=ex)
		    print >>sys.stderr, info_string
		    aMongoConnection = None
		    _isMONGODB = False
	except Exception, e:
	    _isMONGODB = False
	    info_string = _utils.formattedException(details=e)
	    print info_string
	_mongodb_dbname = __mongodb_dbname if (_isMONGODB) else None
	
	if (os.path.exists(_fpath)):
	    print 'Reading XML from "%s".' % (_fpath)
	    x = _utils.readFileFrom(_fpath)
	    try:
		j = xml_to_json(x)
		if (ObjectTypeName.typeClassName(j) not in ['str','unicode']):
		    raise ValueError, 'Wrong value...'
	    except Exception, e:
		try:
		    write_xml_for_into(x,_fpath)
		    x = _utils.readFileFrom(_fpath)
		    j = xml_to_json(x)
		except:
		    print >>sys.stderr, 'ERROR: Cannot continue...'
		    sys.exit(101)
	    d = json_to_python(j)
	    geotagger_on(d)
	    try:
		_json = smsi_json_from(d['RECORDS']['RECORD'])
		_fext = list(os.path.splitext(_fpath))
		_fext[-1] = '.json'
		_fpath3 = '%s-json%s' % tuple(_fext)
		print 'Writing JSON to "%s".' % (_fpath3)
		_utils.writeFileFrom(_fpath3,_json)
	    except Exception, e:
		info_string = _utils.formattedException(details=e)
		print info_string
	    _xml = python_to_xml(d)
	    _fpath2 = '%s@%s' % os.path.splitext(_fpath)
	    print 'Writing XML to "%s".' % (_fpath2)
	    _utils.writeFileFrom(_fpath2,_xml)
	    pass
	elif (_isMySQL):
	    if (_isProfiler):
		import cProfile
		cProfile.run('process_mySQL()')
	    else:
		process_mySQL()
	else:
	    print 'Using the default behavior...'
	    for item in __data_nodes_:
		d = SmartFuzzyObject(item)
		write_data_for(d.name,d.num)
	
        