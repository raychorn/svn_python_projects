import codecs
import encodings

def decodeUnicode(value):
    if (isinstance(value,unicode)):
        return ((codecs.getencoder('unicode_escape'))(value))[0]
    elif (isinstance(value,str)):
        return value
    else:
        return decodeUnicode(str(value))
