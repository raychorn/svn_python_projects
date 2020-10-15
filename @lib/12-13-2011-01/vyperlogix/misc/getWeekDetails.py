import datetime

def weekDetails(year, week):
    from datetime import date, timedelta
    d = date(year,1,1) 
    d = d - timedelta(d.weekday())
    dlt = timedelta(days = (week-1)*7)
    return d + dlt,  d + dlt + timedelta(days=6)

if __name__ == '__main__':
    weeks = xrange(1,52)
    for w in weeks:
        x = weekDetails(2008,w)
        print "Monday of Week %s: %s \n" % (w, x[0])
        print "Sunday of Week %s: %s \n" % (w, x[1])
