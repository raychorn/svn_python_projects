if %1. == more. goto domore
if %1. == profile. goto doprofile

setup.py --yml=setup.yml > test.txt

goto end

:domore
setup.py --yml=setup.yml | more
goto end

:doprofile
 python -m cProfile -s cumulative setup.py --yml=setup.yml > test.txt
goto end

:end

