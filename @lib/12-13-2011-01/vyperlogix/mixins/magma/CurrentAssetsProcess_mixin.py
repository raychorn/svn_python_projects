import wx

import os, sys
from vyperlogix import misc
from vyperlogix.misc import _utils
from vyperlogix.misc import ObjectTypeName
from vyperlogix.parsers.CSV import CSV
from vyperlogix.hash import lists

class CurrentAssetsProcessMixin():
    def CurrentAssetsProcessMixin_init(self):
	self.__sf_login_model = None
	self.__competitors_list = []
	self._csv_model = None
	self._log_path = None

    def sf_login_model():
        doc = "sf_login_model"
        def fget(self):
            return self.__sf_login_model
        def fset(self, sf_login_model):
            self.__sf_login_model = sf_login_model
        return locals()
    sf_login_model = property(**sf_login_model())
    
    def competitors_list():
        doc = "competitors_list"
        def fget(self):
	    if (len(self.__competitors_list) == 0):
		self.__competitors_list = [item.lower() if (not isinstance(item,tuple)) and (not isinstance(item,list)) else list(item)[0].lower() for item in self._getCompetitorsList()]
            return self.__competitors_list
        return locals()
    competitors_list = property(**competitors_list())
    
    def _getCompetitorsList(self):
	self.last_error = ''
	try:
	    from vyperlogix.sf.sf import SalesForceQuery
	    sfQuery = SalesForceQuery(self.sf_login_model)
	    from vyperlogix.sf.magma.competitors import SalesForceMagmaCompetitors
	    competitors = SalesForceMagmaCompetitors(sfQuery)
	    c_list = competitors.getCompetitorsList()
    
	    data = [] # tuple(['One']),tuple(['Two']),tuple(['Three'])
	    if (c_list is not None):
		for item in c_list:
		    data.append(tuple([str(item['Company_Name__c']).lower()]))
	except Exception, details:
	    self.last_error = _utils.formattedException(details=details)
	return data

    def backgroundProcess(self,wxParent):
	'''wxParent is the object instance for the wxPython Frame instance for the app that runs this process or a suitable replacement thereof'''
	try:
	    wxParent.number = 100 # signal the elapsed read-out to begin working...
	    wxParent.count = 1 # signal the elapsed read-out to begin working...
	    wxParent.append_to_message_Q('Init SalesForce Interface.')
	    from vyperlogix.sf.sf import SalesForceQuery
	    sfQuery = SalesForceQuery(self.__login_dialog__.sf_login_model)
	    from vyperlogix.sf.assets import SalesForceAssets
	    wxParent.append_to_message_Q('Issue SOQL for List of Assets.')
	    assets = SalesForceAssets(sfQuery)
	    cassets = assets.getCurrentAssets()
	    cassets = cassets if not _utils.isBeingDebugged else cassets[0:10]
	    wxParent.number = len(cassets)
	    wxParent.count = 0
	    for rec in cassets:
		try:
		    aId = rec['AccountId']
		    wxParent.append_to_message_Q('Fetching Contact for AccountId of "%s".' % (aId))
		    contacts = assets.getAccountContacts(aId)
		    wxParent.append_to_message_Q('\tHas %d Contact%s.' % (len(contacts),'(s)' if (len(contacts) > 1) else ''))
		    wxParent.acceptContacts(rec,contacts)
		except Exception, details:
		    _details = _utils.formattedException(details=details)
		    print >>sys.stdout, _details
		    print >>sys.stderr, _details
		    break
		finally:
		    self.count += 1
	    pass
	except Exception, details:
	    _details = _utils.formattedException(details=details)
	    print >>sys.stdout, _details
	    print >>sys.stderr, _details
    
    def _doAfterExtractionProcessCompleted(self):
	alpha_num_only = lambda s:' '.join(''.join([ch if (ch.isalnum()) else ' ' for ch in s if (ch.isalnum()) or (ch in [' ','_','-'])]).split('  '))

	self.number = 2
	self.count = 1
	self.deduped_Contacts = self.dedupeContacts(self.__contacts__)
	self.appendText('%s :: (%d/%d) contacts.' % (ObjectTypeName.objectSignature(self),len(self.deduped_Contacts),len(self.__contacts__)))
	if (not os.path.exists(self._csv_model.filename)):
	    self._csv_model.filename = os.sep.join([self._log_path,'data_raw.csv'])
	self.appendText('%s :: BEGIN: "%s".' % (ObjectTypeName.objectSignature(self),self._csv_model.filename))
	info_string = CSV.write_as_csv(self._csv_model.filename,self.__contacts__)
	if (len(info_string) > 0):
	    self.appendText('%s :: %s-->%s.' % (ObjectTypeName.objectSignature(self),self._csv_model.filename,info_string))
	self.count = 2
	fname = os.sep.join([self._log_path,'data_cleaned.csv'])
	info_string = CSV.write_as_csv(fname,self.deduped_Contacts)

	if (len(info_string) > 0):
	    self.appendText('%s :: %s-->%s.' % (ObjectTypeName.objectSignature(self),fname,info_string))
	self.appendText('%s :: END!   "%s".' % (ObjectTypeName.objectSignature(self),self._csv_model.filename))

    def _doUploadToSalesForce(self):
	from vyperlogix.sf.sf import SalesForceQuery
	sfQuery = SalesForceQuery(self.__login_dialog__.sf_login_model)
	from vyperlogix.sf.magma.customers import SalesForceCustomers
	customers = SalesForceCustomers(sfQuery)
	timestamp = sfQuery.sfdc.getServerTimestamp()
	s_timestamp = str(timestamp)
	schemas = []
	for item in self.deduped_Contacts:
	    contact_id = item['Id']
	    for asset_id in item['Asset_Ids'].split(','):
		schemas.append(customers.new_schema(asset_id,contact_id,s_timestamp))
	customers.createBatch(schemas)
	if (customers.save_result_isValid):
	    self.appendText('%s :: Sucessfully saved the batch of objects to SalesForce.' % (ObjectTypeName.objectSignature(self)))
	else:
	    print >>sys.stderr, '%s :: Un-Sucessfully saved the batch of objects to SalesForce.' % (ObjectTypeName.objectSignature(self))
	pass
    
    def dedupeContacts(self,_contacts):
	from vyperlogix.hash import lists
	d = lists.HashedLists()
	for c in _contacts:
	    d[c['Email']] = lists.HashedLists2(c)
	contacts = []
	ascii_only = _utils.ascii_only
	for k,v in d.iteritems():
	    if (misc.isList(v)):
		assets = lists.HashedLists2()
		for item in v:
		    try:
			for aKey in item.keys():
			    item[aKey] = ascii_only(item[aKey])
			assets[item['Asset_Id']] = item['Asset_Name']
			del item['Asset_Id']
			del item['Asset_Name']
		    except Exception, details:
			info_string = _utils.formattedException(details=details)
			appendText(self.__child_frame.textboxLog,info_string)
		v[0]['Asset_Ids'] = ','.join(misc.sortCopy([item for item in list(set(assets.keys()))]))
		contacts.append(v[0])
	    else:
		try:
		    for aKey in v.keys():
			v[aKey] = ascii_only(v[aKey])
		except:
		    pass
		contacts.append(v)
	return contacts
    
    def acceptContacts(self,asset,contacts):
	clist = self.__competitors_list
	if (misc.isList(contacts)):
	    if (len(contacts) > 0):
		contacts = [c for c in contacts if (c['Email'] is not None) and (c['Email'].split('@')[-1] not in clist)]
		for c in contacts:
		    c['Asset_Name'] = asset['Name']
		    c['Asset_Id'] = asset['Id']
		self.__contacts__ += contacts
	else:
	    info_string = '%s accepts a list of contacts but not when it is of type "%s".' % (ObjectTypeName.objectSignature(self),type(contacts))
	    print >>sys.stderr, info_string
	    try:
		wx_PopUp_Dialog(parent=self.__child_frame,msg=info_string,title='WARNING',styles=wx.ICON_WARNING | wx.CANCEL)
	    except:
		pass
    
