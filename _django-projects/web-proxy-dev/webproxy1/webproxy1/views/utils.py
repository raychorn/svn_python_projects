from django.conf import settings

from vyperlogix.classes.SmartObject import SmartObject

import os

def sendEmail(self, datas):
    params = SmartObject(args=datas)
    link="http://%s/activate/%s" % (settings.DOMAIN_NAME, params.activation_key)
    c = Context({ 'activation_link' : link, 'username' : params.username})
    f = open(MEDIA_ROOT+datas['email_path'], 'r')
    t = Template(f.read())
    f.close()
    message=t.render(c)
    send_mail(datas['email_subject'], message, 'yourdomain <no-reply@yourdomain.com>', [datas['email']], fail_silently=False)

'''
ses-smtp-user.20161222-075636
SMTP Username:
AKIAIOCDG3LNVRSFD4RA
SMTP Password:
AsQPmlEsKunBADVs3sMjipB/14MoTaLVmyRaGKipPZKi
'''
SMTP_Username = 'AKIAJTZ7T26SIUMUYLFQ'
SMTP_Password = 'Ai7h0BGqpmRy2HaZmu+R/Wt2PBXibOhiJF6i/e97FXFD'

def semd_aws_email(email_from, email_to, email_subject, email_content, email_host='email-smtp.us-east-1.amazonaws.com', email_user = SMTP_Username, email_password = SMTP_Password, email_port=587, email_content_type='html'):
    import smtplib
    
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    # AWS Config
    EMAIL_HOST = email_host
    EMAIL_HOST_USER = email_user
    EMAIL_HOST_PASSWORD = email_password
    EMAIL_PORT = email_port
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = email_subject
    msg['From'] = email_from
    msg['To'] = email_to
    
    if (os.path.exists(email_content)):
        html = open(email_content).read()
    else:
        html = email_content
    
    mime_text = MIMEText(html, email_content_type)
    msg.attach(mime_text)
    
    s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    s.starttls()
    s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    s.sendmail(me, you, msg.as_string())
    s.quit()