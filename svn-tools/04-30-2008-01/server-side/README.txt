hot-backup performs a hot-copy of an SVN Repository followed by an archival process that collects all the files from the hot-copy
into a compressed archive, assuming the user selected a compressed archival format.

Perform a "hot" backup of a Subversion repository and clean any old Berkeley DB logfiles after the backup completes, 
if the repository backend is Berkeley DB.

USAGE: hot-backup.exe [OPTIONS] REPOS_PATH BACKUP_PATH

Create a backup of the repository at REPOS_PATH in a subdirectory of the BACKUP_PATH location, named after the youngest revision.

Options:
  --archive-type=FMT Create an archive of the backup. FMT can be one of:
                       bz2 : Creates a bzip2 compressed tar file.
                       gz  : Creates a gzip compressed tar file.
                       zip : Creates a compressed zip file.
  --num-backups=N    Number of prior backups to keep around (0 to keep all).
  --help      -h     Print this help message and exit.

The original hot-backup.py script is owned and copyrighted by Copyright (c) 2000-2007 CollabNet.  All rights reserved.

This rendition of hot-backup.exe is being published by Vyper Logix Corp. (http://www.VyperLogix.Com), 
Distributed by http://python2.near-by.info as a public service to the Python Community.
        
Disclaimer: The publsiher of this program makes no warranty as to the suitability
of this program for any purpose whatsoever nor is there any warranty to as to
whether this program will be able to properly handle your specific needs.
        
All materials not already covered by a copyright is covered by this copyright notice including all additions and enhancements
made by the publisher of this Windows .EXE rendition of the original Python Script:
(c). Copyright 2007-2008, Vyper Logix Corp., All Rights Reserved.

This software package and all contents contained herein may not be used for any
commercial purpose whatsoever however it may be used for educational purposes so
long as the end-goal or end-product is of a non-commercial purpose and there was
never any intent to use this package to generate any income of any kind.
        
You may not redistribute this package without prior written permission from the publisher.

License: GPL restricted to non-commercial educational use only.
