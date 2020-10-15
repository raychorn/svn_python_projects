#!/bin/bash

if [ -f /root/bin/PYTHONPATH ]; then
	. /root/bin/PYTHONPATH
fi

# python svnHotBackups.py --verbose --archive-type=bzip --num-backups=4 --repo-path="/var/local/svn/repo1" --backup-dir="/var/local/svn/#svn_backups/repo1" --s3="/etc/boto.cfg" --carbonite-hours=24 --carbonite-files=4 --carbonite-optimize=1 --carbonite-schedule="?type1=Primary&days1=M-F&hours1=0-20&type2=Alt&days2=Sa-Su&hours2=*" >./logs/svnHotBackups.log 2>&1

 python svnHotBackups.py --verbose --archive-type=gz --num-backups=4 --repo-path="/var/local/svn/repo1" --backup-dir="/var/local/svn/#svn_backups/repo1" --s3="/etc/boto.cfg" --carbonite-hours=24 --carbonite-files=4 --carbonite-optimize=1 --carbonite-schedule="?type1=Primary&days1=M-F&hours1=0-20&type2=Alt&days2=Sa-Su&hours2=*" >./logs/svnHotBackups.log 2>&1

# python svnHotBackups.py --verbose --archive-type=none --num-backups=4 --repo-path="/var/local/svn/repo1" --backup-dir="/var/local/svn/#svn_backups/repo1" --s3="/etc/boto.cfg" --carbonite-hours=24 --carbonite-files=4 --carbonite-optimize=1 --carbonite-schedule="?type1=Primary&days1=M-F&hours1=0-20&type2=Alt&days2=Sa-Su&hours2=*" >./logs/svnHotBackups.log 2>&1

src="/root/#svn_backups/repo1"
 
IFS=$'\n'
 
for dir in `ls "$src/"`
do
  if [ -d "$src/$dir" ]; then
    #tar cvzf $src/$dir.tar.gz $src/$dir/
    rm -f -R $src/$dir
  fi
done
