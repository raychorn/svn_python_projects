if %1. == profile. goto profile

goto end

:profile
 python -m cProfile -s cumulative main.py
goto end

:end
