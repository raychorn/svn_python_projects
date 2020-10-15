if %1. == profile. goto doprofile

Concordance2.py > test2.txt

goto end

:doprofile
 python -m cProfile -s cumulative Concordance2.py > test2.txt
goto end

:end
