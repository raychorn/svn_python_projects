from urllib2 import urlopen
from urllib import urlencode
try:
	# Python >= 2.5
	from hashlib import md5
except ImportError:
	# Python < 2.5
	import md5
	
from vyperlogix.hash.lists import HashedFuzzyLists2

def admob_ad(request, admob_params=HashedFuzzyLists2()):
	"""
	Given a Django ``request`` object and dict of
	admob parameters returns a Admob ad.

	If no ad can be retrieved displays a one pixel
	Admob tracker image.

	Usage:

	def my_view(request):

		admob_dict = {}
		admob_dict["admob_site_id"] = "required_admob_site_id"
		admob_dict["admob_postal_coode"] = "optional_postal_code"
		admob_dict["admob_area_code"] = "optional_area_code"
		admob_dict["admob_coordinates"] = "optional_coordinates"
		admob_dict["admob_gender"] = "optional_gender"
		admob_dict["admob_keywords"] = "optional_keywords"
		admob_dict["admob_search"] = "optional_search"		
		admob_dict["admob_mode"] = "test" # leave this out for the live site...

		ad = admob_ad(request, admob_dict)

		return HttpResponse(ad)

	"""
	from vyperlogix.misc import ObjectTypeName
	_type = ObjectTypeName.typeClassName(admob_params)
	if (_type.find('vyperlogix.hash.lists.HashedFuzzyLists2') == -1):
		admob_params = HashedFuzzyLists2(fromDict=admob_params)
	# Change to "live" when ready to deploy.
	admob_mode = "test" if (admob_params["admob_mode"] == 'test') else None

	admob_endpoint = "http://r.admob.com/ad_source.php"
	admob_version = "20080714-PYTHON"
	admob_timeout = 1.0
	admob_ignore = ("HTTP_PRAGMA", "HTTP_CACHE_CONTROL", "HTTP_CONNECTION", "HTTP_USER_AGENT", "HTTP_COOKIE",)

	# Build URL.
	admob_post = {} 

	# Required Parameters - will raise if not found.
	admob_post["s"] = admob_params["admob_site_id"]

	# Meta Parameters.
	admob_post["u"] = request.META.get("HTTP_USER_AGENT", None)
	admob_post["i"] = request.META.get("REMOTE_ADDR", None)
	admob_post["p"] = request.build_absolute_uri()
	admob_post["t"] = md5(request.session.session_key).hexdigest()

	# Hardcoded Parameters.
	admob_post["e"] = "UTF-8"
	admob_post["v"] = admob_version

	# Optional Parameters.
	admob_post["ma"] = admob_params["admob_markup"]
	admob_post["d[pc]"] = admob_params["admob_postal_code"]
	admob_post["d[ac]"] = admob_params["admob_area_code"]
	admob_post["d[coord]"] = admob_params["admob_coordinates"]
	admob_post["d[dob]"] = admob_params["admob_dob"]
	admob_post["d[gender]"] = admob_params["admob_gender"]
	admob_post["k"] = admob_params["admob_keywords"]
	admob_post["p"] = admob_params["admob_siteID"]
	admob_post["search"] = admob_params["admob_search"]

	for k, v in request.META.items():
		if k not in admob_ignore:
			admob_post["h[%s]" % k] = v

	# Strip all ``None`` and empty values from admob_post.
	for k, v in admob_post.items():
		if v is None or v == "":
			admob_post.pop(k)

	if admob_mode == "test":
		admob_post["m"] = "test"

	# Request the Ad.
	admob_success = True
	try:
		admob_data = urlencode(admob_post)
		admob_file = urlopen(admob_endpoint, admob_data)
		admob_contents = admob_file.read()
		if admob_contents is None or admob_contents == "":
			admob_success = False
	except Exception, e:
		admob_success = False

	if not admob_success:
		if (admob_params["alternate_content"]):
			admob_contents = admob_params["alternate_content"]
		else:
			admob_contents = "<img src=\"http://t.admob.com/li.php/c.gif/%(admob_site_id)s/1/%(admob_timeout)F/%(absolute_uri)s\" alt=\"\" width=\"1\" height=\"1\" />"  \
				           % {"admob_site_id" : admob_params["admob_site_id"], 
				              "admob_timeout" : admob_timeout, 
				              "absolute_uri" : md5(request.build_absolute_uri()).hexdigest()}

	# DEBUG:
	# print 'Connecting to: %s' % admob_endpoint
	# print 'Sending Parameters:'
	# print admob_post
	# print 'Got reponse:'
	# print admob_contents

	return admob_contents