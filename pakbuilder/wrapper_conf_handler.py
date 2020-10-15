import os, sys

from vyperlogix import misc

from vyperlogix.misc import _utils

from vyperlogix.lists.ListWrapper import ListWrapper

from vyperlogix.hash.lists import HashedLists, HashedLists2

from vyperlogix.classes.SmartObject import SmartObject

from vyperlogix.iterators.dict import dictutils

import re
__regex_wrapper_conf__ = re.compile(r"(?P<variable>.*\..*)=(?P<value>.*)", re.DOTALL | re.MULTILINE)

def parse_and_resequence_wrapper_conf(source):
    fOut = _utils.stringIO()
    
    __keys__ = ['wrapper','java','additional']
    __required__ = ['=-Xdebug','=-Xrunjdwp:']

    __normalize__ = lambda bucket:bucket[0] if (misc.isIterable(bucket)) else bucket
    normalize = lambda bucket,key:__normalize__(bucket[key])
    __unpack__ = lambda bucket,index:bucket[index] if (misc.isTuple(bucket)) else bucket
    _unpack_ = lambda bucket,index:bucket[index] if (misc.isIterable(bucket)) else bucket
    unpack = lambda item:__unpack__(item,0)
    regex_result = lambda item:__unpack__(item,1)
    boolean_result = lambda item:__unpack__(item,2)
    smartObject = lambda item:__unpack__(item,3)
    line_index = lambda item:__unpack__(item,4)
    unload = lambda item:unpack(item) if (misc.isTuple(item)) else unpack(__normalize__(item)) if (misc.isList(item)) else item
    loc_from_collection_item = lambda item:__unpack__(_unpack_(item,1),0)
    line_index_from_collection_item = lambda item:line_index(_unpack_(item,1))

    def __repack__(bucket,index,value):
        if (misc.isIterable(bucket)):
            bucket[index] = value
    
    set_smartObject = lambda item,value:__repack__(item,3,value)
    set_line_index = lambda item,value:__repack__(item,4,value)

    lines = []
    if (misc.isIterable(source) and ( (len(source) == 0) or (len(source) > 1) ) ):
        lines = source
    else:
        lines = source.split('\n')
    lines = [l.strip() for l in lines if (len(l.strip()) > 0)]
    errors = [l.strip() for l in lines if (l.strip().find('No such file or directory') > -1)]
    if (len(errors) > 0):
        print 'Cannot proceed without a valid wrapper.conf file for the collector.'
    else:
        __lines__ = []
        for _i_ in xrange(0,len(lines)):
            l = lines[_i_]
            m = __regex_wrapper_conf__.search(l)
            so = SmartObject(args=m.groupdict() if (m) else {})
            if (m):
                toks = l.split('=')
                so.variable = toks[0]
                so.value = '='.join(toks[1:])
                while (so.variable and so.variable.startswith('#')):
                    if (so.variable and so.variable.startswith('#')):
                        so.variable = so.variable[1:]
                    else:
                        break
                __lines__.append((l,m,l.startswith('#'),so,_i_))
        __lines__ = ListWrapper(__lines__)

        def contains_search_in_values(_item,_search):
            _f_ = False
            try:
                so = smartObject(_item)
                if (_item[1] is not None) and (so is not None) and (so.value is not None) and (so.value.find(_search) > -1):
                    _f_ = True
            except:
                pass
            return _f_

        def contains_search_in_variables(_item,_search):
            _f_ = False
            try:
                so = smartObject(_item)
                if (_item[1] is not None) and (so is not None) and (so.variable is not None) and (so.variable.find(_search) > -1):
                    #print 'DEBUG: %s' % (_item[0])
                    _f_ = True
            except:
                pass
            return _f_
        
        _f_ = __lines__.findFirstMatching('-Xdebug',callback=contains_search_in_values)
        if (_f_ > -1):
            t = __lines__[_f_]
            so = smartObject(t)
            toks = so.variable.split('.')
            v = '.'.join(toks[0:-1])
            v += '.'
            print 'Find all containing "%s".' % (v)
            __indexes2__ = __lines__.findAllContaining(v,callback=contains_search_in_variables,returnIndexes=True,itemHandler=unpack)
            print 'Found lines %s through %s.' % (__indexes2__[0],__indexes2__[-1])
            __delta__ = __indexes2__[0]
            __lines2__ = ListWrapper(__lines__[__indexes2__[0]:__indexes2__[-1]+1])
            assert len(__lines2__) == len(__indexes2__), 'Something is wrong with your logic #1.'
            _f2_ = __lines2__.findFirstMatching('-Xdebug',callback=contains_search_in_values)
            if (_f2_ > -1):
                d = HashedLists()
                for _i_ in xrange(0,len(__lines2__)):
                    l = __lines2__[_i_]
                    #print 'Considering %s.' % (l[0])
                    so = smartObject(l)
                    toks = so.variable.split('.')
                    bucket = d
                    for i in xrange(0,len(toks)):
                        key = toks[i]
                        if (i < (len(toks)-(0 if (str(toks[-1]).isdigit()) else 1))): # if (i < (len(toks)-1)):
                            if (not bucket[key]):
                                bucket[key] = HashedLists()
                            __bucket__ = normalize(bucket,key)
                            if (not misc.isDict(__bucket__)):
                                __list__ = bucket[key]
                                del bucket[key]
                                bucket[key] = HashedLists()
                                for _l_ in __list__:
                                    bucket[key] = _l_
                                __bucket__ = normalize(bucket,key)
                            bucket = __bucket__
                    #print 'DEBUG: key=%s' % (key)
                    bucket[key] = l
                bucket = d
                for k in __keys__:
                    bucket = normalize(bucket,k)
                    if (not bucket):
                        break
                if (bucket):
                    __analysis__ = HashedLists()
                    __sequence__ = [int(k) for k in bucket.keys() if (str(k).isdigit())]
                    misc.sort(__sequence__)
                    items = []
                    for k in __sequence__:
                        v = bucket[k]
                        for _v_ in v:
                            if (not misc.isHashedDict(_v_)):
                                items.append(tuple([k,_v_]))
                                so = smartObject(_v_)
                                __analysis__[so.variable] = __normalize__(v)
                            else:
                                for _k_,_v_ in _v_.iteritems():
                                    for _vv_ in _v_:
                                        items.append(tuple([k,_vv_]))
                                        so = smartObject(_vv_)
                                        __analysis__[so.variable] = _vv_
                    collisions = []
                    dups = []
                    __dups__ = []
                    __collisions__ = []
                    for item in items:
                        k = item[0]
                        so = smartObject(item[-1])
                        if (so.variable not in collisions):
                            collisions.append(so.variable)
                            __collisions__.append(item[-1])
                        else:
                            dups.append(so.variable)
                            _c_ = [cc for cc in __collisions__ if (smartObject(cc).variable == so.variable)]
                            misc.append(__dups__,_c_)
                            __dups__.append(item[-1])
                        print '%s --> %s --> %s' % (k,so.variable,item)
                    for k in __dups__:
                        print 'DUPE: %s' % (str(k))
                    __collection__ = []
                    for k,v_items in __analysis__.iteritems():
                        for v in v_items:
                            __is__ = not misc.isTuple(v)
                            _v_ = v[v.keys()[0]][0] if (__is__) else v
                            _i_ = line_index(_v_)
                            __has__ = False
                            for item in __dups__:
                                _l_ = line_index(item)
                                if (_l_ == _i_):
                                    __has__ = True
                                    break
                            print 'ANALYSIS: %s%s %s --> %s --> %s' % ('(**) ' if (__has__) else '','(+) ' if (__is__) else '',k,_i_,lines[_i_])
                            __collection__.append(tuple([k,_v_]))
                    def keys_comparator(a, b):
                        normalize = lambda item:[int(ch) for ch in item[0].split('.') if (ch.isdigit())][0]
                        __find__ = lambda item,value:item.index(value) if (value in item) else -1
                        has_extension = lambda item,target:__find__(item[0].split('.'),target) == (len(item[0].split('.'))-1)
                        adjust_if_necessary = lambda item,target:(0.1 if (has_extension(item,str(target))) else 0.0)
                        _a_ = normalize(a)
                        _a_ = _a_ - adjust_if_necessary(a,_a_)
                        _b_ = normalize(b)
                        _b_ = _b_ - adjust_if_necessary(b,_b_)
                        return -1 if (_a_ < _b_) else 0 if (_a_ == _b_) else 1
                    __collection__.sort(keys_comparator)
                    __has_required__ = []
                    for item in __collection__:
                        loc = loc_from_collection_item(item)
                        for r in __required__:
                            if (loc.find(r) > -1):
                                __has_required__.append(tuple([r,loc,item]))
                        print item
                    __missing__ = list(set(__required__) -set([h[0] for h in __has_required__]))
                    if (len(__has_required__) != len(__required__)):
                        for h in __has_required__:
                            print 'HAS: %s' % (str(h))
                    assert len(__has_required__) == len(__required__), 'WARNING.1: Some required lines from the wrapper.conf file are missing !!!'
                    if (len(__missing__) > 0):
                        for m in __missing__:
                            print 'MISSING: %s' % (str(m))
                    assert len(__missing__) == 0, 'WARNING.2: Some required lines from the wrapper.conf file are missing !!!'

                    get_sequence_number_from = lambda sample:int(sample[3]) if (sample[0:3] == __keys__) else -1
                    uncollect = lambda sample:sample[0].split('.') if (misc.isTuple(sample)) else []
                    is_commented = lambda sample:sample[1][0].startswith('#') if (misc.isTuple(sample) and (len(sample) > 1) and misc.isTuple(sample[1]) and (len(sample[1]) > 1)) else False
                    is_required = lambda sample:any([unpack(sample[1]).find(r) > -1 for r in __required__]) if (misc.isTuple(sample) and (len(sample) > 1) and misc.isTuple(sample[1]) and (len(sample[1]) > 1)) else False
                    
                    def __resequence_variable__(variable,expected):
                        toks = variable.split('.')
                        toks[len(__keys__)] = '%d' % (expected)
                        return '.'.join(toks)
                    
                    def __resequence_item__(sample,expected):
                        sample = list(sample)
                        sample[0] = __resequence_variable__(sample[0],expected)
                        t = sample[1]
                        so = smartObject(t)
                        so.variable = __resequence_variable__(so.variable,expected)
                        sample[1] = list(sample[1])
                        set_smartObject(sample[1],so)
                        value = '%s=%s' % (so.variable,so.value)
                        __repack__(sample[1],0,value)
                        sample[1] = tuple(sample[1])
                        return tuple(sample)
                        
                    
                    def __resequence_items__(samples,expected):
                        for i in xrange(0,len(samples)):
                            sample = samples[i]
                            sample = __resequence_item__(sample, expected)
                            expected += 1
                            samples[i] = sample
                        return samples
                    
                    print 'BEGIN: RESEQUENCE'
                    i = 0
                    expected_number = 1
                    while (1):
                        max_expected_number = get_sequence_number_from(uncollect(__collection__[-1]))
                        if (expected_number <= max_expected_number):
                            __items__ = [c for c in __collection__ if (get_sequence_number_from(uncollect(c)) == expected_number)]
                            num_toks_simple_item = len(__keys__)+1
                            __simple_items__ = [c for c in __items__ if (len(uncollect(c)) == num_toks_simple_item)]
                            __simple_items__ = [c for c in __simple_items__ if (is_required(c)) or (not is_commented(c))]
                            if (len(__items__) > 0):
                                item = __collection__[i]
                                toks = item[0].split('.')
                                s = get_sequence_number_from(toks)
                                assert s > -1, 'WARNING: Something went wrong with your re-sequence thingy.'
                            else:
                                break
                            if (len(__simple_items__) > 1):
                                __adjustable_items__ = [c for c in __collection__ if (get_sequence_number_from(uncollect(c)) >= expected_number)]
                                __adjustable_items__ = __resequence_items__(__adjustable_items__, expected_number)
                                adjustable_items = (t for t in __adjustable_items__)
                                coll = ListWrapper(__collection__)
                                def __callback__(item,search):
                                    return get_sequence_number_from(uncollect(item)) == search
                                _f_ = coll.findFirstMatching(expected_number, callback=__callback__, returnIndexes=True)
                                if (_f_ > -1):
                                    for i in xrange(_f_,_f_+len(__adjustable_items__)):
                                        __collection__[i] = adjustable_items.next()
                                print '(!!!)'
                        else:
                            break
                        expected_number += 1
                    print 'END:   RESEQUENCE'
                    print 'BEGIN: FINAL SEQUENCE'
                    for item in __collection__:
                        loc = loc_from_collection_item(item)
                        for r in __required__:
                            if (loc.find(r) > -1):
                                __has_required__.append(tuple([r,loc,item]))
                        li = line_index_from_collection_item(item)
                        print '%s --> %s' % (li,item)
                    print 'END:   FINAL SEQUENCE'
                    i1 = line_index_from_collection_item(__collection__[0])
                    i2 = line_index_from_collection_item(__collection__[-1])
                    print 'INFO: i1=%s, i2=%s' % (i1,i2)
                    print 'BEGIN: ORIGINAL SOURCE'
                    for i in xrange(i1,i2+1):
                        item = lines[i]
                        print '%s' % (str(item))
                    print 'END:   ORIGINAL SOURCE'
                    new_lines = []
                    for item in lines[0:i1]:
                        new_lines.append(item)
                    for item in __collection__:
                        loc = loc_from_collection_item(item)
                        new_lines.append(loc)
                    for item in lines[i2+1:]:
                        new_lines.append(item)
                    print 'BEGIN: ADJUSTED SOURCE'
                    for item in new_lines:
                        print >>fOut, '%s' % (str(item))
                    print 'END:   ADJUSTED SOURCE'
    return fOut.getvalue()

