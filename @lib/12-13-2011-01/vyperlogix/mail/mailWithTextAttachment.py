import smtplib, sys, MimeWriter, StringIO, base64
import os
def mailWithTextAttachment(serverURL=None, sender='', to='', subject='', text=''):
    """
    Usage:
    mail('somemailserver.com', 'me@example.com', 'someone@example.com', 'test', 'This is a test')
    """
    message = StringIO.StringIO()
    writer = MimeWriter.MimeWriter(message)
    writer.addheader('Subject', subject)
    writer.startmultipartbody('mixed')

    # start off with a text/plain part
    part = writer.nextpart()
    body = part.startbody('text/plain')
    body.write(text)

    # now add an attachment
    part = writer.nextpart()
    part.addheader('Content-Transfer-Encoding', 'base64')
    body = part.startbody('text/plain')
    base64.encode(open('myfile.txt', 'rb'), body)

    # finish off
    writer.lastpart()

    # send the mail
    smtp = smtplib.SMTP(serverURL)
    smtp.sendmail(sender, to, message.getvalue())
    smtp.quit()
