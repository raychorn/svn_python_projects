if %1. == more. goto domore
if %1. == profile. goto doprofile

mySQL2MSSQL.py --yml=odbc.yml --tables --data --commit > test.txt

goto end

:domore
mySQL2MSSQL.py --yml=odbc.yml --tables --data --commit | more
goto end

:doprofile
 python -m cProfile -s cumulative mySQL2MSSQL.py --yml=odbc.yml --tables --data --commit > test.txt
goto end

:end
