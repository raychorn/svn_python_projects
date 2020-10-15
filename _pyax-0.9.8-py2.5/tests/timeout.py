""" simple test for httplib timeout issue
"""
import sys
from datetime import datetime
from time import sleep

from pyax.connection import Connection
from pyax.sobject.classfactory import ClassFactory
    

def main():
    if len(sys.argv) < 3:
        usage("Incorrect number of arguments")
    else:
        username = sys.argv[1]
        passwd = sys.argv[2]

        if len(sys.argv) >= 4:
            timeoutsecs = sys.argv[3]
        
    try: 
        timeoutsecs = int(timeoutsecs)
    except:
        timeoutsecs = 300
    
    
    # log in to get an authenticated Connection object
    sfdc = Connection.connect(username, passwd)
        
    print "%s: initial call" %datetime.now()
    try:
        print sfdc.getServerTimestamp()
    except:
        pass
    
    print "%s: Sleeping for %s seconds" %(datetime.now(), timeoutsecs)
    sleep(timeoutsecs)
    
    print "%s: second call" %datetime.now()
    try:
        print sfdc.getServerTimestamp()
    except:
        pass
    
    
    print "%s: third call (no sleep)" %datetime.now()
    try:
        print sfdc.getServerTimestamp()
    except:
        pass
    
    return

if __name__ == "__main__":
    main()
    pass
    