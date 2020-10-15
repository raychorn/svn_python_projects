@echo off

"F:\@Downloads\Apache 2.3.8-alpha\httpd-2.3.8-alpha-x86\Apache23\bin\ab.exe" -n 10000 -c 1000 -w -k http://127.0.0.1:8888/ > test1-ab.html

goto end

"F:\@Downloads\Apache 2.3.8-alpha\httpd-2.3.8-alpha-x86\Apache23\bin\ab.exe" -n 1000 -c 1 -w -k http://127.0.0.1:8888/ > "F:\@Vyper Logix Corp\@Projects\python\Stackless Python\stacklesswsgi\single-process\test1-ab-1.html"
"F:\@Downloads\Apache 2.3.8-alpha\httpd-2.3.8-alpha-x86\Apache23\bin\ab.exe" -n 1000 -c 2 -w -k http://127.0.0.1:8888/ > "F:\@Vyper Logix Corp\@Projects\python\Stackless Python\stacklesswsgi\single-process\test1-ab-2.html"
"F:\@Downloads\Apache 2.3.8-alpha\httpd-2.3.8-alpha-x86\Apache23\bin\ab.exe" -n 1000 -c 5 -w -k http://127.0.0.1:8888/ > "F:\@Vyper Logix Corp\@Projects\python\Stackless Python\stacklesswsgi\single-process\test1-ab-5.html"
"F:\@Downloads\Apache 2.3.8-alpha\httpd-2.3.8-alpha-x86\Apache23\bin\ab.exe" -n 1000 -c 10 -w -k http://127.0.0.1:8888/ > "F:\@Vyper Logix Corp\@Projects\python\Stackless Python\stacklesswsgi\single-process\test1-ab-10.html"

:end
