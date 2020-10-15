if %1. == . goto Bigtest
if %1. == test. goto Bigtest2
if %1. == input. goto Bigtest3
if %1. == bcp. goto Bigtest4
if %1. == bcpt5. goto Bigtest4t5
if %1. == bcpt500. goto Bigtest4t500

goto end

:Bigtest
 python -m cProfile -s cumulative bcp.py --output=Bigtest.txt
goto end

:Bigtest2
 python -m cProfile -s cumulative bcp.py --test=Bigtest.txt
goto end

:Bigtest3
 python -m cProfile -s cumulative bcp.py --input=Bigtest.txt
goto end

:Bigtest4
 python -m cProfile -s cumulative bcp.py --bcp=Bigtest.txt
goto end

:Bigtest4t5
 python -m cProfile -s cumulative bcp.py --threaded=5 --bcp=Bigtest.txt
goto end

:Bigtest4t500
 python -m cProfile -s cumulative bcp.py --threaded=500 --bcp=Bigtest.txt
goto end

:end
