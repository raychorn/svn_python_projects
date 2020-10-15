import os
import sys
from vyperlogix import floatValue
from vyperlogix.oodb import *
import globalVars
from vyperlogix.hash import lists
from vyperlogix.gds import julian
from vyperlogix import QIF

_money_data = lists.HashedLists()

_money_data_checks = lists.HashedLists()

_money_data_years = lists.HashedLists()

def getRequiredYears(qifReader,data,databases):
    missing = {}
    if ( (isinstance(data,dict)) or (isinstance(data,lists.HashedLists)) ):
        names = set([qifReader.getDatabaseFileNameFor(k) for k in data.keys()])
        _missing = list(names.difference(set(databases)))
        for k in data.keys():
            missing[k] = [n for n in _missing if n.find('_%d' % k) > -1][0]
    else:
        print '(getRequiredYears) :: ERROR in the data parameter that is supposed to be of type "dict" but is of type "%s".' % terseClassName(fullClassName(data))
    return missing

def dumpQIFItem(item):
    s = str(item)+'\n'
    return s

def normalizeAmount(value):
    v = '%10.2f' % floatValue.floatValue(value.replace('$','').replace(',',''))
    return v.strip()

def main():
    qifReader = QIF.QifReader(None,None)
    databases = qifReader.databases
    for item in qifReader.items:
        _money_data[item.date[-1]] = item
        if (item.checkNumber):
            _money_data_checks['%d' % item.checkNumber] = item
        _money_data_years[item.yyyy] = item
    numItems = 0
    for k,v in _money_data.iteritems():
        numItems += len(v)
    numChecks = 0
    for k,v in _money_data_checks.iteritems():
        numChecks += len(v)
    item = qifReader.items[-1]
    print 'len(qifReader.items)=(%s)' % (len(qifReader.items))
    print 'len(_money_data)=(%s), numItems=%d' % (len(_money_data),numItems)
    print 'len(_money_data_checks)=(%s), numChecks=%d' % (len(_money_data_checks),numChecks)
    assert len(qifReader.items) == numItems, 'Oops, number of items read "%d" does not match the number of items stored ("%d") by date.' % (len(qifReader.items),numItems)
    print 'item=(%s)' % str(item)
    _item = QIF.QifItem(str(item))
    print '_item=(%s)' % str(_item)
    s_item = str(item)
    s__item = str(_item)
    assert s_item == s__item, 'Oops, something went wrong with the automatic Pickler/Unpickler process for the "%s" class.\n%s\n%s' % (QIF.utils.fullClassName(_item),s_item,s__item)
    item_ser = dumps(item)
    x = loads(item_ser)
    print 'x=(%s)' % (str(x))
    required_years = getRequiredYears(qifReader,_money_data_years,databases)
    for k,v in required_years.iteritems():
        isReadOnly = os.path.exists(v)
        dbx = PickledHash(v,PickleMethods.useSafeSerializer)
        if (not isReadOnly):
            i = 0
            for item in _money_data_years[k]:
                spam = terseClassName(fullClassName(item))
                item_key = '%s_%d' % (spam,i)
                _spam = '_%s' % spam
                dbx[item_key] = item
                _fields = item.__dict__.keys()
                for field in _fields:
                    _field = field
                    if (field.find('__') > -1):
                        field = field.replace('_%s' % spam,'')
                    isNormalizeAmount = field == 'amount'
                    skey = '%s_%d' % (field,i)
                    if ( (field != 'payee') and (field != 'memo') and (field != '__mm') and (field != '__dd') and (field != '__yyyy') and (field != 'order') ):
                        dbx[skey] = item_key
                        _data = item.__dict__[_field]
                        if (field == '__date'):
                            _data = '%02d/%02d/%04d' % tuple([int(n) for n in _data])
                        if (isinstance(_data,list)):
                            for datum in _data:
                                _datum = datum
                                if (isNormalizeAmount):
                                    _datum = normalizeAmount(datum)
                                elif ( (_datum) and (not isinstance(_datum,str)) ):
                                    _datum = str(_datum)
                                _datum = _datum.strip()
                                if ( (_datum) and (len(_datum) > 0) and (isAnyAlphaNumeric(_datum)) and (_datum.find(_spam) == -1) and (_datum not in _fields) ):
                                    dbx[_datum] = dbx.listify(_datum,item_key)
                        else:
                            _datum = str(_data) if _data != None else _data
                            if (isNormalizeAmount):
                                _datum = normalizeAmount(_datum)
                            elif ( (_datum) and (not isinstance(_datum,str)) ):
                                _datum = str(_datum)
                            if ( (_datum) and (len(_datum) > 0) and (isAnyAlphaNumeric(_datum)) and (_datum.find(_spam) == -1) and (_datum not in _fields) ):
                                dbx[_datum] = dbx.listify(_datum,item_key)
                        dbx[skey] = _data
                i += 1
        dbx.sync()
        dbx.dump(dumpQIFItem)
        dbx.close()
        pass
    pass

if (__name__ == '__main__'):
    from vyperlogix import _psyco
    _psyco.importPsycoIfPossible()
    main()
