from vyperlogix.products import keys

_username = 'Rhorn6'
_password = keys._decode('7065656B61623030')

ACCEPTED_ID = lambda __version__:keys._encode('%s%s%s' % (__version__,_username,_password))
