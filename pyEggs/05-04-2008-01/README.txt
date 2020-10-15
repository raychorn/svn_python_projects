pyCompileLib compiles all Python scripts contained within a folder tree into a cooresponding folder tree 
on another drive to facilitate delivery as a compiled library.

Usage:

--libroot=?                  ... path to root of the library.
--libdest=?                  ... path to root of the destination for the library (when not specified uses a temp folder).
--egg                        ... make-egg on the target.
--ignore=?                   ... [item,item] or [%libroot%\item,item] list of folders to ignore, such as archives or the like.
--nosource                   ... eggs laid without source.
--verbose                    ... output more stuff.
--barsvn                     ... use _svn as the ignore filter for svn.
--dotsvn                     ... use .svn as the ignore filter for svn (default in case both are either used or not used).
--help                       ... displays this help text.

Sample:

pyEggs --egg --libroot="Z:\python projects\@lib" --dotsvn --nosource --ignore="[%libroot%\archive]"

where:
    --egg  ................................ produces an egg in the folder in which this command was execute.
    --libroot="Z:\python projects\@lib" ... specifies the folder in which the source module(s) reside.
    --dotsvn .............................. ignores SVN files and folders that contain the .SVN substring.
    --nosource ............................ produces an egg without the source (remove this option to include the source).
    --ignore="[%libroot%\archive]" ........ ignores a list of folders, %libroot%\archive expands to specify the archive folder that resides within the root of the library.
    
Note:

You will not see any contents placed in the %libdest% folder, pyEggs cleans these contents after the egg has been produced.

The source files are not touched other than to compile all source files into .pyc files.

Published by Vyper Logix Corp. (http://www.VyperLogix.Com), Distributed by http://www.pypi.info
        
Disclaimer: The author of this program makes no warranty as to the suitability
of this program for any purpose whatsoever nor is there any warranty to as to
whether this program will be able to properly handle your specific needs.
        
(c). Copyright 2007-2008, Vyper Logix Corp., All Rights Reserved.
        
This software package and all contents contained herein may not be used for any
commercial purpose whatsoever however it may be used for educational purposes so
long as the end-goal or end-product is of a non-commercial purpose and there was
never any intent to use this package to generate any income of any kind.
        
You may not redistribute this package without prior written permission from the publisher.

License: GPL restricted to non-commercial educational use only.
