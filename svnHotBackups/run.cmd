@echo off
cls
echo BEGIN:

set PYTHONPATH=c:\python25\lib;j:\@Vyper Logix Corp\@Projects\python-projects\@lib\12-13-2011-01;

REM python svnHotBackups.py --archive-type=bzip --num-backups=100 --repo-path=Z:\svn --backup-dir=C:\@1d

REM python sftp.py --computer=misha-lap.ad.magma-da.com --verbose --server=river --username=sfscript --password=sf@magma05 --source=C:\@1d\*.zip --dest=/home/sfscript/@data

REM python sftp.py --computer=misha-lap.ad.magma-da.com --verbose --server=river --username=sfscript --password=sf@magma05 --source=C:\@1d\*.gz --dest=/home/sfscript/@data

REM python sftp.py --computer=misha-lap.ad.magma-da.com --verbose --server=river --username=sfscript --password=sf@magma05 --source=C:\@1d\*.txt --dest=/home/sfscript/@data

REM C:\@utils\svnHotBackups\bin\svnHotBackups.exe --restore="C:\#svn_backups\avikohn\avikohn-2.bzip" --repo-path="C:\#svn_backups\avikohn-restore" > run_log_avikohn.txt

REM --verbose --archive-type=bzip --num-backups=4 --repo-path="F:\#svn\repo1" --backup-dir="F:/#svn_backups/repo1" --carbonite="P:\#svn_backups" --carbonite-hours=24 --carbonite-files=4 --carbonite-optimize=1 --carbonite-schedule=?type1=Primary&days1=M-F&hours1=0-20&type2=Alt&days2=Sa-Su&hours2=*

REM --verbose --archive-type=bzip --num-backups=2 --repo-path="J:\#svn\repo1" --backup-dir="J:\#svn_backups" --carbonite="J:\#svn_backups(Carbonite)" --carbonite-hours=24 --carbonite-files=2 --carbonite-optimize=1

REM python svnHotBackups.py --verbose --archive-type=bzip --num-backups=2 --repo-path="J:\#svn\repo1" --backup-dir="J:\#svn_backups" --carbonite="J:\#svn_backups(Carbonite)" --carbonite-hours=24 --carbonite-files=2 --carbonite-optimize=1 --aws_access_key=AKIAI52A6BTLWZHHDLCA --aws_secret_access_key=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 --bucket=__vyperlogix_svn_backups__

REM S3Delete.exe -AWSAccessKeyId AKIAI52A6BTLWZHHDLCA -AWSSecretAccessKey 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 -BucketName __vyperlogix_svn_backups__ -S3KeyName "testing/launch-pageant.cmd" -LogOnlyMode False

REM s3 put __vyperlogix_svn_backups__/testing/ "J:\@8\programming-test-php-08-23-2012.zip" /yes /key:AKIAI52A6BTLWZHHDLCA /secret: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

REM "J:\@Vyper Logix Corp\@Projects\python-projects\svnHotBackups\S3Delete.exe" -AWSAccessKeyId AKIAI52A6BTLWZHHDLCA -AWSSecretAccessKey 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 -BucketName __vyperlogix_svn_backups__ -S3KeyName "testing/programming-test-php-08-23-2012.zip" -LogOnlyMode False

REM s3 list __vyperlogix_svn_backups__/testing /key:AKIAI52A6BTLWZHHDLCA /secret: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


REM C:\@utils\svnHotBackups\bin\svnHotBackups.exe --restore="backups/repo1-16030.bzip" --repo-path="J:/#svn_backups(Test)/" --aws_access_key=AKIAI52A6BTLWZHHDLCA --aws_secret_access_key=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 --bucket=__vyperlogix_svn_backups__ > run_log_avikohn.txt

REM --verbose --test --archive-type=bzip --num-backups=2 --repo-path="J:\#svn\repo1" --backup-dir="J:\#svn_backups" --carbonite="J:\#svn_backups(Carbonite)" --carbonite-hours=24 --carbonite-files=2 --carbonite-optimize=1 --aws_access_key=AKIAI52A6BTLWZHHDLCA --aws_secret_access_key=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

REM --verbose --debug --archive-type=bzip --num-backups=2 --repo-path="J:/#svn/repo1" --backup-dir="J:/#svn_backups" --aws_access_key=AKIAI52A6BTLWZHHDLCA --aws_secret_access_key=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 --bucket=__vyperlogix_svn_backups__

@echo on

REM s3 list __vyperlogix_svn_backups__/testing /key:AKIAI52A6BTLWZHHDLCA /secret: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

REM s3 get "__vyperlogix_svn_backups__/testing/To-Do.txt" "J:/@7/To-Do.txt" /key:AKIAI52A6BTLWZHHDLCA /secret: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

REM dist\svnHotBackups.exe --verbose --restore="testing/To-Do.txt" --repo-path="J:/#svn_backups(Test)/" --aws_access_key=AKIAI52A6BTLWZHHDLCA --aws_secret_access_key=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 --bucket=__vyperlogix_svn_backups__

REM --verbose --debug --test --skipZiptest --restore="backups" --newest --backup-dir="J:/#svn_backups(Test)/" --repo-path="J:/#svn/repo1" --aws_access_key=AKIAI52A6BTLWZHHDLCA --aws_secret_access_key=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 --bucket=__vyperlogix_svn_backups__

dist\svnHotBackups.exe --verbose --debug --test --restore="backups" --newest --backup-dir="J:/#svn_backups(Test)/" --repo-path="J:/#svn/repo1" --aws_access_key=AKIAI52A6BTLWZHHDLCA --aws_secret_access_key=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 --bucket=__vyperlogix_svn_backups__


echo END!

