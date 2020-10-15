REM http://blog.cartviper.com/post/2012/04/02/Backup-Subversion-to-Amazon-S3.aspx

set path="C:\Program Files (x86)\VisualSVN Server\bin"

svnadmin hotcopy c:\Repositories\Btb "c:\svn backup\temp\Btb"

"C:\Program Files (x86)\SprightlySoft S3 Sync\S3Sync\S3Sync.exe" -AWSAccessKeyId xxxxxx -AWSSecretAccessKey xxxxxx -SyncDirection upload -LocalFolderPath "c:\svn backup\temp" -bucketName SubversionBackup

rd "c:\svn backup\temp\Btb" /q /s
