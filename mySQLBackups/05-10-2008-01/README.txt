mySQLBackups automated the process of backing-up the contents of a mySQL Database from a local or remote server.

Usage:

--username=?                        ... username for the host account.
--binpath=?                         ... path to mySQL binaries.
--verbose                           ... output more stuff.
--freq=?                            ... how often (seconds) should the progpath be executed.
--destpath=?                        ... path to backups.
--host=?                            ... host address (127.0.0.1 by default).
--password=?                        ... password for the host user account.
--help                              ... displays this help text.
--maxbackups=?                      ... how many backups should be retained.

Typical Usage:

mySQLBackups --host=127.0.0.1 --username=root --password=password --binpath="C:\Program Files\MySQL\MySQL Server 5.0\bin" --destpath="d:\mySQLBackups" --maxbackups=60 --freq=14400

where:

--host=127.0.0.1 

This identifies the host which for this example is localhost or 127.0.0.1 however this could be any valid Internet address where an accessible instance of mySQL is located.

--username=root 

This is the username for your mySQL user account.

--password=password 

This is the password for your mySQL user account.

--binpath="C:\Program Files\MySQL\MySQL Server 5.0\bin" 

This is the path to your local copy of the mySQL binaries.

--destpath="d:\mySQLBackups" 

This is the path for your mySQL backups.

--maxbackups=60 

This is the number of backups you wish to retain at a time, all additional backups will be removed.

--freq=14400

This is the number of seconds between backups, approx every 4 hours.


This program is being published by Vyper Logix Corp. (http://www.VyperLogix.Com), 
Distributed by http://python2.near-by.info as a public service to the Python Community.
        
Disclaimer: The publsiher of this program makes no warranty as to the suitability
of this program for any purpose whatsoever nor is there any warranty to as to
whether this program will be able to properly handle your specific needs.
        
All materials not already covered by a copyright are covered by this copyright notice including all additions and enhancements
made by the publisher of this Windows .EXE rendition of the original Python Script(s):
(c). Copyright 2007-2008, Vyper Logix Corp., All Rights Reserved.

This software package and all contents contained herein may not be used for any
commercial purpose whatsoever however it may be used for educational purposes so
long as the end-goal or end-product is of a non-commercial purpose and there was
never any intent to use this package to generate any income of any kind.
        
You may not redistribute this package without prior written permission from the publisher.

License: GPL restricted to non-commercial educational use only.
