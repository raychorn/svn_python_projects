"""
Copyright 2006 Simon Fell
Portions Copyright 2007, 2008, 2009 Kevin Shuk
All rights reserved

This file (beatbox) is part of pyax.

pyax is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

pyax is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyax.  If not, see <http://www.gnu.org/licenses/>.
"""
__version__ = "0.96pyax"
__author__ = "Simon Fell, Ron Hess. pyax modifications by Kevin Shuk"
__credits__ = "Mad shouts to the sforce posse"

import httplib
import sys
from urlparse import urlparse
from StringIO import StringIO
import gzip
import datetime
import xmltramp as xmltramp
from xmltramp import islst
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import quoteattr
from xml.sax.xmlreader import AttributesNSImpl

from pyax.beatbox.context import Context

# import the right transport
IS_APP_ENGINE = False
try:
    from google.appengine.api import urlfetch
    IS_APP_ENGINE = True
except ImportError:
    import urllib2

# global constants for namespace strings, used during serialization
_partnerNs = "urn:partner.soap.sforce.com"
_sobjectNs = "urn:sobject.partner.soap.sforce.com"
_envNs = "http://schemas.xmlsoap.org/soap/envelope/"
_metadataNs = "http://soap.sforce.com/2006/04/metadata"
_xsi = "http://www.w3.org/2001/XMLSchema-instance"
_wsdl_apexNs = "http://soap.sforce.com/2006/08/apex"
_noAttrs = AttributesNSImpl({}, {})

# global constants for xmltramp namespaces, used to access response data
_tPartnerNS = xmltramp.Namespace(_partnerNs)
_tSObjectNS = xmltramp.Namespace(_sobjectNs)
_tMetadataNS = xmltramp.Namespace(_metadataNs)
_tSoapNS = xmltramp.Namespace(_envNs)
_tWsdlApexNS = xmltramp.Namespace(_wsdl_apexNs)
_tXsiNS = xmltramp.Namespace(_xsi)
_xmlns_attrs = AttributesNSImpl({ (None, u'xmlns'): _metadataNs}, {})
#(None, u'xmlns:ns2'): 'http://soap.sforce.com/2006/04/metadata'

class NoTwistedInstalledError(Exception):
    """Raised when trying use asynchronous calls without Twisted."""

