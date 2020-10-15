import sys
import types

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

    from vyperlogix import misc
from vyperlogix.misc import ObjectTypeName
from vyperlogix.classes.CooperativeClass import Cooperative

class Message(Cooperative):
    """
    Represents an email message for sending.

    Creates full text implementation on initialization as well as storing
    all fields as member variables.

    fromAdd - single address of message sender
    toAdds - single address or list of addresses of primary recipients
    body - Text of message body as string
    subject - optional subject string
    ccAdds - optional single address or list of addresses of copy recipients
    bccAdds - optional single address or list of addresses of
              blindcopy recipients
    """
    def __init__(self, fromAdd, toAdds, body, subject="", ccAdds=None, bccAdds=None, passThru=False):
        '''passThru set to True tells the system to refrain from formatting the message.'''
        self.fromAdd = fromAdd

        self.toAddList = self.stringOrIterable(toAdds)
        self.ccAddList = self.stringOrIterable(ccAdds)
        self.bccAddList = self.stringOrIterable(bccAdds)

        self.subject = subject
        self.body = body

        self.message = body
        if (not passThru):
            self.buildMsg()
        return
    
    def __str__(self):
        return "%s" %self.message

    def __repr__(self):
        return "Message('%s', %s, '''%s''', %s, %s, %s)" %(self.fromAdd,
                                                           self.toAddList,
                                                           self.body,
                                                           self.subject,
                                                           self.ccAddList,
                                                           self.bccAddList)

    def stringOrIterable(self, value):
        """
        if value is not a list or tuple, packs value as one item list
        before returning it
        """
        if value is None:
            return value
        elif type(value) == types.TupleType or type(value) == types.ListType:
            return value
        else:
            return [value]
                                                           
    def buildMsg(self, noSubject=False):
        """
        Builds and stores message text based on the member components.
        Call this if any of the data (recipients, subject, body) has changed
        after the object has been instantiated.
        """
        msgBuf = StringIO()
        
        # build the header
        msgBuf.write('From: %s\r\n' % self.fromAdd)

        msgBuf.write('To: %s\r\n' %','.join(self.toAddList))

        if self.ccAddList is not None:
            msgBuf.write('CC: %s\r\n' %','.join(self.ccAddList))
        
        if self.bccAddList is not None:
            msgBuf.write('BCC: %s\r\n' %','.join(self.bccAddList))

        if (len(self.subject) > 0):
            msgBuf.write('Subject: %s\r\n' %self.subject.encode('ascii','replace'))

        msgBuf.write('\r\n') # Separator break btwn hdr and msg

        # Add the body
            
        msgBuf.write(self.body) # .encode('ascii','replace')

        self.message =  msgBuf.getvalue()

        return self.message

class HTMLMessage(Message):
    """
    Represents an email message as HTML for sending.

    Creates full text implementation on initialization as well as storing
    all fields as member variables.

    fromAdd - single address of message sender
    toAdds - single address or list of addresses of primary recipients
    body - Text of message body as string
    subject - optional subject string
    ccAdds - optional single address or list of addresses of copy recipients
    bccAdds - optional single address or list of addresses of
              blindcopy recipients
    """
    def __init__(self, fromAdd, toAdds, body, subject="", ccAdds=None, bccAdds=None):
	from vyperlogix.mail import html
	content = self.renderHTML(subject,body)
	body = body if (isinstance(body,list)) else body.split('\r\n') if (body.find('\r\n') > -1) else body.split('\r') if (body.find('\r') > -1) else body.split('\n') if (body.find('\n') > -1) else [body]
	self.__text_body__ = '<br/>'.join(body)
	self.__html_body__ = html.asHTMLEmail(self.__text_body__,content,subject)
        super(HTMLMessage, self).__init__(fromAdd, toAdds, self.__html_body__, subject=subject, ccAdds=ccAdds, bccAdds=bccAdds, passThru=True)

    def html_body():
        doc = "html_body"
        def fget(self):
            return self.__html_body__
        return locals()
    html_body = property(**html_body())
    
    def text_body():
        doc = "text_body"
        def fget(self):
            return self.__text_body__
        return locals()
    text_body = property(**text_body())
    
    def renderHTML(self,subj,body):
	from vyperlogix.html import myOOHTML as oohtml
	h_html = oohtml.Html()
	
	if (misc.isString(subj)) and (misc.isList(body)):
	    h_html.text(oohtml.oohtml.DOCTYPE_40_TRANSITIONAL)
	    
	    html_html = h_html.tag(oohtml.oohtml.HTML)
	    head_html = html_html.tag(oohtml.oohtml.HEAD)
	    head_html.tagOp(oohtml.oohtml.META, http_equiv=oohtml.oohtml.CONTENT_TYPE, content=oohtml.oohtml.TEXT_HTML_CHARSET_ISO_8859_1)
	    head_html.metas(
		    (oohtml.oohtml.AUTHOR, "Ray C Horn (rhorn@magma-da.com)"),
		    (oohtml.oohtml.KEYWORDS, "SMTP Email Message"),
		    (oohtml.oohtml.DESCRIPTION, "The contents of this email are considered to be confidential unless otherwise specified."),
		    (oohtml.oohtml.ROBOTS, oohtml.oohtml.ALL))
	    head_html.tagTITLE('SMTP Email Message')
	    body_html = html_html.tag(oohtml.oohtml.BODY)
	    idContent = body_html.tag(oohtml.oohtml.DIV, id="content", style="background-color: white")
    
	    idContent.html_simple_table(body)
	    pass
	else:
	    print >>sys.stderr, '%s :: "subj" parm must be of type str and "body" parm must be of type list rather than of types "%s" and "%s", respectively.' % (ObjectTypeName.objectSignature(self),type(subj),type(body))
	return h_html.toHtml()
        
