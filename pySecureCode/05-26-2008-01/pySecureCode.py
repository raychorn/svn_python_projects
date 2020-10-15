import os
import lib.zip.SecurePyZipFile
import zipfile
import traceback

# To-Do:
#   1). Passphrase encryption - 
#       a). Automated process that creates an object that returns a random passphrase from a series of methods.
#       b). Master Passphrase is used to encrypt all passphrases.
#       c). Each passphrase for each file is the name of each file reveresed padded with nulls.

zipName = os.path.join('Z:\\python projects\\pySecureCode','test.zip')

if (os.path.exists(zipName)):
    os.remove(zipName)

print 'zipName=[%s]' % zipName
c = lib.zip.SecurePyZipFile.SecurePyZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)
c.isSourceless = False
print 'c=[%s]' % c
try:
    c.writepy('Z:\\@myMagma\\python-local-new-trunk\\pyax')
except Exception, details:
    print 'ERROR due to "%s".' % details
    traceback.print_exc()
c.close()
pass
