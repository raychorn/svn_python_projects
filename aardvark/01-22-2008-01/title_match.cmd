if %1. == more. goto domore

title_matching.py --match=0 > test.txt

goto end

:domore
title_matching.py --match=0 | more
goto end

:end
