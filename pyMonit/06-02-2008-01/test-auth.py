from authentication import SalesForceAuthentication

if (__name__ == '__main__'):
   sfAuth = SalesForceAuthentication.SalesForceAuthentication('rhorn@magma-da.com','sisko@7660$boo')
   print 'Good to go !' if (sfAuth.isLoginSuccessful) else 'Sorry Charlie !'

   sfAuth = SalesForceAuthentication.SalesForceAuthentication('rhorn@magma-da.com','Peekaboo')
   print 'Good to go !' if (sfAuth.isLoginSuccessful) else 'Sorry Charlie !'
   pass
