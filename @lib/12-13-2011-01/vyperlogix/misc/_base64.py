import base64

def toBase64(fname):
    fin = open(fname,"rb")
    try:
        data = fin.read()
    finally:
        fin.close()
    return base64.b64encode(data)

def fromBase64(data,fname):
    _data = base64.b64decode(data)
    fout = open(fname,"wb")
    try:
        fout.write(_data)
    finally:
        fout.close()
