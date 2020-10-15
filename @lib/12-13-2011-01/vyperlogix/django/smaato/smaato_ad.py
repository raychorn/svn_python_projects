from urllib2 import urlopen
	
def smaato_ad(request,alternate_content=''):
	"""
	Given a Django ``request`` object a Smaato ad.
	"""
	smaato_endpoint = "http://www.near-by.info/smaato-ads.php"

	# Request the Ad.
	smaato_success = True
	try:
		smaato_file = urlopen(smaato_endpoint)
		smaato_contents = smaato_file.read()
		if smaato_contents is None or smaato_contents == "":
			smaato_success = False
	except Exception, e:
		smaato_success = False

	if not smaato_success:
		smaato_contents = alternate_content

	return smaato_contents