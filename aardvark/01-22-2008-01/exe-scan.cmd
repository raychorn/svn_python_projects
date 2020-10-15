if %1. == more. goto domore
if %1. == profile. goto doprofile

exe-scanner2.py > test.txt

goto end

:domore
exe-scanner2.py | more
goto end

:doprofile
 python -m cProfile -s cumulative exe-scanner2.py > test.txt
goto end

:end