# the main sforce client proxy class
class Client(object):
    def __init__(self, context=None):
        self.sessionId = None
        if context is None:
            context = Context()
        self.context = context

    # login, the serverUrl and sessionId are automatically handled, returns the loginResult structure
    def login(self, username, password, org_id=None):
        del self.context.endpoint # force the endpoint back to the login_endpoint
        tramp = LoginRequest(self.context, username, password, org_id).post()
        lr = tramp[_tSoapNS.Body][0][0]
        self.useSession(str(lr[_tPartnerNS.sessionId]),
                        str(lr[_tPartnerNS.serverUrl]))
        return tramp

    def logout(self):
        return str(AuthenticatedRequest(self.context, self.sessionId,
                                        "logout").post())
        
    # ids can be 1 or a list, returns a single delete result or a list
    def invalidateSessions(self, sessionIds):
        return InvalidateSessionsRequest(self.context, self.sessionId, 
                                         sessionIds).post()
        
    # initialize from an existing sessionId & serverUrl, useful if we're being launched via a custom link    
    def useSession(self, sessionId, serverUrl):
        self.sessionId = sessionId
        self.context.endpoint = serverUrl # set the server-reply api endpoint

    # set the batchSize property on the Client instance to change the batchsize for query/queryMore
    def query(self, soql, callback=None, errback=None):
        return QueryRequest(self.context, self.sessionId,
                            soql).post(callback=callback, errback=errback)

    def queryAll(self, soql, callback=None, errback=None):
        return QueryAllRequest(self.context, self.sessionId,
                               soql).post(callback=callback, errback=errback)

    def queryMore(self, queryLocator, callback=None, errback=None):
        return QueryMoreRequest(self.context, self.sessionId,
                                queryLocator).post(callback=callback,
                                                   errback=errback)

    def search(self, sosl):
        return SearchRequest(self.context, self.sessionId, sosl).post()

    def getUpdated(self, sObjectType, start, end):
        return GetUpdatedRequest(self.context, self.sessionId, sObjectType,
                                 start, end).post()

    def getDeleted(self, sObjectType, start, end):
        return GetDeletedRequest(self.context, self.sessionId, sObjectType,
                                 start, end).post()

    def retrieve(self, fields, sObjectType, ids):
        return RetrieveRequest(self.context, self.sessionId, fields,
                               sObjectType, ids).post()

    # sObjects can be 1 or a list, returns a single save result or a list
    def create(self, sObjects):
        return CreateRequest(self.context, self.sessionId, sObjects).post()

    # sObjects can be 1 or a list, returns a single save result or a list
    def update(self, sObjects):
        return UpdateRequest(self.context, self.sessionId, sObjects).post()

    # sObjects can be 1 or a list, returns a single upsert result or a list
    def upsert(self, externalIdName, sObjects):
        return UpsertRequest(self.context, self.sessionId, externalIdName,
                             sObjects).post()

    # ids can be 1 or a list, returns a single delete result or a list
    def delete(self, ids):
        return DeleteRequest(self.context, self.sessionId, ids).post()

    def executeanonymous(self, codeblock):
        return ExecuteAnonRequest(self.context, self.__serverUrl, 
                                  self.sessionId, codeblock).post()
                                  
    def executeApex(self, method, args, is_array, namespaces, url, 
                    header_ns, sobject_ns):
        ar = ExecuteApexRequest(self.context, self.sessionId, method, args, 
                                is_array, header_ns, sobject_ns)
        #print ar.makeEnvelope()
        return ar.post(apex_webservice_url=url)

    # ids can be 1 or a list, returns a single delete result or a list
    def emptyRecycleBin(self, ids):
        return EmptyRecycleBinRequest(self.context, self.sessionId, ids).post()
        
    # ids can be 1 or a list, returns a single delete result or a list
    def undelete(self, ids):
        return UndeleteRequest(self.context, self.sessionId, ids).post()

    # sObjectTypes can be 1 or a list, returns a single describe result or a list of them
    def describeSObjects(self, sObjectTypes):
        return DescribeSObjectsRequest(self.context, self.sessionId,
                                       sObjectTypes).post()

    def describeGlobal(self):
        return AuthenticatedRequest(self.context, self.sessionId,
                                    "describeGlobal").post()

    def describeLayout(self, sObjectType):
        return DescribeLayoutRequest(self.context, self.sessionId,
                                     sObjectType).post()

    def describeTabs(self):
        return AuthenticatedRequest(self.context, self.sessionId,
                                    "describeTabs").post()

    def getServerTimestamp(self):
        return AuthenticatedRequest(self.context, self.sessionId,
                                     "getServerTimestamp").post()

    def resetPassword(self, userId):
        return ResetPasswordRequest(self.context, self.sessionId, userId).post()

    def setPassword(self, userId, password):
        SetPasswordRequest(self.context, self.sessionId, userId,
                           password).post()

    def getUserInfo(self):
        return AuthenticatedRequest(self.context, self.sessionId,
                                    "getUserInfo").post()

#    def _invoke(self, method, args, is_array, namespaces, url,
#                    header_ns, sobject_ns):
#        ar = ApexRequest(self.context, self.sessionId, method, args, is_array,
#                         header_ns, sobject_ns)
#        #print ar.makeEnvelope()
#        return ar.post(apex_webservice_url=url)

    # TODO
    #def convertLead(self, convertLeads):

    #def merge(self, ):
    
    
# fixed version of XmlGenerator, handles unqualified attributes correctly
class BeatBoxXmlGenerator(XMLGenerator):
    def __init__(self, destination, encoding):
        XMLGenerator.__init__(self, destination, encoding)

    def makeName(self, name):
        if name[0] is None:
            #if the name was not namespace-scoped, use the qualified part
            return name[1]
        # else try to restore the original prefix from the namespace
        return self._current_context[name[0]] + ":" + name[1]

    def startElementNS(self, name, qname, attrs):
        self._out.write('<' + self.makeName(name))

        for pair in self._undeclared_ns_maps:
            self._out.write(' xmlns:%s="%s"' % pair)
        self._undeclared_ns_maps = []

        for (name, value) in attrs.items():
            self._out.write(' %s=%s' % (self.makeName(name), quoteattr(value)))
        self._out.write('>')

    def writeAdHoc(self, content):
        self._out.write(content)

