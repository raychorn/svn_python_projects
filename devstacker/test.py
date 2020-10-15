import re
import yaml
import os, sys

from vyperlogix.classes.SmartObject import SmartObject

__tasks__ = ['tasks']
__vars__ = ['vars']

__re__ = re.compile(r"\{\{\s*(?P<value>.*)\s*\}\}", re.DOTALL | re.MULTILINE)

__re2__ = re.compile("(?P<name>.*)=(?P<value>.*)", re.DOTALL | re.MULTILINE)

fpath = os.path.abspath('./devstack.yaml')
stream = open(fpath, 'r')
__dict__ = yaml.load(stream)
#print __dict__

from vyperlogix.iterators.dict import dictutils

__vars__ = __dict__[0].get(__vars__[0],{})

__data__ = SmartObject()
task_name = lambda task,bucket:'%s %s' % (len(bucket),task.get('name','UNDEFINED'))
for k,v in dictutils.walk(__dict__,options=dictutils.DictWalkOptions.keys_and_values):
    if (k in __tasks__):
        if (__data__[k] == None):
            __data__[k] = SmartObject()
        for task in v:
            __key__ = task_name(task,__data__[k])
            if (__data__[k][__key__] == None):
                __data__[k][__key__] = SmartObject()
            print '-'*30
            for kk,vv in dictutils.walk(task,options=dictutils.DictWalkOptions.keys_and_values):
                while (1):
                    for var in __vars__:
                        toks = str(vv).split('{{ %s }}' % (var))
                        if (len(toks) > 1):
                            value = __vars__.get(var,None)
                            if (value):
                                vv = value.join(toks)
                            continue
                    break
                if (kk != 'name'):
                    toks = str(vv).split()
                    if (len(toks) > 2):
                        print 'WARNING: Work on this --> "%s"' % (vv)
                    for t in toks:
                        m = __re2__.search(t)
                        if (m and m.groupdict()):
                            for kkk,vvv in m.groupdict().iteritems():
                                __data__[k][__key__][kkk] = vvv
                else:
                    __data__[k][__key__][kk] = vv
                print '%s:\n%s' % (kk,vv)
                print
            print '-'*30
            print

print '='*40
        
    