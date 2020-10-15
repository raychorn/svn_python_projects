if %1. == Bigtest. goto Bigtest
if %1. == bes_data. goto bes_data

goto end

:Bigtest
 python -m cProfile -s cumulative main3.py --input=Bigtest.txt
goto end

:bes_data
 python -m cProfile -s cumulative main3.py --input=
goto end

:end