# general purpose xml writer, does a bunch of useful stuff above & beyond XmlGenerator
class XmlWriter:
    def __init__(self, doGzip):
        self.__buf = StringIO("")
        if doGzip:
            self.__gzip = gzip.GzipFile(mode='wb', fileobj=self.__buf)
            stm = self.__gzip
        else:
            stm = self.__buf
            self.__gzip = None
        self.xg = BeatBoxXmlGenerator(stm, "utf-8")
        self.xg.startDocument()
        self.__elems = []

    def startPrefixMapping(self, prefix, namespace):
        self.xg.startPrefixMapping(prefix, namespace)

    def endPrefixMapping(self, prefix):
        self.xg.endPrefixMapping(prefix)

    def startElement(self, namespace, name, attrs = _noAttrs):
        self.xg.startElementNS((namespace, name), name, attrs)
        self.__elems.append((namespace, name))

    # if value is a list, then it writes out repeating elements, one for each value
    def writeStringElement(self, namespace, name, value, attrs = _noAttrs):
        if islst(value):
            for v in value:
                self.writeStringElement(namespace, name, v, attrs)
        else:
            self.startElement(namespace, name, attrs)
            self.characters(value)
            self.endElement()

    def writeAdHoc(self, content):
        self.xg.writeAdHoc(content)

    def endElement(self):
        e = self.__elems[-1];
        self.xg.endElementNS(e, e[1])
        del self.__elems[-1]

    def characters(self, s):
        # todo base64 ?
        if isinstance(s, datetime.datetime):
            # todo, timezones
            s = s.isoformat()
        elif isinstance(s, datetime.date):
            # todo, try isoformat
            s = "%04d-%02d-%02d" % (s.year, s.month, s.day)
        elif isinstance(s, int):
            s = str(s)
        elif isinstance(s, float):
            s = str(s)
        self.xg.characters(s)

    def endDocument(self):
        self.xg.endDocument()
        if (self.__gzip != None):
            self.__gzip.close();
        return self.__buf.getvalue()

# exception class for soap faults
class SoapFaultError(Exception):
    def __init__(self, faultCode, faultString):
        self.faultCode = faultCode
        self.faultString = faultString

    def __str__(self):
        return repr(self.faultCode) + " " + repr(self.faultString)


class SessionTimeoutError(Exception):
    """SessionTimeouts are recoverable errors, merely needing the creation
       of a new connection, we create a new exception type, so these can 
       be identified and handled seperately from SoapFaultErrors
    """
    def __init__(self, faultCode, faultString):
        self.faultCode = faultCode
        self.faultString = faultString
    
    def __str__(self):
        return repr(self.faultCode) + " " + repr(self.faultString)


# soap specific stuff ontop of XmlWriter
class SoapWriter(XmlWriter):
    def __init__(self, context, *args):
        self.namespace_pairs = list(args)
        XmlWriter.__init__(self, context.gzip_request)
        for ns_tuple in self.namespace_pairs:
            (prefix, namespace) = ns_tuple
            self.startPrefixMapping(prefix, namespace)
        self.startElement(_envNs, "Envelope")

    def endDocument(self):
        self.endElement()  # envelope)
        self.namespace_pairs.reverse()
        for ns_tuple in self.namespace_pairs:
            (prefix, namespace) = ns_tuple
            self.endPrefixMapping(prefix)

        return XmlWriter.endDocument(self)

