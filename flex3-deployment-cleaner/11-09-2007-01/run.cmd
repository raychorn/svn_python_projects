if %1. == more. goto domore
if %1. == profile. goto doprofile

goto end

:domore
flex3cleaner.py --folder="Z:\Ruby In Steel\BigFix_DSS\reports\public\BigFixDSS" --svn=".svn" --base="\\public\\" --target="dss" > test.txt
goto end

:doprofile
 python -m cProfile -s cumulative flex3cleaner.py --folder="Z:\Ruby In Steel\BigFix_DSS\reports\public\BigFixDSS" --svn=".svn" --base="\\public\\" --target="dss" > test.txt
goto end

:end
if exist dos.cmd dos.cmd

