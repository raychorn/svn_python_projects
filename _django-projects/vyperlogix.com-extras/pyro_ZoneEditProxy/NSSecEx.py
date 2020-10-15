#!/usr/bin/env python

#  Name Server security plugins.

__version__ = '''4.1.0'''

from config import ACCEPTED_ID

from vyperlogix.google.gae import gae_utils
_is_running_local = gae_utils.is_running_local()

ident = ACCEPTED_ID(__version__)

#----- required global funcs that return validator objects ------
def BCGuard():
	return None		# no special broadcast server guard

def NSGuard():
	v=NSnewConnValidator()
	v.setAllowedIdentifications([ident])
	return v

#----- validator object implementation --------

import Pyro.protocol

# NS Pyro Daemon newConnValidator
class NSnewConnValidator(Pyro.protocol.DefaultConnValidator):
	def acceptIdentification(self, tcpserver, conn, hash, challenge):
		print conn.addr[0],'SENDS IDENTIFICATION...'
		(ok,reason)=Pyro.protocol.DefaultConnValidator.acceptIdentification(self, tcpserver, conn, hash, challenge)
		if not ok:
			info_string = "Make sure the identification is %s" % (ident)
			if (not _is_running_local):
				info_string = ''
			print 'Connection denied!%s' % ()
		return (ok,reason)

