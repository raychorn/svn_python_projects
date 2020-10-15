run_tests = [2]
if (__name__ == '__main__'):
    import sys
    import rubypythonlib
    if (sys.platform == 'win32'):
        _username = "rhorn@magma-da.com"
        sandbox_password = "Peekab00"
        _password = sandbox_password # validated the fact that Staging only talks to the Sandbox and not Production.
        _token = ''

        #_username = "molten_admin@magma-da.com"
        #_password = "u2cansleepr"
        #_token = "WI2X9JakDlxjcuAofhggFbaf"
        
        if (1 in run_tests):
            # Test #1 :: Create a new object
            _xml = '<bridge username="%s" password="%s" token="%s" staging="1"><create table="Case_Watcher_List__c"><column name="Name" value="+++"/><column name="Email__c" value="rhorn@magma-da.com"/><column name="Case_Watcher__c" value="a0t30000000CsCnAAK"/></create></bridge>' % (_username,_password,_token)
            xml = rubypythonlib.salesForceConnector(_xml)
            print xml
        
        # To-Do:
        # Code the update record function...
        if (3 in run_tests):
            _soql = "Select c.Case_Watcher__c, c.Email__c, c.Id, c.Name from Case_Watcher_List__c c where c.Name = '+++'"
            _xml = '<bridge username="%s" password="%s" token="%s" staging="1"><soql>%s</soql></bridge>' % (_username,_password,_token,_soql)
            xml = rubypythonlib.salesForceConnector(_xml)
            print xml
            print '\n'
            print '='*80
            d = rubypythonlib.xmlToDict(xml)
            ids = [k for k in d.keys() if k != 'data']
            print 'There are %d id(s).' % len(ids)
            _xml = '<bridge username="%s" password="%s" token="%s" staging="1">' % (_username,_password,_token)
            _xml += '<update table="Case_Watcher_List__c">'
            for id in ids:
                _xml += '<item id="%s">' % id
                if (d.has_key(id)):
                    if (d[id].has_key('Name')):
                        _name = d[id]['Name']
                        _name_x = [ch for ch in _name]
                        _name_x[len(_name_x)/2] = chr(ord(_name_x[len(_name_x)/2])+1)
                        _name = ''.join(_name_x)
                        _xml += '<column name="Name" value="%s"/>' % (_name)
                        pass
                _xml += '</item>'
                pass
            _xml += '</update>'
            _xml += '</bridge>'
            print 'Updating %d id(s).' % len(ids)
            xml = rubypythonlib.salesForceConnector(_xml)
            print xml
            print '='*80
            pass
        
        if (2 in run_tests):
            _soql = "Select c.Case_Watcher__c, c.Email__c, c.Id, c.Name from Case_Watcher_List__c c where c.Email__c = 'rhorn@magma-da.com'"
            _xml = '<bridge username="%s" password="%s" token="%s" staging="1"><soql>%s</soql></bridge>' % (_username,_password,_token,_soql)
            xml = rubypythonlib.salesForceConnector(_xml)
            print xml
            print '\n'
            print '='*80
            d = rubypythonlib.xmlToDict(xml)
            ids = [k for k in d.keys() if k != 'data']
            print 'There are %d id(s).' % len(ids)
            _xml = '<bridge username="%s" password="%s" token="%s" staging="1">' % (_username,_password,_token)
            _xml += '<delete table="Case_Watcher_List__c">'
            for id in ids:
                _xml += '<item id="%s"/>' % id
                pass
            _xml += '</delete>'
            _xml += '</bridge>'
            print 'Deleting %d id(s).' % len(ids)
            xml = rubypythonlib.salesForceConnector(_xml)
            print xml
            print '='*80
            pass
        
        if (9 in run_tests):
            # Test #9 :: Process SOQL
            _soql = "Select c.Case_Watcher__c, c.Id, c.LastModifiedDate, c.Name, c.Alias_Email__c, c.Email__c from Case_Watcher_List__c c"
            _xml = '<bridge username="%s" password="%s" token="%s" staging="1"><soql>%s</soql></bridge>' % (_username,_password,_token,_soql)
            xml = rubypythonlib.salesForceConnector(_xml)
            print xml
    
        sys.exit(1)
else:
    print 'Do you have any idea what you are doing ?  Get a grip and figure this out !  NOW !'
