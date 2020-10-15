import sys
def decode(s, enc=None, denc=sys.getdefaultencoding()):
    """try interpreting s using several possible encodings.
    return value is a three-element tuple.  The first element is either an
    ASCII string or a Unicode object.  The second element is 1
    if the decoder had to punt and delete some characters from the input
    to successfully generate a Unicode object."""
    if isinstance(s, unicode):
        return s, 0, "utf-8"
    try:
        x = unicode(s, "ascii")
        # if it's ascii, we're done
        return s, 0, "ascii"
    except UnicodeError:
        encodings = ["utf-8","iso-8859-1","cp1252","iso-8859-15"]
        # if the default encoding is not ascii it's a good thing to try
        if denc != "ascii": encodings.insert(0, denc)
        # always try any caller-provided encoding first
        if enc: encodings.insert(0, enc)
        for enc in encodings:

            # Most of the characters between 0x80 and 0x9F are displayable
            # in cp1252 but are control characters in iso-8859-1.  Skip
            # iso-8859-1 if they are found, even though the unicode() call
            # might well succeed.

            if (enc in ("iso-8859-15", "iso-8859-1") and
                re.search(r"[\x80-\x9f]", s) is not None):
                continue

            # Characters in the given range are more likely to be 
            # symbols used in iso-8859-15, so even though unicode()
            # may accept such strings with those encodings, skip them.

            if (enc in ("iso-8859-1", "cp1252") and
                re.search(r"[\xa4\xa6\xa8\xb4\xb8\xbc-\xbe]", s) is not None):
                continue

            try:
                x = unicode(s, enc)
            except UnicodeError:
                pass
            else:
                if x.encode(enc) == s:
                    return x, 0, enc

        # nothing worked perfectly - try again, but use the "ignore" parameter
        # and return the longest result
        output = [(unicode(s, enc, "ignore"), enc) for enc in encodings]
        output = [(len(x), x) for x in output]
        output.sort()
        x, enc = output[-1][1]
        return x, 1, enc