# processing for a single soap request / response
class SoapEnvelope:
    def __init__(self, context, operationName, 
                 clientId="BeatBox/" + __version__, namespace=_partnerNs):
        self.context = context
        self.operationName = operationName
        self.clientId = clientId
        self.namespace = namespace
        self.meta = False 
        
    def writeHeaders(self, writer):
        pass

    def writeBody(self, writer):
        pass

    def makeEnvelope(self):
        s = SoapWriter(self.context,
                       ("s", _envNs), 
                       ("p", _partnerNs),
                       ("m", _metadataNs), 
                       ("o", _sobjectNs),
                       ("w", _wsdl_apexNs),
                       ("xsi", _xsi))
        s.startElement(_envNs, "Header")
        s.characters("\n")
        s.startElement(_partnerNs, "CallOptions")
        s.writeStringElement(_partnerNs, "client", self.clientId)
        s.endElement()
        s.characters("\n")
        self.writeHeaders(s)
        s.endElement()    # Header
        s.startElement(_envNs, "Body")
        s.characters("\n")
        if ( self.meta ):
            s.startElement(None, self.operationName, _xmlns_attrs) 
        else:
            s.startElement(self.namespace , self.operationName)
        self.writeBody(s)
        s.endElement()  # operation
        s.endElement()  # body
        return s.endDocument()

    def _cbReceivedResponse(self, response, callback, factory):
        headers = factory.response_headers
        # Convert Twisted headers to urllib convention
        for key, value in headers.items():
            if isinstance(value, list):
                headers[key] = ",".join(value)
        response = self.parseResponse(response, headers)
        callback(response)

    def _ebReceivedResponse(self, failure):
        from twisted.internet import reactor
        sys.stderr.write("An error has occurred: <%s>" % str(failure))
        reactor.stop()

    def checkTwistedPresence(self):
        """Raise NoTwistedInstalledError if twisted is not in sys.path."""
        try:
            import twisted
        except ImportError:
            raise NoTwistedInstalledError()

    def _makeAsyncRequest(self, url, data, headers, callback, errback):
        self.checkTwistedPresence()

        from twisted.web import client
        from twisted.internet import ssl, reactor

        contextFactory = ssl.ClientContextFactory()
        factory = client.HTTPClientFactory(url, method="POST",
                                           postdata=data, headers=headers)
        scheme, host, port, path = client._parse(url)
        reactor.connectSSL(host, port, factory, contextFactory)

        if errback is None:
            errback = self._ebReceivedResponse
        factory.deferred.addCallbacks(self._cbReceivedResponse, errback,
                                      (callback, factory))

    def parseResponse(self, response_data, response_headers):
        if response_headers.get('content-encoding','') == 'gzip':
            response_data = gzip.GzipFile(fileobj=StringIO(response_data)).read()
        #print response_data
        tramp = xmltramp.parse(response_data)
        if tramp[_tSoapNS.Body].has_key(_tSoapNS.Fault):
            faultString = str(tramp[_tSoapNS.Body][_tSoapNS.Fault].faultstring)
            faultCode   = str(tramp[_tSoapNS.Body][_tSoapNS.Fault].faultcode).split(':')[-1]
            raise SoapFaultError(faultCode, faultString)
        return tramp

    def post(self, apex_webservice_url=None, callback=None, errback=None):
        """ does all the grunt work:
        * serializes the request,
        * makes a http request,
        * passes the response to tramp
        * checks for soap fault
        * todo: check for mU='1' headers
        * returns the relevant result from the body child
        """
        headers = { "User-Agent": self.clientId,
                    "SOAPAction": "\"\"",
                    "Content-Type": "text/xml; charset=utf-8" }
        if self.context.gzip_response:
            headers['accept-encoding'] = 'gzip'
        if self.context.gzip_request:
            headers['content-encoding'] = 'gzip'
        payload = self.makeEnvelope()
        # if we're calling an apex code web service
        if apex_webservice_url is not None:
            url = "%s%s" %(self.context.endpoint_base, apex_webservice_url)
        else:
            url = self.context.endpoint

        if callback:
            self._makeAsyncRequest(url, payload, headers, callback, errback)
        else:
            if IS_APP_ENGINE:
                response = urlfetch.fetch(url, payload, urlfetch.POST, headers)
                response_header = response.headers
                response_body = response.content
            else:
                request = urllib2.Request(url=url, data=payload, 
                                          headers=headers)
                try:
                    response = urllib2.urlopen(request)
                except urllib2.HTTPError, e:
                    # an HTTPError can function as an urlopen response in the case of
                    # an error
                    response = e
                response_body = response.read()
                response_headers = response.info()
            return self.parseResponse(response_body, response_headers)


