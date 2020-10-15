from pyax.connection import Connection
from pyax.context import Context
from pyax.apex import Apex

class ReConnection(Connection):
    __context = None
    
    @classmethod
    def connect(cls, sessionId, serverUrl):
        """ Authenticate a Salesforce.com user
        
        @param sessionId: sessionId from the previous session
        @param serverUrl: serverUrl from the previous session
            
        @return: authenticated connection object
        @rtype: pyax.connection.Connection
        """
        context = Context()
        
        cxn = cls(context)
        cxn.svc.sessionId = sessionId
        cxn.svc.serverUrl = serverUrl
        cxn.svc.context.endpoint = '/'.join(serverUrl.split('/')[0:-1])
        cxn.describe_global_response = cxn.describeGlobal()
        cxn.global_types = cxn.describe_global_response.get('types', [])
        
        cxn.apex = Apex(cxn)
        
        # informative attrs - changing these does nothing
        cxn.session_id = sessionId
        cxn.server_url = serverUrl
        return cxn
        
