if %1. == more. goto domore
if %1. == profile. goto doprofile

nightlyBuild.py --yml=nightlyBuild.yml --ignoreSVN > test.txt

goto end

:domore
nightlyBuild.py --yml=nightlyBuild.yml --ignoreSVN | more
goto end

:doprofile
REM python -m cProfile -s cumulative nightlyBuild.py --yml=nightlyBuild.yml --ignoreSVN --makeMSI --zip="dss.zip" > test.txt
 python -m cProfile -s cumulative nightlyBuild.py --yml=nightlyBuild.yml --ignoreSVN --zip="dss.zip" > test.txt
goto end

:end

REM zip2exe.cmd