class LoginRequest(SoapEnvelope):
    def __init__(self, context, username, password, org_id=None):
        SoapEnvelope.__init__(self, context, "login")
        self.__username = username
        self.__password = password
        self.__org_id = org_id

    def writeHeaders(self, s):
        # if org_id has been passed in, write a LoginScopeHeader as we're
        # trying to authenticate a self-service user
        if self.__org_id is not None:
            s.startElement(_partnerNs, "LoginScopeHeader")
            s.writeStringElement(_partnerNs, "organizationId", self.__org_id)
            s.endElement()
        else:
            pass

    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "username", self.__username)
        s.writeStringElement(_partnerNs, "password", self.__password)


# base class for all methods that require a sessionId
class AuthenticatedRequest(SoapEnvelope):
    def __init__(self, context, sessionId, operationName):
        SoapEnvelope.__init__(self, context, operationName)
        self.sessionId = sessionId

    def writeHeaders(self, s):
        s.startElement(_partnerNs, "SessionHeader")
        s.writeStringElement(_partnerNs, "sessionId", self.sessionId)
        s.endElement()

    def writeSObjects(self, s, sObjects, elemName="sObjects"):
        if islst(sObjects):
            for o in sObjects:
                self.writeSObjects(s, o, elemName)
        else:
            s.startElement(_partnerNs, elemName)
            # type has to go first
            s.writeStringElement(_sobjectNs, "type", sObjects['type'])
            for fn in sObjects.keys():
                if (fn != 'type'):
                    s.writeStringElement(_sobjectNs, fn, sObjects[fn])
            s.endElement()


# for Meta data apply a different namespace     
class MetaCreateRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, metadata, operationName="create"):
        logging.info(serverUrl)
        AuthenticatedRequest.__init__(self, context, sessionId, operationName)
        self.__metadata = metadata 
        self.meta = True
        self.namespace = _metadataNs
        
    def writeBody(self, s):
        attr_vals = { (None, u'xsi:type'): 'ns2:'+ self.__metadata['xsitype'], (None, u'xmlns:ns2'): _metadataNs }       
        s.startElement(None, "metadata", AttributesNSImpl(attr_vals, { }) )
        s.characters("\n")
        
        for fn in self.__metadata:
            if ( fn == 'xsitype' ):
                pass
            elif ( fn == 'nameField' ):
                s.startElement(None,'nameField')
                nameField = self.__metadata[fn];
                logging.info(nameField)
                for nf in nameField:    
                    s.writeStringElement(None, nf, nameField[nf])    
                s.endElement() # name field
            elif (fn == 'tabVisibilities'):
                s.startElement(None,'tabVisibilities')
                tabVisibilities = self.__metadata[fn];
                logging.info(tabVisibilities)
                for nf in tabVisibilities:    
                    s.writeStringElement(None, nf, tabVisibilities[nf])
                s.endElement()               
            else :
                s.writeStringElement(None, fn, self.__metadata[fn])
 
        s.characters("\n")      
        s.endElement() # metadata 
 
 
class MetaUpdateRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, metadata, operationName="update"):
        logging.info(serverUrl)
        AuthenticatedRequest.__init__(self, context, sessionId, operationName)
        self.__metadata = metadata 
        self.meta = True
        self.namespace = _metadataNs
        self.currentName = metadata['fullName']
        
    def writeBody(self, s):
        attr_vals = { (None, u'xsi:type'): 'ns2:'+ self.__metadata['xsitype'], (None, u'xmlns:ns2'): _metadataNs }       
        s.startElement(None, 'UpdateMetadata' )
        s.writeStringElement(None, 'currentName', self.currentName)
        s.startElement(None, "metadata", AttributesNSImpl(attr_vals, { }) )
        s.characters("\n")        
        
        for fn in self.__metadata:
            if ( fn == 'xsitype' ):
                pass 
            elif ( fn == 'nameField' ):
                s.startElement(None,'nameField')
                nameField = self.__metadata[fn];
                logging.info(nameField)
                for nf in nameField:    
                    s.writeStringElement(None, nf, nameField[nf])    
                s.endElement() # name field                
            elif (fn == 'tabVisibilities'):
                s.startElement(None,'tabVisibilities')
                tabVisibilities = self.__metadata[fn];
                logging.info(tabVisibilities)
                for nf in tabVisibilities:    
                    s.writeStringElement(None, nf, tabVisibilities[nf])
                s.endElement()
            else :
                s.writeStringElement(None, fn, self.__metadata[fn]) 
        s.characters("\n")      
        s.endElement() # updateMetadata
        s.endElement() # metadata 
        
