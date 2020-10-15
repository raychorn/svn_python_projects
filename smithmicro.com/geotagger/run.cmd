@echo off

REM set PYTHONPATH=j:\Python2557(Stackless)-09-02-2010\Python25;j:\@Vyper Logix Corp\@Projects\python\@lib;J:\@Vyper Logix Corp\@Projects\python\_google_appengine_1_5_1\lib\django_1_2;
set PYTHONPATH=j:\Python2557(Stackless)-09-02-2010\Python25;j:\@Vyper Logix Corp\@Projects\python\@lib;J:\@Vyper Logix Corp\@Projects\python\_google_appengine_1_5_1\lib\django_1_2;j:\@Vyper Logix Corp\@Projects\python\SQLAlchemy-0.7.1\lib;
set DJANGO_SETTINGS_MODULE=settings
REM python25.exe results_sampler.py --fpath=ray_gps_out.xml

REM python25.exe results_sampler.py --fpath="J:\@Vyper Logix Corp\@Projects\python\smithmicro.com\geotagger\@paris_10_out\paris_10_out.xml"

python25.exe results_sampler.py --fpath="J:\@Vyper Logix Corp\@Projects\python\smithmicro.com\geotagger\@Data-From-Fred\gps_SFBay_10M_70-20-10\gps_SFBay_10M_70-20-10.xml"

REM python25.exe results_sampler.py --fpath="J:\@Vyper Logix Corp\@Projects\python\smithmicro.com\geotagger\@paris_20_out\paris_20_out.xml"

REM python25.exe results_sampler.py --fpath="J:\@Vyper Logix Corp\@Projects\python\smithmicro.com\geotagger\@gps_1M\gps_1M.xml"

REM python25.exe results_sampler.py --mysql --profiler

REM python25.exe results_sampler.py --mysql --mongodb=gps_1M --mongoip=127.0.0.1 --mongoport=65535 --dropdb --profiler 1> results_sampler_log.txt 2>&1

REM python25.exe results_sampler.py --mysql --etl

