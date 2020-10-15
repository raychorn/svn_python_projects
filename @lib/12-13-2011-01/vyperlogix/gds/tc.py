'''
Class to calculate temperatures and voltages of thermocouples.  The
basic equation is T = f(V) where T is temperature and V is voltage. The
approximating polynomials come from the Omega Temperature Catalog vol 26,
1988, page T-12.

The Tc class constructor takes a string that identifies the thermocouple.
Supported types are E, J, K, R, S, T.  Type K is the default type.  The
class methods are:

    mV_to_degF
    mV_to_degC
    degF_to_mV
    degC_to_mV

An exception will be raised if the input voltage or temperature is outside
of the allowed range.

The method used is to calculate T give V by the polynomial approximation.
The inverse function (to calculate V given T) is gotten by using Newton's
method to invert the polynomial.

If you call this module as a main module, it will run tests that validate
the output of the Tc class.

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

import sys, string
__version__ = "$Id: tc.py,v 1.3 2002/08/21 12:41:49 donp Exp $"

	
class Tc:
    # The following dictionary contains the coefficients of the polynomials 
    # that convert EMF to temperature in degrees C.

    # xx Check that the type K array is correct.  In the C version, it had
    # xx only 9 terms, not 10.  I made the last element (the x^9 term) 0.
    # xx Also check for type R.

    coefficients = {
        "E" : [0.104967248, 17189.45282, -282639.0850, 12695339.5, -448703084.6, 1.10866e10, -1.76807e11, 1.71842e12, -9.19278e12, 2.06132e13],
        "J" : [-0.048868252, 19873.14503, -218614.5353, 11569199.78, -264917531.4, 2018441314.0, 0.0, 0.0, 0.0, 0.0],
        "K" : [0.226584602, 24152.10900, 67233.4248, 2210340.682, -860963914.9, 4.83506e10, -1.18452e12, 1.38690e13, -6.33708e13, 0.0],
        "R" : [0.263632917, 179075.491, -48840341.37, 1.90002e10, -4.82704e12, 7.62091e14, -7.20026e16, 3.71496e18, -8.03104e19, 0.0],
        "S" : [0.927763167, 169526.5150, -31568363.94, 8990730663.0, -1.63565e12, 1.88027e14, -1.37241e16, 6.17501e17, -1.56105e19, 1.69535e20],
        "T" : [0.100860910, 25727.94369, -767345.8295, 78025595.81, -9247486589.0, 6.97688e11, -2.66192e13, 3.94078e14, 0.0, 0.0]
        }

    mV_limits = { 
        "E" : [-5.237, 76.358], 
        "J" : [0.0,    42.922],
        "K" : [0.0,    54.807],
        "R" : [0.0,    10.503], 
        "S" : [0.0,    18.504], 
        "T" : [-4.865, 20.869]
        }
    tc_error = -999.0
    
    def __init__(self, tcType = "K", ignore_error = 0):
        self.coef = self.coefficients[tcType]
        self.limits = self.mV_limits[tcType]
        self.ignore_error = 0

    def mV_to_degC(self, mV):
        if mV < self.limits[0] or mV > self.limits[1]:
            if self.ignore_error:
                raise `mV` + " out of limits"
            else:
                return self.tc_error
        return self.__v2c(mV/1000.)

    def mV_to_degF(self, mV):
        return self.__c2f(self.mV_to_degC(mV))

    def degF_to_mV(self, mV):
        pass

    def degC_to_mV(self, T):
        # Use Newton's method to find the root.
        raise "Not written"
        count = 0
        while 1:
            mV_new = mV_old - self.mV_to_degC(mV_old)/self.__deriv(mV_old)
            count = count + 1
            if (count > 100):
                raise "Too many iterations"
            if abs(mV_new - mV_old) < .001:
                pass
                

    def __v2c(self, v):
        # Evaluate the polynomial.  Input is voltage in volts, output is 
        # temperature in degrees C.
        a = self.coef
        return a[0]+v*(a[1]+v*(a[2]+v*(a[3]+v*(a[4]+v*(a[5]+v*(a[6]+v*(a[7]                +v*(a[8]+v*a[9]))))))))

    def __c2f(self, t):
        return 9.*t/5 + 32

##############################################################################
# Test the Tc class

if __name__ == "__main__":

    error_cases = [
        [-5.238e-3, "E"],
        [76.359e-3, "E"],
        [-1e-3,     "J"],
        [42.923e-3, "J"],
        [-1e-3,     "K"],
        [54.808e-3, "K"],
        [-1e-3,     "R"],
        [10.504e-3, "R"],
        [-1e-3,     "S"],
        [18.505e-3, "S"],
        [-4.866e-3, "T"],
        [20.870e-3, "T"],
    ]

    # Polynomial error should be less than the following values in deg C
    tolerance = {
        "E" : 0.5,
        "J" : 0.1,
        "K" : 0.7,
        "R" : 0.5,
        "S" : 1.0,
        "T" : 0.5,
    }
    test_cases = {
        "E" : [
            [0.0, 0.0],
            [6.317, 100.0],
            [13.419, 200.0],
            [21.033, 300.0],
            [28.943, 400.0],
            [36.999, 500.0],
            [45.085, 600.0],
            [53.110, 700.0],
            [61.022, 800.0],
            [68.783, 900.0],
            [76.357, 1000.0],
        ],
        "J" : [
            [0.0, 0.0],
            [5.268, 100.0],
            [10.777, 200.0],
            [16.325, 300.0],
            [21.846, 400.0],
            [27.388, 500.0],
            [33.096, 600.0],
            [39.130, 700.0],
            [42.922, 760.0],
        ],
        "K" : [
            [0.0, 0.0],
            [4.095, 100.0],
            [ 8.137, 200.0],
            [12.207, 300.0],
            [16.395, 400.0],
            [20.640, 500.0],
            [24.902, 600.0],
            [29.128, 700.0],
            [33.277, 800.0],
            [37.325, 900.0],
            [41.269, 1000.0],
            [45.108, 1100.0],
            [48.828, 1200.0],
            [52.398, 1300.0],
        ],
        "R" : [
            [0.0, 0.0],
            [0.647, 100.0],
            [ 1.468, 200.0],
            [ 2.400, 300.0],
            [ 3.407, 400.0],
            [ 4.471, 500.0],
            [ 5.582, 600.0],
            [ 6.741, 700.0],
            [ 7.949, 800.0],
            [ 9.203, 900.0],
            [10.503, 1000.0],
        ],
        "S" : [
            [0.0, 0.0],
            [0.645, 100.0],
            [ 1.440, 200.0],
            [ 2.323, 300.0],
            [ 3.260, 400.0],
            [ 4.234, 500.0],
            [ 5.237, 600.0],
            [ 6.274, 700.0],
            [ 7.345, 800.0],
            [ 8.448, 900.0],
            [ 9.585, 1000.0],
            [10.754, 1100.0],
            [11.947, 1200.0],
            [13.155, 1300.0],
            [14.368, 1400.0],
            [15.576, 1500.0],
            [16.771, 1600.0],
            [17.942, 1700.0],
            [18.503, 1750.0],
        ],
        "T" : [
            [-4.864, -160.0],
            [-3.378, -100.0],
            [0.0, 0.0],
            [4.277, 100.0],
            [ 9.286, 200.0],
            [14.860, 300.0],
            [20.869, 400.0],
        ]
    }
    
    # Test EMF to temperature conversion
    for tc_type in test_cases.keys():
        tc = Tc(tcType = tc_type)
        cases = test_cases[tc_type]
        for case in cases:
            mV = case[0]
            degC_correct = case[1]
            degC = tc.mV_to_degC(mV)
            eps = degC - degC_correct
            if abs(eps) > tolerance[tc_type]:
                raise "Bad test case for type " + tc_type
        del tc

    # Test the cases that should raise exceptions
    for case in error_cases:
        mV = case[0]
        tc_type = case[1]
        tc = Tc(tcType = tc_type)
        try:
            degC = tc.mV_to_degC(mV)
            raise "Didn't get exception"
        except:
            pass

    #print "Tests finished"

    ambient = [70, 75, 80, 85, 90, 95]
    tc = Tc() # Defaults to type K
    print " " * 10, "Ambient Temperature in deg F\n"
    print " mV\t",
    for amb in ambient:
        print "%5d\t" % amb,
    print
    for mv in xrange(100):
        mV = mv/10.
        degF = tc.mV_to_degF(mV)
        print "%.1f" % mV,
        for amb in ambient:
            print "\t%.0f" % (degF+amb),
        print

