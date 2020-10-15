'Usage:	 cscript sendemail.vbs <email_recipient@example.com> "<subject_line>" "<email_body>" "<optional:email_attachment_path>"
'Ex. No attach:	cscript sendemail.vbs example@gmail.com "test subject line" "test email body"
'Ex. W/ attach:	cscript sendemail.vbs example@gmail.com "test subject line" "test email body" "c:\scripts\log.txt"

'***********
'****CONFIGURE THE FROM EMAIL ADDRESS AND PASSWORD

Const fromEmail	= "raychorn@gmail.com"
Const password	= "sisko@7660$boo"

'****END OF CONFIGURATION
'***********

Dim emailObj, emailConfig
Set emailObj = CreateObject("CDO.Message")
emailObj.From = fromEmail
emailObj.To = WScript.Arguments.Item(0)
emailObj.Subject = WScript.Arguments.Item(1)
emailObj.TextBody = WScript.Arguments.Item(2)

If WScript.Arguments.Count > 3 Then
emailObj.AddAttachment WScript.Arguments.Item(3)
End If

Set emailConfig = emailObj.Configuration
emailConfig.Fields("http://schemas.microsoft.com/cdo/configuration/smtpserver") = "smtp.gmail.com"
emailConfig.Fields("http://schemas.microsoft.com/cdo/configuration/smtpserverport") = 465
emailConfig.Fields("http://schemas.microsoft.com/cdo/configuration/sendusing") = 2
emailConfig.Fields("http://schemas.microsoft.com/cdo/configuration/smtpauthenticate") = 1
emailConfig.Fields("http://schemas.microsoft.com/cdo/configuration/smtpusessl") = true
emailConfig.Fields("http://schemas.microsoft.com/cdo/configuration/sendusername") = fromEmail
emailConfig.Fields("http://schemas.microsoft.com/cdo/configuration/sendpassword") = password
emailConfig.Fields.Update

emailObj.Send

Set emailobj	= nothing
Set emailConfig	= nothing

