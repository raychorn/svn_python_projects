#!/usr/bin/env twistd -ny
#
import os
import codecs
import cyclone.web
from twisted.application import service, internet
from twisted.python import log

class MainHandler(cyclone.web.RequestHandler):
  def get(self):
    self.render("index.html")

class UploadHandler(cyclone.web.RequestHandler):
  def post(self):
    fnames = []
    datafiles = self.request.files['datafile']
    for f in datafiles:
      log.msg('filename=%s' % (f['filename']))
      fname = '%s/%d_%s' % (self.settings.incoming_path, 1,f['filename'])
      log.msg(fname)
      try:
        fp = codecs.open(fname, 'wb')
        fp.write(f['body'])
        fp.close()
        fnames.append(fname)
      except Exception, e:
        log.err('error writing file: ', e) 
    
    self.write(repr(fnames))

settings = dict(
    cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    incoming_path=os.path.join(os.path.dirname(__file__), "incoming"),
  )

webapp = cyclone.web.Application([
  (r"/", MainHandler),
  (r"/upload", UploadHandler),
], **settings)

application = service.Application("cyclone")
cycloneService = internet.TCPServer(8888, webapp)
cycloneService.setServiceParent(application)
