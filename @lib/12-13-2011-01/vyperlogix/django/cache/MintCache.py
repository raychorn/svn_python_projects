# http://www.djangosnippets.org/snippets/155/
try:
    import memcache
except ImportError:
    _MintCache = None
else:
    class _MintCache(_Cache):
        "Memcached cache backend the sequel."
        def __init__(self, server, params):
            _Cache.__init__(self, params)
            self._cache = memcache.Client(server.split(';'))
        def get(self, key, default=None):
            key = self.scrub_key( key )
            val = self._cache.get(key)
            if val is None:
                val = default
            else:
                try:
                    stale_after,val = pickle.loads(val)
                    now = time.time()
                    if now > stale_after:
                        cache_log( "stale, refreshing" )
                        self.set( key, val, 60 ) # the old val will now last for 60 additional secs
                        val = default
                except:
                    pass
            return val
        def set(self, key, value, timeout=0):
            key = self.scrub_key( key )
            if timeout is 0:
                timeout = self.default_timeout
            now = time.time()
            val = pickle.dumps( ( now + timeout, value ),  2)
            self._cache.set(key, val, 7*86400)
        def delete(self, key):
            key = self.scrub_key( key )
            self._cache.delete(key)