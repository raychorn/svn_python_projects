""" Dealing with dates, times and timezones  programmatically is a beast!
Let's draw a line in the sand with what we can rely upon:
sforce always returns dates and datetimes as ISO format in UTC
userinfo provides the user's timezone.

What I'm not sure of, but is easily provable:
sforce expects times in inserts/updates as UTC?
sforce expects times in queries as UTC?
I think that if the ISO format specifies an offset, Salesforce will
convert accordingly

What is best avoided:
relying upon the local machine's idea of localtime.

"""
import os
import time
from datetime import date, datetime, timedelta, tzinfo

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'

ZERO = timedelta(0)
class UTCtz(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO
UTC = UTCtz()
    
class ApexDate(date):
    """ Specialized subclass of datetime to support the date or datetime
    format used by Salesforce.com.
    
    @note:  the magic here is that when coerced to string, this object is
            formatted ready to use by the Apex API.
    """

    @classmethod
    def fromSfIso(cls, sfdc_date_str):
        """ construct an ApexDatetime instance from a datetime string in UTC 
        
        @param sfdc_date_str: ISO formatted UTC time from Apex API call
        
        @return: passed datetime as an ApexDate
        @rtype: ApexDate
        """
        global DATE_FORMAT
        
        #timestamp = sfDatetimeString.split('.', 1)[0]
        datestruct = time.strptime(sfdc_date_str, DATE_FORMAT)

        return ApexDate(datestruct[0], # year
                        datestruct[1], # month
                        datestruct[2], # day
                        )
    
    def __add__(self, td):
        newdate = date.__add__(self, td)
        return ApexDate(newdate.year, newdate.month, newdate.day)
    
    def __sub__(self, td):
        newdate = date.__sub__(self, td)
        if isinstance(newdate, date):
            return ApexDate(newdate.year, newdate.month, newdate.day)
        return newdate # actually a timedelta
    
    def __str__(self):
        return self.isoformat()

class ApexDatetime(datetime):
    """ Specialized subclass of datetime to support the date or datetime
    format used by Salesforce.com. 
    
    @note:  the magic here is that when coerced to string, this object is
            formatted ready to use by the Apex API.
    """

    @classmethod
    def fromSfIso(cls, sfdc_datetime_str):
        """ construct an ApexDatetime instance from a datetime string in UTC 

        @param sfdc_datetime_str: ISO formatted UTC time from Apex API call
        
        @return: passed datetime as an ApexDatetime
        @rtype: ApexDatetime 
        """
        global UTC
        global DATETIME_FORMAT
        
        timestamp = sfdc_datetime_str.split('.', 1)[0]
        timestruct = time.strptime(timestamp, DATETIME_FORMAT)

        return ApexDatetime(timestruct[0], # year
                            timestruct[1], # month
                            timestruct[2], # day
                            timestruct[3], # hour
                            timestruct[4], # minute
                            timestruct[5], # second
                            0, # microsecond
                            UTC)
 
    def __add__(self, td):
        newdt = datetime.__add__(self, td)
        return ApexDatetime.fromSfIso(newdt.isoformat())
    
    def __sub__(self, td):
        newdt = datetime.__sub__(self, td)
        if isinstance(newdt, datetime):
            return ApexDatetime.fromSfIso(newdt.isoformat())
        return newdt # actually a timedelta
          
    def __str__(self):
        return self.isoformat()


