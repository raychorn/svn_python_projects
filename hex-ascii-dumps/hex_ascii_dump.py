from vyperlogix.misc import hex_ascii

if (__name__ == '__main__'):
    filename = __file__
    file = open(filename, 'rb')
    data = file.read()
    file.close()
    
    io = hex_ascii.dumps(data, size=20)
    print io.getvalue()
