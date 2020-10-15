'''
Defines the Wire class, which is used to model various characteristics
of wire.

Copyright (C) 2002 GDS Software

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the Free
Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
MA  02111-1307  USA

See http://www.gnu.org/licenses/licenses.html for more details.
'''

from math import pow, pi
from util import SignificantFigures, SignMantissaExponent
__version__ = "$Id: wire.py,v 1.5 2002/08/22 02:25:57 donp Exp $"

#################### Classes ############################################

class Wire:
    '''Utility class to deal with wire properties.  Internal calculations
    are done in SI units:  m for length, ohms for resistance, kg for mass, 
    K for temperature.  Utility functions are provided for unit conversions.
    '''
    # The properties dictionary gives the following list of properties:
    #   Specific gravity
    #   Resistivity in 1e-6 ohm*cm
    #   Temperature coefficient of resistivity (1/K)
    # These numbers from CRC Handbook of Chemistry & Physics, 59th ed.
    properties = { 
        "aluminum"    : [  2.70,   2.824 , .0039  ],
        "copper"      : [  8.89,   1.7241, .00393 ],
        "brass"       : [  8.6 ,   7     , .002   ],
        "gold"        : [ 19.3 ,   2.44  , .0034  ],
        "iron"        : [  7.8 ,  10     , .005   ],
        "lead"        : [ 11.4 ,  22     , .0039  ],
        "magnesium"   : [  1.74,   4.6   , .004   ],
        "monel"       : [  8.9 ,  42     , .0020  ],
        "nichrome"    : [  8.2 , 100     , .0004  ],
        "nickel"      : [  8.9 ,   7.8   , .0033  ],
        "platinum"    : [ 21.4 ,  10     , .003   ],
        "silver"      : [ 10.5 ,   1.59  , .0038  ],
        "steel"       : [  7.7 ,  11     , .004   ],
        "tin"         : [  7.3 ,  11.5   , .0042  ],
        "zinc"        : [  7.1 ,   5.8   , .0037  ],
    }

    def __init__(self, diam_in_m = 0.0, length_in_m = 0.0):
        self.material    = "copper"
        self.SetMaterial(self.material)
        self.diam_in_m   = diam_in_m
        self.temp_in_K   = 20 + 273
        self.length_in_m = length_in_m

    def SetMaterial(self, material):
        if not self.properties.has_key(material):
            raise "'%s' is an unknown material" % material
        prop = self.properties[material]
        self.specific_gravity = prop[0]
        self.resistivity      = prop[1]/1e8  # Convert to ohm*m
        self.temp_coeff       = prop[2]

    def GetProperties(self):
        '''Returns a tuple containing the following elements:
            Resistance in ohms
            Length in m
            Mass in kg
            Diameter in m
            Resistivity in ohm*m at current temperature
            Specific gravity
            Temperature in K
            Material
        '''
        area = pi * self.diam_in_m * self.diam_in_m / 4
        resistance = self.resistivity * self.length_in_m/area
        temp_corr  = 1 + self.temp_coeff * self.temp_in_K
        resistance = resistance * temp_corr
        mass = 1000 * self.specific_gravity * area * self.length_in_m
        return (             resistance,             self.length_in_m,             area,             mass,             self.diam_in_m,             self.resistivity * temp_corr,             self.specific_gravity,             self.temp_in_K,             self.material         )

    def GetPropertyNames(self):
        return (             "Resistance",             "Length in m",             "Area in m^2",             "Mass in kg",             "Diameter in m",             "Resistivity",             "Specific gravity",             "Temperature in K",             "Material"         )

    def SetLength(self, length_in_m):
        self.length_in_m = length_in_m
        if length_in_m < 0.0:
            raise "Length in m must be >= 0.0"

    def SetDiameter(self, diam_in_m):
        self.diam_in_m = diam_in_m
        if diam_in_m <= 0.0:
            raise "Diameter in m must be > 0.0"

    def SetTemperatureInK(self, temp_in_K):
        self.temp_in_K = temp_in_K
        if temp_in_K <= 0.0 or temp_in_K > (150 + 273):
            raise "'%s' is improper temperature" % `temp_in_K`

#################### Utility functions ##################################
    
def AWG_to_meters(n):
    '''Returns the wire diameter in meters given the AWG gauge 
    number.
    '''
    if n < 0 or n > 40:
        raise "AWG argument out of range"
    return .0254*(.46/pow(92, (n+3.)/39))

def WireTable(temp_deg_C, wire_material):
    '''Print a wire table in terms of AWG diameters for the indicated
    wire type.
    '''
    ft_to_m = 0.3048
    m_to_mils = 39370
    kg_to_lbs = 2.2046
 
    print "Wire Table for %s at %d degrees C" % (wire_material, int(temp_deg_C))
    print ""
    print "AWG  Diam, mils    ft/lb    ohm/1000 ft"
    print "---  ----------   --------  -----------"
    w = Wire()
    w.SetMaterial("copper")
    w.SetTemperatureInK(temp_deg_C + 273)
    for gauge in xrange(0, 41, 2):
        w.SetLength(1 * ft_to_m)
        w.SetDiameter(AWG_to_meters(gauge))
        p = w.GetProperties()
        resistance  = p[0]
        mass        = p[3]
        print " %2d  %8.1f" % (gauge, w.diam_in_m * m_to_mils),
        ft_per_lb       = 1/(mass * kg_to_lbs)
        milliohm_per_ft = resistance * 1000.
        print " %10.2f  %11.4f" % (ft_per_lb, milliohm_per_ft)

if __name__ == "__main__":
    WireTable(20, "copper")

import sys
sys.stderr.write("Warning:  wire.py does not seem to work correctly.\n" + "18 gauge wire has wrong resistance -- should be 6.5 milliohms/ft at 77 deg F.\n" + "R & H give rho for Cu at 20 deg C as 1.56e-8 ohm*m, so I've got bad\n" + "resistivity data.\n\n")

ft_to_m = 0.3048
m_to_mils = 39370
kg_to_lbs = 2.2046
w = Wire()
w.SetMaterial("copper")
w.SetTemperatureInK(20 + 273)
gauge = 18
w.SetLength(1 * ft_to_m)
w.SetDiameter(AWG_to_meters(gauge))
p = w.GetProperties()
n = w.GetPropertyNames()

for ix in xrange(len(n)):
    print n[ix], p[ix]

resistance  = p[0]
mass        = p[3]
print " %2d  %8.1f" % (gauge, w.diam_in_m * m_to_mils),
ft_per_lb       = 1/(mass * kg_to_lbs)
milliohm_per_ft = resistance * 1000.
print " %10.2f  %11.4f" % (ft_per_lb, milliohm_per_ft)
