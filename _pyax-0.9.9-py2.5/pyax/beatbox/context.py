from urlparse import urlparse

class Context(object):
    """ Defines the context for a salesforce session (endpoint, http|https,
    gzip compression of outgoing and/or incoming requests
    """
    def __init__(self):
        """ Defines the default context settings """
        ## context defaults 
        # endpoint parts
        self.__login_servers = {'production': 'www.salesforce.com',
                                'sandbox': 'test.salesforce.com'}
        self.__default_instance = 'production'
        
        self.__endpoint_path = 'services/Soap/u'
        
        self.__api_version = '15.0'
        
        # are we going to gzip our request to the server?
        self.__default_gzip_request = True
        
        # are we going to ask the server to gzip its response?
        self.__default_gzip_response = True
        
        # force connections to http for debugging
        self.__default_force_http = False
        
        # assignment rule header settings
        self.__use_default_assignment_rule = False
        self.__assignment_rule_id = None
        
        ## tunables - generally not for the end user, but for the deveoper
        # how many times should an apex call be retried?
        self.__max_retry = 2
        
        # number of objects to allow in various types of batches before slicing

        self.__min_batch = 200
        self.__max_batch = 2000
        self.__default_batch_size = 500
        self.__batch_size = self.__default_batch_size

        # max objects in a create call
        self.__max_create = 200
        
        # max IDs in a single retrieve
        self.__max_retrieve = 2000
        
        # max objects in a single update call
        self.__max_update = 200
        
        # max IDs in a single delete call
        self.__max_delete = 200
  
    # force_http property - determines endpoint URL scheme
    def _get_force_http(self):
        try:
            return self.__force_http
        except AttributeError:
            return self.__default_force_http
    
    def _set_force_http(self, force_bool):
        if isinstance(force_bool, bool):
            self.__force_http = force_bool
        else:
            self.__force_http = self.__default_force_http

    force_http = property(_get_force_http, _set_force_http, 
                        doc="Force fall back to HTTP for debugging")
        
    
    # instance property
    def _get_instance(self):
        try:
            return self.__instance
        except AttributeError:
            return self.__default_instance

    
    def _set_instance(self, instance):
        if instance in self.__login_servers.keys():
            self.__instance = instance
        else:
            # opt or the default login server
            self.__instance = self.__default_instance
            return
    instance = property(_get_instance, _set_instance, 
                        doc="Salesforce instance to use")
    
    
    # login_endpoint property
    def _get_login_endpoint(self):
        try:
            url = self.__login_endpoint
        except AttributeError:
            scheme = 'https'
            if self.force_http is True:
                scheme = 'http'
            
            url = "%s://%s/%s/%s" \
            %(scheme,
              self.__login_servers.get(self.instance,
                                       self.__login_servers.get(self.__default_instance)), 
              self.__endpoint_path, 
              self.__api_version)
            
        return url
    
    def _set_login_endpoint(self, login_endpoint):
        self.__login_endpoint = login_endpoint
        
    def _del_login_endpoint(self):
        del self.__login_endpoint
        
    login_endpoint = property(_get_login_endpoint, 
                              _set_login_endpoint, 
                              _del_login_endpoint, 
                            "SOAP endpoint for Salesforce.com API login")


    # the primary endpoint property
    def _get_endpoint(self):
        try:
            return self.__endpoint
        except AttributeError:
            return self.login_endpoint
    
    def _set_endpoint(self, endpoint):
        self.__endpoint = endpoint
        return
        
    def _del_endpoint(self):
        # make this "safe", as in always callable
        try:
            del self.__endpoint
        except AttributeError:
            pass #swallow - this is OK
        return
            
    endpoint = property(_get_endpoint, 
                        _set_endpoint, 
                        _del_endpoint, 
                        "SOAP endpoint for authenticated API calls")   

    # just the scheme and netloc of the endpoint
    def _get_endpoint_base(self):
        o = urlparse(self.endpoint)
        base = "%s://%s" %(o.scheme, o.netloc)
        return base
    endpoint_base = property(_get_endpoint_base)

    # gzip_request property - determines whether we send out gzipped messages
    def _get_gzip_request(self):
        if self.force_http is True:
            return False
        else:
            try: 
                return self.__gzip_request
            except AttributeError:
                return self.__default_gzip_request
    
    def _set_gzip_request(self, gzip_bool):
        if isinstance(gzip_bool, bool):
            self.__gzip_request = gzip_bool
        else:
            self.__gzip_request = self.__default_gzip_request
            
    def _del_gzip_request(self):
        del self.__gzip_request

    gzip_request = property(_get_gzip_request, _set_gzip_request, 
                            _del_gzip_request,
                            doc="Determines whether we gzip outbound requests")


   # gzip_response property - determines we ask for gzipped responses
    def _get_gzip_response(self):
        if self.force_http is True:
            return False
        else:
            try: 
                return self.__gzip_response
            except AttributeError:
                return self.__default_gzip_response
    
    def _set_gzip_response(self, gzip_bool):
        if isinstance(gzip_bool, bool):
            self.__gzip_response = gzip_bool
        else:
            self.__gzip_response = self.__default_gzip_response
            
    def _del_gzip_response(self):
        del self.__gzip_response

    gzip_response = property(_get_gzip_response, _set_gzip_response, 
                             _del_gzip_response,
                             doc="Determines whether we ask for gzipped responses")


    ## Assignment Rule Header options
    def _get_assignment_rule_id(self):
        return self.__assignment_rule_id
    
    def _set_assignemnt_rule_id(self, assignment_rule_id):
        self.__assignment_rule_id = assignment_rule_id
        self.__use_default_assignment_rule = False
        return
    
    def _del_assignment_rule_id(self):
        self.assignment_rule_id = None
    
    assignment_rule_id = property(_get_assignment_rule_id, 
                                  _set_assignemnt_rule_id,
                                  _del_assignment_rule_id)
    
    def _get_use_default_assignment_rule(self):
        return self.__use_default_assignment_rule
    
    def _set_use_default_assignemnt_rule(self, use_default_rule):
        if not isinstance(use_default_rule, bool):
                use_default_rule = False
        self.__use_default_assignment_rule = use_default_rule
        return
    
    def _del_use_defualt_assignment_rule(self):
        self.__use_default_assignment_rule = False   
        return
    
    use_default_assignment_rule = property(_get_use_default_assignment_rule,
                                           _set_use_default_assignemnt_rule,
                                           _del_use_defualt_assignment_rule)
    def _get_max_retry(self):
        return self.__max_retry
    max_retry = property(_get_max_retry, 
                         doc="How many times an apex call should be retried")
    
    
    def _get_batch_size(self):
        return self.__batch_size
    
    def _set_batch_size(self, batch_size):
        if not isinstance(batch_size, int):
            batch_size = self.__default_batch_size
        elif batch_size < self.min_batch:
            batch_size = self.min_batch
        elif batch_size > self.max_batch:
            batch_size = self.max_batch
        self.__batch_size = batch_size
        return
    
    def _del_batch_size(self):
        self.__batch_size = self.__default_batch_size
        return    
    batch_size = property(_get_batch_size, _set_batch_size, _del_batch_size,
                         doc="Default Apex batch size")

    def _get_min_batch_size(self):
        return self.__min_batch
    min_batch = property(_get_min_batch_size, 
                         doc="Minimum Apex batch size")
    
    def _get_max_batch_size(self):
        return self.__max_batch
    max_batch = property(_get_max_batch_size, 
                         doc="Maximum Apex batch size")    
    
    def _get_max_create(self):
        return self.__max_create
    max_create = property(_get_max_create, 
                         doc="Max batch size for a create before slicing")
    
    
    def _get_max_retrieve(self):
        return self.__max_retrieve
    max_retrieve = property(_get_max_retrieve, 
                         doc="Max batch size for a retrieve before slicing")
 
 
    def _get_max_update(self):
        return self.__max_update
    max_update = property(_get_max_update, 
                         doc="Max batch size for an update before slicing")
    
    
    def _get_max_delete(self):
        return self.__max_delete
    max_delete = property(_get_max_delete, 
                         doc="Max batch size for a delete before slicing")


