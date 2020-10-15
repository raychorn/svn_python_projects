@echo off
cls
echo BEGIN:

cd dist
compdb -c ..\analytics_portal_test-bouygues-portal.sql ..\analytics_portal_dev_test.sql
cd ..

echo END!
