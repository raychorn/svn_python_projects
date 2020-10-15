import random

__data__ = []

for i in xrange(20):
    __data__.append({'a':i+1,'b':random.choice(['a','b','c','d']),'type':random.choice(['Linux','Windows'])})

print 'BEGIN: (unsorted)'
for data in __data__:
    print str(data)
print 'END!!!'

print 'First sort by "type".'

def sort_by_field_type(a,b):
    key = 'type'
    _a_= a.get(key,'')
    _b_ = b.get(key,'')
    result = -1 if (_a_ < _b_) else 1 if (_a_ > _b_) else 0
    return result

__data__.sort(cmp=sort_by_field_type)

print
print 'BEGIN: (primary sort is "type")'
for data in __data__:
    print str(data)
print 'END!!!'
print
print 'As you can see this groups all the like "type" records together.'
print
print 'The next sort does NOT act upon the whole sorted list, rather it acts upon each sub-list within the whole list.' 

__types__ = list(set([item.get('type','') for item in __data__]))

print
print 'BEGIN: (list of types)'
for data in __types__:
    print str(data)
print 'END!!!'
print

__groups__ = []

for aType in __types__:
    __groups__.append([item for item in __data__ if (item.get('type','') == aType)])
    
print
print 'BEGIN: (list of groups)'
for group in __groups__:
    if (isinstance(group,list)):
        print 'BEGIN-TYPE: %s' % (group[0].get('type',''))
        for item in group:
            print '\t%s' % (str(item))
        print 'END-TYPE: %s' % (group[0].get('type',''))
    else:
        print str(group)
print 'END!!!'
print

print 'As you can see each group has only those items for each group by type.'
print
print 'Now we apply the next sort to each group as-if each group is a separate list.'
print

def sort_by_field_b(a,b):
    key = 'b'
    _a_= a.get(key,'')
    _b_ = b.get(key,'')
    result = -1 if (_a_ < _b_) else 1 if (_a_ > _b_) else 0
    return result

for i in xrange(len(__groups__)):
    group = __groups__[i]
    if (isinstance(group,list)):
        group.sort(cmp=sort_by_field_b)
        __groups__[i] = group

print
print 'BEGIN: (list of groups)'
for group in __groups__:
    if (isinstance(group,list)):
        print 'BEGIN-TYPE: %s' % (group[0].get('type',''))
        for item in group:
            print '\t%s' % (str(item))
        print 'END-TYPE: %s' % (group[0].get('type',''))
    else:
        print str(group)
print 'END!!!'
print

print 'As you can see each sub-group has been sorted as a separate sub-group.'
print

print 'This process would be repeated for as many stacked options as the user specified'
print 'with each succesive sort being applied to an ever-shrinking list of records'
print 'as was done in this short example.'
print
print 'Of course, one would want to make this algorithm into an Object represented as a Class to better encapsulate the behaviors.'
print
print 'This is what one would want the SQL code to do if this is being done by SQL by a single dynamically created statement at run-time.'
