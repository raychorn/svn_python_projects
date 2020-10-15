def decodeUnicode(value):
    try:
        value = value.encode('utf-8')
    except UnicodeError:
        value = unicode(value, "utf-8")
    return value
