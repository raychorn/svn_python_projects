def isListenerActive(ip,port=None):
   import socket
   
   if (isinstance(ip,list)):
      ip = tuple(ip)
   
   if (isinstance(ip,tuple)):
      ip,port = ip[0:2]
   
   isOkay = False
   try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((ip, port))
      s.close()
      del s
      isOkay = True
   except:
      pass
   return isOkay

