# Copyright (C) 2005, 2006, 2007 Canonical Ltd
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__copyright__ = "Copyright 2007-2008, Kevin Shuk, Canonical Ltd."

# same format as sys.version_info: "A tuple containing the five components of
# the version number: major, minor, micro, releaselevel, and serial. All
# values except releaselevel are integers; the release level is 'alpha',
# 'beta', 'candidate', or 'final'. The version_info value corresponding to the
# Python version 2.0 is (2, 0, 0, 'final', 0)."  Additionally we use a
# releaselevel of 'dev' for unreleased under-development code.
import time
serial = int(time.strftime("%Y%m%d%H%M%S", time.gmtime()))

version_info = (0, 9, 7, 2, 'final', serial)

__version = lambda v,isDigits:[str(t) for t in v if (str(t).isdigit() == isDigits)]

if (__version(version_info[0:-1],False)[0] == 'final'):
    version_string = '.'.join(__version(version_info[0:-1],True))
else:
    version_string = '%s' % ('.'.join(['%d' % (t) for t in version_info]))
__version__ = version_string



def test_suite():
    import tests
    return tests.test_suite()
