import math
import geolocation

NUM_SMALL_BOXES = 100

def geotagger(lat,lng):
    '''take lat,lng and returns a tuple that contains the following:
    int(lat),int(lng),int(x),int(y),int(num),{lat:lat,'lng':lng}
    '''
    sign = lambda num:'+' if (num >= 0) else ''
    geoTagPrefix_as_str = lambda lat,lng:'%s%03d,%s%03d'%(sign(lat),int(lat),sign(lng),int(lng))
    geoTagPrefix_as_tuple = lambda lat,lng:geoTagPrefix_as_str(lat,lng).split(',')

    def fractional(value):
        _frac = str(value).split('.')[-1]
        return float(_frac)/math.pow(10,len(_frac))
    normalized = lambda value:int(fractional(value) * NUM_SMALL_BOXES)

    x = normalized(lng)
    y = normalized(lat)

    result = None
    _t_ = geoTagPrefix_as_tuple(lat,lng)
    _result = {'heat_lat':_t_[0],'heat_lng':_t_[-1],'heat_x':x,'heat_y':y,'heat_num':NUM_SMALL_BOXES,'heat_gps':{'lat':lat,'lng':lng}}
    return _result

if (__name__ == '__main__') :
    lat1 = 37.5
    lat2 = 38.5
    lon1 = -122.5
    lon2 = -123.5
    geo = geolocation.GeolocationDistance()
    dist = geo.distance(lat1,lon1,lat2,lon2,geo.KM)
    print 'dist=%4.2f' % (dist)
    print '='*30
    print
    
    assert '%4.2f' % (dist) == '141.73', 'Oops, something has gone wrong #1.'

    print 'BEGIN: (default)'
    tag1 = geotagger(lat1,lon1)
    print tag1
    print
    print '-'*10
    print
    tag2 = geotagger(lat2,lon2)
    print tag2
    print 'END!  %s' % ('='*30)
    print

    assert tag1['heat_x'] == 50, 'Oops, something has gone wrong #2.1.1'
    assert tag1['heat_y'] == 50, 'Oops, something has gone wrong #2.1.2'
    assert tag1['heat_lat'] == '+037', 'Oops, something has gone wrong #2.1.3'
    assert tag1['heat_lng'] == '-122', 'Oops, something has gone wrong #2.1.4'
    assert tag1['heat_gps']['lat'] == 37.5, 'Oops, something has gone wrong #2.1.5'
    assert tag1['heat_gps']['lng'] == -122.5, 'Oops, something has gone wrong #2.1.6'
    assert tag1['heat_num'] == NUM_SMALL_BOXES, 'Oops, something has gone wrong #2.1.7'

    assert tag2['heat_x'] == 50, 'Oops, something has gone wrong #2.2.1'
    assert tag2['heat_y'] == 50, 'Oops, something has gone wrong #2.2.2'
    assert tag2['heat_lat'] == '+038', 'Oops, something has gone wrong #2.2.3'
    assert tag2['heat_lng'] == '-123', 'Oops, something has gone wrong #2.2.4'
    assert tag2['heat_gps']['lat'] == 38.5, 'Oops, something has gone wrong #2.2.5'
    assert tag2['heat_gps']['lng'] == -123.5, 'Oops, something has gone wrong #2.2.6'
    assert tag2['heat_num'] == NUM_SMALL_BOXES, 'Oops, something has gone wrong #2.2.7'

    print 'Done !'
