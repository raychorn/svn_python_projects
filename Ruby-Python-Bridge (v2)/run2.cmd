@echo off
set PYTHONPATH=C:\Python25\lib;Z:\@myMagma\python-local-new-trunk-ruby-daemon;Z:\@myMagma\python-local-new-trunk;Z:\@myMagma\python-local-new-trunk-ruby-daemon\bridge;Z:\python projects\@lib;Z:\@myMagma\python-local-new-trunk\sfapi2\sflib;
cls
if %1. == . python pythonProcess.py
if %1. == 1. goto multi_test
goto end

:multi_test
start "Python #1" /ABOVENORMAL python pythonProcess.py

start "Ruby #1" /ABOVENORMAL ruby ruby\rubyProcess.rb
start "Ruby #2" /ABOVENORMAL ruby ruby\rubyProcess.rb
REM start "Ruby #3" /ABOVENORMAL ruby ruby\rubyProcess.rb
REM start "Ruby #4" /ABOVENORMAL ruby ruby\rubyProcess.rb
REM start "Ruby #5" /ABOVENORMAL ruby ruby\rubyProcess.rb
REM start "Ruby #6" /ABOVENORMAL ruby ruby\rubyProcess.rb
REM start "Ruby #7" /ABOVENORMAL ruby ruby\rubyProcess.rb
REM start "Ruby #8" /ABOVENORMAL ruby ruby\rubyProcess.rb
REM start "Ruby #9" /ABOVENORMAL ruby ruby\rubyProcess.rb
REM start "Ruby #10" /ABOVENORMAL ruby ruby\rubyProcess.rb
:end