class MetaCheckStatus(AuthenticatedRequest):
    def __init__(self, context, sessionId, id):
        AuthenticatedRequest.__init__(self, context, sessionId, 'checkStatus' )
        self.__id = id
        self.meta = True
        self.namespace = _metadataNs
        
    def writeBody(self, s):    
        s.writeStringElement(None, 'id', self.__id) 

class QueryOptionsRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, operationName):
        AuthenticatedRequest.__init__(self, context, sessionId, operationName)
        self.batchSize = context.batch_size

    def writeHeaders(self, s):
        AuthenticatedRequest.writeHeaders(self, s)
        s.startElement(_partnerNs, "QueryOptions")
        s.writeStringElement(_partnerNs, "batchSize", self.batchSize)
        s.endElement()

class AssignmentRuleHeaderRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, operationName):
        AuthenticatedRequest.__init__(self, context, sessionId, operationName)
        self.use_default_assignment_rule = context.use_default_assignment_rule
        self.assignment_rule_id = context.assignment_rule_id

    def writeHeaders(self, s):
        AuthenticatedRequest.writeHeaders(self, s)
        s.startElement(_partnerNs, "AssignmentRuleHeader")
        if self.use_default_assignment_rule is True:
            s.writeStringElement(_partnerNs, "useDefaultRule", "true")
        elif self.assignment_rule_id is not None:
            s.writeStringElement(_partnerNs, "assignmentRuleID",
                                 self.assignment_rule_id)
        s.endElement()


class QueryRequest(QueryOptionsRequest):
    def __init__(self, context, sessionId, soql):
        QueryOptionsRequest.__init__(self, context, sessionId, "query")
        self.__query = soql

    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "queryString", self.__query)


class QueryAllRequest(QueryOptionsRequest):
    def __init__(self, context, sessionId, soql):
        QueryOptionsRequest.__init__(self, context, sessionId, "queryAll")
        self.__query = soql

    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "queryString", self.__query)


class QueryMoreRequest(QueryOptionsRequest):
    def __init__(self, context, sessionId, queryLocator):
        QueryOptionsRequest.__init__(self, context, sessionId, "queryMore")
        self.__queryLocator = queryLocator

    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "queryLocator", self.__queryLocator)


class SearchRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, sosl):
        AuthenticatedRequest.__init__(self, context, sessionId, "search")
        self.__search = sosl

    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "search", self.__search)


class GetUpdatedRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, sObjectType, start, end, operationName="getUpdated"):
        AuthenticatedRequest.__init__(self, context, sessionId, operationName)
        self.__sObjectType = sObjectType
        self.__start = start;
        self.__end = end;

    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "sObjectType", self.__sObjectType)
        s.writeStringElement(_partnerNs, "startDate", self.__start)
        s.writeStringElement(_partnerNs, "endDate", self.__end)


class GetDeletedRequest(GetUpdatedRequest):
    def __init__(self, context, sessionId, sObjectType, start, end):
        GetUpdatedRequest.__init__(self, context, sessionId, sObjectType, start, end, "getDeleted")


class UpsertRequest(AssignmentRuleHeaderRequest):
    def __init__(self, context, sessionId, externalIdName, sObjects):
        AssignmentRuleHeaderRequest.__init__(self, context, sessionId, "upsert")
        self.__externalIdName = externalIdName
        self.__sObjects = sObjects

    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "externalIDFieldName", self.__externalIdName)
        self.writeSObjects(s, self.__sObjects)


class UpdateRequest(AssignmentRuleHeaderRequest):
    def __init__(self, context, sessionId, sObjects, operationName="update"):
        AssignmentRuleHeaderRequest.__init__(self, context, sessionId, operationName)
        self.__sObjects = sObjects

    def writeBody(self, s):
        self.writeSObjects(s, self.__sObjects)


class CreateRequest(AssignmentRuleHeaderRequest):
    def __init__(self, context, sessionId, sObjects):
        AssignmentRuleHeaderRequest.__init__(self, context, sessionId, "create")
        self.__sObjects = sObjects

    def writeBody(self, s):
        self.writeSObjects(s, self.__sObjects)


class ExecuteAnonRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, codeblock):
        serverUrl = serverUrl.replace('/u/','/s/')
        AuthenticatedRequest.__init__(self, context, sessionId, "executeAnonymous")
        self.__block = codeblock;
        self.namespace = _wsdl_apexNs
        
    def writeBody(self, s):
        s.writeStringElement(_wsdl_apexNs, "String", self.__block)


class DeleteRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, ids):
        AuthenticatedRequest.__init__(self, context, sessionId, "delete")
        self.__ids = ids;

    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "id", self.__ids)

        
class EmptyRecycleBinRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, ids):
        AuthenticatedRequest.__init__(self, context, sessionId, 
                                      "emptyRecycleBin")
        self.__ids = ids
        
    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "ids", self.__ids)                


class UndeleteRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, ids):
        AuthenticatedRequest.__init__(self, context, sessionId, "undelete")
        self.__ids = ids;

    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "id", self.__ids)

        
class InvalidateSessionsRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, sessionIdList):
        AuthenticatedRequest.__init__(self, context, sessionId, 
                                      "invalidateSessions")
        self.__sessionIds = sessionIdList
        
    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "sessionIds", self.__sessionIds)
        

class RetrieveRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, fields, sObjectType, ids):
        AuthenticatedRequest.__init__(self, context, sessionId, "retrieve")
        self.__fields = fields
        self.__sObjectType = sObjectType
        self.__ids = ids

    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "fieldList", self.__fields)
        s.writeStringElement(_partnerNs, "sObjectType", self.__sObjectType);
        s.writeStringElement(_partnerNs, "ids", self.__ids)


class ResetPasswordRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, userId):
        AuthenticatedRequest.__init__(self, context, sessionId, "resetPassword")
        self.__userId = userId

    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "userId", self.__userId)


class SetPasswordRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, userId, password):
        AuthenticatedRequest.__init__(self, context, sessionId, "setPassword")
        self.__userId = userId
        self.__password = password

    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "userId", self.__userId)
        s.writeStringElement(_partnerNs, "password", self.__password)


class DescribeSObjectsRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, sObjectTypes):
        AuthenticatedRequest.__init__(self, context, sessionId, "describeSObjects")
        self.__sObjectTypes = sObjectTypes

    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "sObjectType", self.__sObjectTypes)

class DescribeLayoutRequest(AuthenticatedRequest):
    def __init__(self, context, sessionId, sObjectType):
        AuthenticatedRequest.__init__(self, context, sessionId, "describeLayout")
        self.__sObjectType = sObjectType

    def writeBody(self, s):
        s.writeStringElement(_partnerNs, "sObjectType", self.__sObjectType)


class ExecuteApexRequest(SoapEnvelope):
    """ Class for calling Apex methods that have been exposed as web services
    """
    def __init__(self, context, sessionId, method, args, is_array,
                 header_ns, sobject_ns):
        self.header_ns = header_ns
        self.sobject_ns = sobject_ns
        self.method = method
        SoapEnvelope.__init__(self, context, method)
        self.sessionId = sessionId
        self.args = args
        #self.url = url

    def makeEnvelope(self):
        s = SoapWriter(self.context, ("se", _envNs), ("sfns", self.header_ns))
        s.startElement(_envNs, "Header")
        s.characters("\n")
        s.startElement(_envNs, "CallOptions")
        s.writeStringElement(_envNs, "client", self.clientId)
        s.endElement()
        s.characters("\n")
        self.writeHeaders(s)
        s.endElement()    # Header
        s.startElement(_envNs, "Body")
        s.characters("\n")
        self.writeBody(s)
        s.endElement()  # body
        return s.endDocument()

    def writeHeaders(self, s):
        s.startElement(self.header_ns, "SessionHeader")
        s.writeStringElement(self.header_ns, "sessionId", self.sessionId)
        s.endElement()

    def writeBody(self, s):
        s.startElement(self.sobject_ns, self.operationName)
        for (arg_name, value) in self.args.items():
            s.writeStringElement(self.sobject_ns, arg_name, value)
        s.endElement()    # operation

