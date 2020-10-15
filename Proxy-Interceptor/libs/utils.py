__regex_valid_ip__ = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
__regex_valid_ip_and_port__ = r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):([0-9]{1,5})"

is_valid_ip = lambda value:re.compile(__regex_valid_ip__, re.MULTILINE).match(value) is not None
is_valid_ip_and_port = lambda value:re.compile(__regex_valid_ip_and_port__, re.MULTILINE).match(value) is not None

def is_ip_address_valid(ip):
    '''127.0.0.1 is the general form of an IP address'''
    if (is_valid_ip(ip) or is_valid_ip_and_port(ip)):
	if (is_valid_ip_and_port(ip)):
	    toks1 = ip.split(':')
	    toks2 = toks1[0].split('.')
	    return (len(toks2) == 4) and all([str(n).isdigit() for n in list(tuple(toks2+[toks1[-1]]))])
	elif (is_valid_ip(ip)):
	    toks = ip.split('.')
	    return (len(toks) == 4) and all([str(n).isdigit() for n in toks])
    return False

def make_number_valid_or_none(value,allow_float=True):
    value = str(value) if (value is not None) else value
    if (value and value.replace('.','').isdigit()):
	toks = value.split('.')
	if (len(toks) >= 2):
	    toks[1] = ''.join(toks[1:])
	    if (len(toks) > 2):
		del toks[2:]
	return float('.'.join(toks)) if (allow_float) else int(''.join(toks))
    return None

