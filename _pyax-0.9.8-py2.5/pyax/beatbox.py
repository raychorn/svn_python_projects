"""beatbox: Makes the salesforce.com SOAP API easily accessible."""
__version__ = "0.95pyax"
__author__ = "Simon Fell"
__credits__ = "Mad shouts to the sforce possie"
__copyright__ = "(C) 2006 Simon Fell. GNU GPL 2."

import httplib
import urllib2
import sys
from urlparse import urlparse
from StringIO import StringIO
import gzip
import datetime
import xmltramp
from xmltramp import islst
from xml.sax.saxutils import XMLGenerator
from xml.sax.saxutils import quoteattr
from xml.sax.xmlreader import AttributesNSImpl

from pyax.context import Context


class NoTwistedInstalledError(Exception):
    """Raised when trying use asynchronous calls without Twisted."""


# global constants for namespace strings, used during serialization
_partnerNs = "urn:partner.soap.sforce.com"
_sobjectNs = "urn:sobject.partner.soap.sforce.com"
_envNs = "http://schemas.xmlsoap.org/soap/envelope/"
_noAttrs = AttributesNSImpl({}, {})

# global constants for xmltramp namespaces, used to access response data
_tPartnerNS = xmltramp.Namespace(_partnerNs)
_tSObjectNS = xmltramp.Namespace(_sobjectNs)
_tSoapNS = xmltramp.Namespace(_envNs)


# the main sforce client proxy class
class Client:
    def __init__(self, context=None):
        if context is None:
            context = Context()
        self.context = context

    # login, the serverUrl and sessionId are automatically handled, returns the loginResult structure
    def login(self, username, password, org_id=None):
        del self.context.endpoint # force the endpoint back to the login_endpoint
        lr = LoginRequest(self.context, username, password, org_id).post()
        self.useSession(str(lr[_tPartnerNS.sessionId]),
                        str(lr[_tPartnerNS.serverUrl]))
        return lr

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
                                    "describeTabs").post(always_return_list=True)

    def getServerTimestamp(self):
        return str(AuthenticatedRequest(self.context, self.sessionId,
                                        "getServerTimestamp").post()[_tPartnerNS.timestamp])

    def resetPassword(self, userId):
        return ResetPasswordRequest(self.context, self.sessionId, userId).post()

    def setPassword(self, userId, password):
        SetPasswordRequest(self.context, self.sessionId, userId,
                           password).post()

    def getUserInfo(self):
        return AuthenticatedRequest(self.context, self.sessionId,
                                    "getUserInfo").post()

    def _invoke(self, method, args, is_array, namespaces, url,
                    header_ns, sobject_ns):
        ar = ApexRequest(self.context, self.sessionId, method, args, is_array,
                         header_ns, sobject_ns)
        #print ar.makeEnvelope()
        return ar.post(apex_webservice_url=url)

    #def convertLead(self, convertLeads):

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
    def __init__(self, context, operationName, clientId="BeatBox/" + __version__):
        self.context = context
        self.operationName = operationName
        self.clientId = clientId

    def writeHeaders(self, writer):
        pass

    def writeBody(self, writer):
        pass

    def makeEnvelope(self):
        s = SoapWriter(self.context,
                          ("s", _envNs), ("p", _partnerNs), ("o", _sobjectNs))
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
        s.startElement(_partnerNs, self.operationName)
        self.writeBody(s)
        s.endElement()    # operation
        s.endElement()  # body        # hmm, need real _invoke method somewhere. Prolly in beatbox
        # probably won't be called invoke, either.
        return s.endDocument()

    def _cbReceivedResponse(self, response, callback, factory, always_return_list):
        headers = factory.response_headers
        # Convert Twisted headers to urllib convention
        for key, value in headers.items():
            if isinstance(value, list):
                headers[key] = ",".join(value)

        response = self.parseResponse(response, headers, always_return_list)
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

    def _makeAsyncRequest(self, url, data, headers, callback, errback,
                          always_return_list):
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
                                      (callback, factory, always_return_list))

    def parseResponse(self, response_data, response_headers, always_return_list):
        if response_headers.get('content-encoding','') == 'gzip':
            response_data = gzip.GzipFile(fileobj=StringIO(response_data)).read()

        tramp = xmltramp.parse(response_data)
        try:
            faultString = str(tramp[_tSoapNS.Body][_tSoapNS.Fault].faultstring)
            faultCode   = str(tramp[_tSoapNS.Body][_tSoapNS.Fault].faultcode).split(':')[-1]
            raise SoapFaultError(faultCode, faultString)
        except KeyError:
            pass
        # first child of body is XXXXResponse
        result = tramp[_tSoapNS.Body][0]
        # it contains either a single child, or for a batch call multiple children
        if always_return_list or len(result) > 1:
            return result[:]
        elif len(result) == 0:
            return None
        else:
            return result[0]

    # does all the grunt work,
    #   serializes the request,
    #   makes a http request,
    #   passes the response to tramp
    #   checks for soap fault
    #   todo: check for mU='1' headers
    #   returns the relevant result from the body child
    def post(self, apex_webservice_url=None, always_return_list=False,
             callback=None, errback=None):
        headers = { "User-Agent": self.clientId,
                    "SOAPAction": "\"\"",
                    "Content-Type": "text/xml; charset=utf-8" }
        if self.context.gzip_response:
            headers['accept-encoding'] = 'gzip'
        if self.context.gzip_request:
            headers['content-encoding'] = 'gzip'

        # if we're calling an apex code web service
        if apex_webservice_url is not None:
            url = "%s%s" %(self.context.endpoint_base, apex_webservice_url)
        else:
            url = self.context.endpoint

        data = self.makeEnvelope()

        if callback:
            self._makeAsyncRequest(url, data, headers, callback, errback,
                                   always_return_list)
        else:
            request = urllib2.Request(url=url, data=data, headers=headers)
            try:
                response = urllib2.urlopen(request)
            except urllib2.HTTPError, e:
                # an HTTPError can function as an urlopen response in the case of
                # an error
                response = e

            return self.parseResponse(response.read(), response.info(),
                                      always_return_list)


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

class ApexRequest(SoapEnvelope):
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