def parse_and_resequence(fpath):
    contents = []
    if (os.path.exists(fpath)):
        fIn = open(fpath)
        contents = fIn.readlines()
        fIn.close()
    return parse_and_resequence_wrapper_conf(contents)

if (__name__ == '__main__'):
    responses = '''
#include %ALIVE_BASE%/user/conf/collector/wrapper-license.conf
#include %ALIVE_BASE%/user/conf/email.properties

# Java Application
wrapper.java.command=%ALIVE_BASE%/jre/bin/java

wrapper.ignore_sequence_gaps=TRUE

# Java Main class.  This class must implement the WrapperListener interface
#  or guarantee that the WrapperManager class is initialized.  Helper
#  classes are provided to do this for you.  See the Integration section
#  of the documentation for details.
wrapper.java.mainclass=com.integrien.alive.collector.CollectorMain

# Java Classpath (include wrapper.jar)  Add class path elements as
#  needed starting from 1
wrapper.java.classpath.1=%ALIVE_BASE%/collector/lib/vcops-collector-1.0-SNAPSHOT.jar
wrapper.java.classpath.2=%ALIVE_BASE%/common/lib/wrapper.jar
wrapper.java.classpath.3=%ALIVE_BASE%/common/lib/junit.jar
wrapper.java.classpath.4=%ALIVE_BASE%/common/lib/alive_common.jar
wrapper.java.classpath.5=%ALIVE_BASE%/common/lib/xerces.jar
wrapper.java.classpath.6=%ALIVE_BASE%/common/lib/log4j-1.2.14.jar
wrapper.java.classpath.7=%ALIVE_BASE%/common/lib/commons-lang-2.3.jar
wrapper.java.classpath.8=%ALIVE_BASE%/collector/lib/joda-time-1.4.jar
wrapper.java.classpath.9=%ALIVE_BASE%/common/lib/activemq-all-5.5.0.jar
wrapper.java.classpath.10=%ALIVE_BASE%/common/lib/commons-logging-1.1.jar
wrapper.java.classpath.11=%ALIVE_BASE%/collector/lib/ireasoningsnmp.jar
wrapper.java.classpath.12=%ALIVE_BASE%/common/lib/commons-configuration-1.6.jar
wrapper.java.classpath.13=%ALIVE_BASE%/common/lib/commons-collections-3.1.jar
wrapper.java.classpath.14=%ALIVE_BASE%/common/lib/mail.jar
wrapper.java.classpath.15=%ALIVE_BASE%/common/lib/activation.jar
wrapper.java.classpath.16=%ALIVE_BASE%/common/lib/alive_platform.jar
wrapper.java.classpath.17=%ALIVE_BASE%/common/lib/slf4j-log4j12-1.5.11.jar
wrapper.java.classpath.18=%ALIVE_BASE%/collector/lib/commons-discovery-0.4.jar
wrapper.java.classpath.19=%ALIVE_BASE%/collector/lib/axis-1.4.jar
wrapper.java.classpath.20=%ALIVE_BASE%/collector/lib/jaxrpc-api-1.1.jar
wrapper.java.classpath.21=%ALIVE_BASE%/collector/lib/vmware_wsdl4j-1.6.2.jar
wrapper.java.classpath.22=%ALIVE_BASE%/common/lib/vcops-vc-common.jar

# Java Library Path (location of Wrapper.DLL or libwrapper.so)
wrapper.java.library.path.1=%ALIVE_BASE%/common/bin

# Java Additional Parameters
wrapper.java.additional.1=-DALIVE_BASE="%ALIVE_BASE%"
wrapper.java.additional.1.stripquotes=TRUE
wrapper.java.additional.2=-Djava.security.policy="%ALIVE_BASE%/user/conf/policy"
wrapper.java.additional.2.stripquotes=TRUE
wrapper.java.additional.3=-XX:MaxPermSize=196m
wrapper.java.additional.4=-Djava.protocol.handler.pkgs=jcifs
wrapper.java.additional.5=-Dcom.ireasoning.configDir="%ALIVE_BASE%/user/conf"
wrapper.java.additional.5.stripquotes=TRUE
#wrapper.java.additional.6=-XX:+UseGCOverheadLimit
wrapper.java.additional.6=-XX:+UseParallelOldGC
wrapper.java.additional.7=-da
wrapper.java.additional.8=-Djava.rmi.server.hostname=%RMI_ADDRESS%
wrapper.java.additional.9=-XX:+HeapDumpOnOutOfMemoryError
wrapper.java.additional.10=-XX:HeapDumpPath=/data/heapdump/
wrapper.java.additional.11=-XX:OnOutOfMemoryError="/usr/lib/vmware-vcops/user/conf/install/oom-handler.sh %p"
wrapper.java.additional.11.stripquotes=TRUE
wrapper.java.additional.12=-XX:ErrorFile=/data/vcops/log/java/java_error%p.log
wrapper.java.additional.13=-XX:+DisableExplicitGC
wrapper.java.additional.14=-Dun.rmi.dgc.client.gcInterval=3600000
wrapper.java.additional.15=-Djdk.xml.entityExpansionLimit=0


# Java debugging options. Enable them when required. Keep the sequence numbering consistent
#wrapper.java.additional.15=-Xdebug
#wrapper.java.additional.16=-Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8004

wrapper.ping.timeout=600
wrapper.ping.interval=60
wrapper.startup.timeout=120
wrapper.on_exit.default=RESTART


# Initial Java Heap Size (in MB)
wrapper.java.initmemory=128

# Maximum Java Heap Size (in MB)
wrapper.java.maxmemory=

# Application parameters.  Add parameters as needed starting from 1
#wrapper.app.parameter.1=

#********************************************************************
# Wrapper Logging Properties
#********************************************************************
# Format of output for the console.  (See docs for formats)
wrapper.console.format=PM

# Log Level for console output.  (See docs for log levels)
wrapper.console.loglevel=INFO

# Log file to use for wrapper output logging.
wrapper.logfile=%ALIVE_BASE%/user/log/collector-wrapper.log

# Format of output for the log file.  (See docs for formats)
wrapper.logfile.format=LPTM

# Log Level for log file output.  (See docs for log levels)
wrapper.logfile.loglevel=ERROR

# Maximum size that the log file will be allowed to grow to before
#  the log is rolled. Size is specified in bytes.  The default value
#  of 0, disables log rolling.  May abbreviate with the 'k' (kb) or
#  'm' (mb) suffix.  For example: 10m = 10 megabytes.
wrapper.logfile.maxsize=1024k

# Maximum number of rolled log files which will be allowed before old
#  files are deleted.  The default value of 0 implies no limit.
wrapper.logfile.maxfiles=5

# Log Level for sys/event log output.  (See docs for log levels)
wrapper.syslog.loglevel=NONE

#********************************************************************
# Wrapper Windows Properties
#********************************************************************
# Title to use when running as a console
wrapper.console.title=CollectorService

#********************************************************************
# Wrapper Windows NT/2000/XP Service Properties
#********************************************************************
# WARNING - Do not modify any of these properties when an application
#  using this configuration file has been installed as a service.
#  Please uninstall the service before modifying this section.  The
#  service can then be reinstalled.

# Name of the service
wrapper.ntservice.name=CollectorService

# Display name of the service
wrapper.ntservice.displayname=CollectorService

# Description of the service
wrapper.ntservice.description=CollectorService

# Service dependencies.  Add dependencies as needed starting from 1
wrapper.ntservice.dependency.1=

# Mode in which the service is installed.  AUTO_START or DEMAND_START
wrapper.ntservice.starttype=AUTO_START

# Allow the service to interact with the desktop.
wrapper.ntservice.interactive=false
    '''
    fOut = open('wrapper.conf', 'w')
    print >>fOut, '%s' % (responses)
    fOut.flush()
    fOut.close()
    
    fname = fOut.name
    
    output1 = parse_and_resequence_wrapper_conf(responses)
    print output1
    
    output2 = parse_and_resequence(fname)
    print output2
    
    assert output1 == output2, 'Better check your logic. This one has problems.'
    
    print 'All is well !!!'
