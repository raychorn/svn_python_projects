import os, sys
import smtplib
server = smtplib.SMTP('smtpout.secureserver.net')
try:
    print 'server.login...'
    server.login('webmaster@pypi.info', 'peekab00')
    print 'done.'
except smtplib.SMTPAuthenticationError, details:
    print 'ERROR 101 due to %s.' % (details)

msg = (
"To: raychorn@vyperlogix.com\r\n"
"From: webmaster@pypi.info\r\n"
"Subject: Test e-mail\r\n"
"Content-type: text/plain\r\n"
"\r\n"
"Hello,\r\n"
"sys.argv=%s\r\n" % (sys.argv))

try:
    print 'server.sendmail...'
    server.sendmail('webmaster@pypi.info', 'raychorn@vyperlogix.com', msg)
    server.quit()
    print 'done.'
except smtplib.SMTPAuthenticationError, details:
    print 'ERROR 201 due to %s.' % (details)

