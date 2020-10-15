from vyperlogix.misc import _utils

import logging

import math

has_numpy = False
try:
    import numpy
    math_pi = numpy.math.pi
    math_sin = numpy.sin
    math_sqrt = numpy.sqrt
    math_cos = numpy.cos
    math_asin = numpy.arcsin
    has_numpy = True
except ImportError, e:
    math_pi = math.pi
    math_sin = math.sin
    math_sqrt = math.sqrt
    math_cos = math.cos
    math_asin = math.asin
    #info_string = _utils.formattedException(details=e)
    #logging.error('Cannot import numpy because "%s" falling back on standard math lib.' % (info_string))

class GeolocationDistance():
    '''
    Requires numpy if present - now safe for GAE...
    '''
    def __init__(self):
        self.EARTH_RAD = 6378137.0
	self.feet_in_mile = 5280.0
        self.radmiles = self.EARTH_RAD*100.0/2.54/12.0/self.feet_in_mile
        self.feet_per_meter = 3280.8398950131 / 1000
	self.FEET = 'feet'
	self.RADIANS = 'radians'
	self.MILES = 'miles'
	self.MI = 'mi'
	self.METERS = 'meters'
	self.M = 'm'
	self.KM = 'km'
	self.DEGREES = 'degrees'
	self.MIN = 'min'
        self.multipliers = {
            self.RADIANS : 1, 
            self.MILES : self.radmiles, 
            self.MI : self.radmiles, 
            self.FEET : self.radmiles * self.feet_in_mile,
            self.METERS : self.EARTH_RAD, 
            self.M : self.EARTH_RAD, 
            self.KM : self.EARTH_RAD / 1000, 
            self.DEGREES : 360 / (2 * math_pi), 
            self.MIN : 60 * 360 / (2 * math_pi)
        }
        
    def convert_feet_to_feet(self,feet):
        return feet

    def convert_miles_to_feet(self,miles):
        return miles * self.feet_in_mile
    
    def convert_feet_to_miles(self,feet):
        return feet / self.feet_in_mile
    
    def convert_km_to_feet(self,km):
        return km * self.feet_per_meter * 1000
    
    def convert_m_to_feet(self,m):
        return m * self.feet_per_meter
    
    def radians(self,degrees):
	return degrees*2*math_pi/360
    
    def hemispherical_offset_for_lat_or_lng(self,value,units,direction=False):
	return (-units if (value > 0) else units) if (direction) else (units if (value > 0) else -units)

    def distance(self, lat1, lon1, lat2, lon2, units):
	'''
	this formula works best for points close together or antipodal
	rounding error strikes when distance is one-quarter Earth's circumference
	(ref: wikipedia Great-circle distance)
	'''
	latRadians1 = self.radians(lat1)
	latRadians2 = self.radians(lat2)
	sdlat = math_sin((latRadians1 - latRadians2) / 2.0);
	sdlon = math_sin((self.radians(lon1) - self.radians(lon2)) / 2.0);
	result = math_sqrt(sdlat * sdlat + math_cos(latRadians1) * math_cos(latRadians2) * sdlon * sdlon);
	result = 2 * math_asin(result);
	try:
	    if (self.multipliers.has_key(units)):
		result = result * self.multipliers[units];
	except Exception, e:
	    print str(e)
	return result;
    