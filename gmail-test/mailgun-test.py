import smtplib
import sys, traceback

from vyperlogix import misc

sender = "Vyper Logix Corp Support Dept <do-not-respond@vyperlogix.com>"
to = "Ray C Horn <raychorn@vyperlogix.com>"
subject = "Test smtplib"

headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (sender, to, subject)
msg = headers + "Hello. How are you? #3"

mailserver = smtplib.SMTP("smtp.mailgun.org", 587)
mailserver.set_debuglevel(0) 
try:
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    _gmail_login = "postmaster@vyperlogix.com"
    _from_address = 'do-not-respond@vyperlogix.com'
    mailserver.login(_gmail_login, "5gqe8q71c2g9")
    mailserver.sendmail(_from_address, "raychorn@hotmail.com", msg)
except:
    exc_info = sys.exc_info()
    info_string = '\n'.join(traceback.format_exception(*exc_info))
    print >>sys.stderr, '(%s) :: Cannot send email... \n%s' % (misc.funcName(),info_string)
finally:
    mailserver.close()
    print 'Done !'