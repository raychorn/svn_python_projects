import math
import geolocation

NUM_SMALL_BOXES = 30

_AS_STR = 'str'
_AS_TUPLE = 'tuple'
_AS_DICT = 'dict'

is_str = lambda value:value == _AS_STR
is_tuple = lambda value:value == _AS_TUPLE
is_dict = lambda value:value == _AS_DICT

_keys_ = ['heat_lat','heat_lng','heat_x','heat_y','heat_num']

_is_debugging = False

def geotagger(lat,lng,_as_=_AS_STR):
    '''take lat,lng and returns a tuple that contains the following:
    int(lat),int(lng),int(x),int(y),int(num)
    when _as_ is _AS_STR then a string is returned in the form of a csv.
    when _as_ is _AS_TUPLE then a tuple is returned
    when _as_ is _AS_DICT then a dict is returned
    '''
    sign = lambda num:'+' if (num >= 0) else ''
    geoTagPrefix_as_str = lambda lat,lng:'%s%03d,%s%03d'%(sign(lat),int(lat),sign(lng),int(lng))
    geoTagPrefix_as_tuple = lambda lat,lng:geoTagPrefix_as_str(lat,lng).split(',')
    geo = geolocation.GeolocationDistance()

    _lat = float(int(lat))
    _lng = float(int(lng))

    _lat2 = _lat+geo.hemispherical_offset_for_lat_or_lng(lat,1,False)
    _lng2 = _lng+geo.hemispherical_offset_for_lat_or_lng(lng,1,False)

    topDist = geo.distance(lat,lng,lat,_lng2,geo.FEET)
    leftDist = geo.distance(lat,lng,_lat2,lng,geo.FEET)
    
    if (_is_debugging):
        print 'topDist=%4.2f (feet), %4.2f (miles)' % (topDist,geo.convert_feet_to_miles(topDist))
        print 'leftDist=%4.2f (feet), %4.2f (miles)' % (leftDist,geo.convert_feet_to_miles(leftDist))

    refTopDist = geo.distance(_lat,_lng,_lat,_lng2,geo.FEET)
    refLeftDist = geo.distance(_lat,_lng,_lat2,_lng,geo.FEET)

    if (_is_debugging):
        print 'refTopDist=%4.2f (feet), %4.2f (miles)' % (refTopDist,geo.convert_feet_to_miles(refTopDist))
        print 'refLeftDist=%4.2f (feet), %4.2f (miles)' % (refLeftDist,geo.convert_feet_to_miles(refLeftDist))
    
    x = int(math.floor((refTopDist-topDist) / (refTopDist/NUM_SMALL_BOXES)))
    y = int(math.floor((refLeftDist-leftDist) / (refLeftDist/NUM_SMALL_BOXES)))
    
    result = None
    _result = geoTagPrefix_as_tuple(lat,lng)+[x,y,NUM_SMALL_BOXES]
    if (is_str(_as_)):
        result = ','.join([str(item) for item in _result])
    elif (is_tuple(_as_)):
        result = _result
    elif (is_dict(_as_)):
        d = {}
        for i in xrange(0,min(len(_result),len(_keys_))+1):
            try:
                d[_keys_[i]] = _result[i]
            except:
                pass
        result = d
    return result
