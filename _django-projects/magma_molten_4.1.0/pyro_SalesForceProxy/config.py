from vyperlogix.products import keys
from maglib.salesforce.cred import credentials

e_passphrase = keys._decode('4D61676D612044657369676E204175746F6D6174696F6E204D6F6C74656E')
__sf_account__ = credentials(e_passphrase)

ACCEPTED_ID = lambda __version__:keys._encode('%s%s%s' % (__version__,__sf_account__['username'],__sf_account__['password']))
