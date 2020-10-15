import numpy
import math
from scipy import *

class GeolocationDistance2():
    def __init__(self):
        self.eq_rad = 6378.137 #eq radius in km
        self.polar_rad = 6356.752 #polar radius in km
        
    def radians(self,degrees):
	return degrees*2*numpy.pi/360
    
    def earth_radius(self,lat):
        '''
        Given a latitude in radias returns earth radius in km
        '''
    
        top = (self.eq_rad**2 * numpy.cos(lat))**2 + (self.polar_rad**2 * numpy.sin(lat))**2
        bottom = (self.eq_rad * numpy.cos(lat))**2 + (self.polar_rad * numpy.sin(lat))**2
    
        return numpy.sqrt(top/bottom)
    
    def haver_sin(self, x):
        return numpy.sin(x/2) ** 2
    
    def arc_haver_sin(self, x):
        return 2*numpy.arcsin(numpy.sqrt(x))

    def distance_in_km(self, lat1, lon1, lat2, lon2):
        '''
        Given a set of geo coordinates (in degrees) it will return the distance in km
        '''
    
        #convert to radians
        lon1 = self.radians(lon1) #lon1*2*numpy.pi/360
        lat1 = self.radians(lat1) #lat1*2*numpy.pi/360
        lon2 = self.radians(lon2) #lon2*2*numpy.pi/360
        lat2 = self.radians(lat2) #lat2*2*numpy.pi/360
    
        R = self.earth_radius((lat1+lat2)/2) #km
    
        #haversine formula - angles in radians
        deltaLon = numpy.abs(lon1-lon2)
        deltaLat = numpy.abs(lat1-lat2)
    
        dOverR = self.haver_sin(deltaLat) + numpy.cos(lat1)*numpy.cos(lat2)*self.haver_sin(deltaLon)
    
        return R * self.arc_haver_sin(dOverR)
    
